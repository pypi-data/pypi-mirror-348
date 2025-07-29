# === File: act/nodes/gemini_node.py ===

import logging
import json
import os
import asyncio
from typing import Dict, Any, Optional, List, Union, Callable

try:
    from .base_node import (
        BaseNode,
        NodeSchema,
        NodeParameter,
        NodeParameterType,
        NodeValidationError,
        NodeExecutionError,
    )
except ImportError:
    # Fallback for running standalone
    print("Warning: Could not import from .base_node. Using placeholder BaseNode.")
    class NodeValidationError(Exception): pass
    class NodeExecutionError(Exception): pass
    class NodeParameterType: ANY="any"; STRING="string"; BOOLEAN="boolean"; NUMBER="number"; ARRAY="array"; OBJECT="object"; SECRET="secret"
    class NodeParameter:
        def __init__(self, name, type, description, required=True, default=None, enum=None):
            self.name = name; self.type = type; self.description = description; self.required = required; self.default = default; self.enum = enum
    class NodeSchema:
        def __init__(self, node_type, version, description, parameters, outputs, tags=None, author=None):
            self.node_type=node_type; self.version=version; self.description=description; self.parameters=parameters; self.outputs=outputs; self.tags=tags; self.author=author
    class BaseNode:
        def get_schema(self): raise NotImplementedError
        async def execute(self, data): raise NotImplementedError
        def validate_schema(self, data): return data.get("params", {})
        def handle_error(self, error, context=""):
             logger = logging.getLogger(__name__)
             logger.error(f"Error in {context}: {error}", exc_info=True)
             return {"status": "error", "message": f"Error in {context}: {error}", "error_type": type(error).__name__}

# --- Node Logger ---
logger = logging.getLogger(__name__)

# --- Optional global client for efficiency ---
_gemini_client = None

class GeminiNode(BaseNode):
    """
    Node for interacting with Google's Gemini models via the Google AI Studio API.
    Provides capabilities for generating text, analyzing images, and more using
    the Gemini models.
    """

    def get_schema(self) -> NodeSchema:
        """Returns the schema definition for the GeminiNode."""
        return NodeSchema(
            node_type="gemini",
            version="1.0.0",
            description="Generates text and processes multimodal inputs using Google's Gemini models",
            parameters=[
                NodeParameter(
                    name="api_key",
                    type=NodeParameterType.SECRET,
                    description="Google AI Studio API key. If not provided, will use GEMINI_API_KEY environment variable.",
                    required=False,
                    default="${GEMINI_API_KEY}"
                ),
                NodeParameter(
                    name="model",
                    type=NodeParameterType.STRING,
                    description="Gemini model to use (e.g. 'gemini-1.5-pro', 'gemini-1.5-flash', 'gemini-2.5-pro-preview-03-25')",
                    required=True,
                    default="gemini-1.5-pro"
                ),
                NodeParameter(
                    name="prompt",
                    type=NodeParameterType.STRING,
                    description="The text prompt to send to Gemini",
                    required=True
                ),
                NodeParameter(
                    name="temperature",
                    type=NodeParameterType.NUMBER,
                    description="Controls randomness. Lower values are more deterministic (range: 0.0 to 1.0)",
                    required=False,
                    default=0.7
                ),
                NodeParameter(
                    name="max_output_tokens",
                    type=NodeParameterType.NUMBER,
                    description="Maximum number of tokens to generate",
                    required=False,
                    default=None
                ),
                NodeParameter(
                    name="top_p",
                    type=NodeParameterType.NUMBER,
                    description="Nucleus sampling parameter (range: 0.0 to 1.0)",
                    required=False,
                    default=None
                ),
                NodeParameter(
                    name="top_k",
                    type=NodeParameterType.NUMBER,
                    description="Number of highest probability tokens to consider (range: 1 to 40)",
                    required=False,
                    default=None
                ),
                NodeParameter(
                    name="stream",
                    type=NodeParameterType.BOOLEAN,
                    description="Whether to stream the response",
                    required=False,
                    default=False
                ),
                NodeParameter(
                    name="mime_type",
                    type=NodeParameterType.STRING,
                    description="Response mime type (e.g. 'text/plain', 'application/json')",
                    required=False,
                    default="text/plain"
                ),
                NodeParameter(
                    name="images",
                    type=NodeParameterType.ARRAY,
                    description="Optional array of image URLs or base64 encoded images to include with the prompt",
                    required=False,
                    default=None
                )
            ],
            outputs={
                "result_text": NodeParameterType.STRING,
                "finish_reason": NodeParameterType.STRING,
                "usage": NodeParameterType.OBJECT,
                "full_response": NodeParameterType.OBJECT
            },
            tags=["ai", "nlp", "text generation", "chat", "multimodal", "google", "gemini"],
            author="ACT Framework"
        )

    async def execute(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        """Executes the Gemini operation with the provided data."""
        node_name = node_data.get('__node_name', 'GeminiNode')
        logger.debug(f"Executing GeminiNode: {node_name}")

        try:
            # Extract parameters
            params = node_data.get("params", {})
            
            # Try to import Google Gemini library
            try:
                from google import genai
                from google.genai import types
            except ImportError:
                raise NodeExecutionError("Required package 'google-generativeai' is not installed. Install with 'pip install google-generativeai'")
            
            # Get API key (prioritize parameter, then environment variable)
            api_key = params.get("api_key") or os.environ.get("GEMINI_API_KEY")
            if not api_key:
                raise NodeValidationError("No API key provided. Either set the 'api_key' parameter or GEMINI_API_KEY environment variable.")
            
            # Get required parameters
            model = params.get("model", "gemini-1.5-pro")
            prompt = params.get("prompt")
            if not prompt:
                raise NodeValidationError("No prompt provided. The 'prompt' parameter is required.")
            
            # Get optional parameters
            temperature = params.get("temperature")
            max_output_tokens = params.get("max_output_tokens")
            top_p = params.get("top_p")
            top_k = params.get("top_k")
            stream = params.get("stream", False)
            mime_type = params.get("mime_type", "text/plain")
            images = params.get("images", [])
            
            # Create client
            global _gemini_client
            if _gemini_client is None:
                _gemini_client = genai.Client(api_key=api_key)
            client = _gemini_client
            
            # Set up the contents for the request
            user_parts = []
            
            # Add text prompt
            user_parts.append(types.Part.from_text(text=prompt))
            
            # Add images if provided
            for image in images:
                if image.startswith("http"):
                    # If it's a URL
                    user_parts.append(types.Part.from_uri(uri=image, mime_type="image/jpeg"))
                elif image.startswith("data:"):
                    # If it's a data URI
                    parts = image.split(";base64,")
                    if len(parts) == 2:
                        mime = parts[0].replace("data:", "")
                        data = parts[1]
                        user_parts.append(types.Part.from_data(data=base64.b64decode(data), mime_type=mime))
                else:
                    # Assume it's base64
                    try:
                        user_parts.append(types.Part.from_data(data=base64.b64decode(image), mime_type="image/jpeg"))
                    except:
                        logger.warning(f"Unable to decode image data: {image[:30]}...")
            
            # Create content object with user parts
            contents = [
                types.Content(
                    role="user",
                    parts=user_parts
                )
            ]
            
            # Create generate content config
            generate_content_config = types.GenerateContentConfig(
                response_mime_type=mime_type,
            )
            
            # Add temperature if provided
            if temperature is not None:
                generate_content_config.temperature = float(temperature)
                
            # Add max_output_tokens if provided  
            if max_output_tokens is not None:
                generate_content_config.max_output_tokens = int(max_output_tokens)
                
            # Add top_p if provided
            if top_p is not None:
                generate_content_config.top_p = float(top_p)
                
            # Add top_k if provided
            if top_k is not None:
                generate_content_config.top_k = int(top_k)
            
            logger.info(f"{node_name} - Executing Gemini with model '{model}', temperature={temperature}, max_tokens={max_output_tokens or 'default'}")
            
            # Handle streaming vs non-streaming
            try:
                if stream:
                    # Use run_in_executor to make synchronous API call asynchronous
                    def generate_stream():
                        result_text = ""
                        for chunk in client.models.generate_content_stream(
                            model=model,
                            contents=contents,
                            config=generate_content_config,
                        ):
                            if chunk.text:
                                result_text += chunk.text
                        return result_text
                    
                    # Execute the stream processing
                    result_text = await asyncio.to_thread(generate_stream)
                    
                else:
                    # Synchronous response, made async
                    def generate_content():
                        response = client.models.generate_content(
                            model=model,
                            contents=contents,
                            config=generate_content_config,
                        )
                        return response
                    
                    # Execute the content generation
                    response = await asyncio.to_thread(generate_content)
                    result_text = response.text
                    full_response = response
                
                logger.info(f"{node_name} - Successfully generated content with Gemini. Result length: {len(result_text)} chars")
                
                return {
                    "status": "success",
                    "message": "Gemini operation completed successfully.",
                    "result": {
                        "result_text": result_text,
                        "finish_reason": "stop",  # Gemini doesn't expose this directly
                        "usage": {},  # Gemini doesn't expose token usage like OpenAI
                        "full_response": full_response if not stream else None
                    }
                }
                
            except Exception as e:
                error_msg = f"Error during Gemini API call: {str(e)}"
                logger.error(f"{node_name} - {error_msg}")
                return self.handle_error(e, context=f"{node_name} API Call")
            
        except Exception as e:
            logger.error(f"Error in {node_name}: {str(e)}", exc_info=True)
            return self.handle_error(e, context=node_name)

# For standalone testing
if __name__ == "__main__":
    import asyncio
    import os
    
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s [%(levelname)s] - %(message)s'
    )
    
    async def test_gemini():
        print("\n--- Testing GeminiNode ---")
        node = GeminiNode()
        print(f"Schema: {node.get_schema()}")
        
        # Make sure API key is set
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            print("❌ GEMINI_API_KEY environment variable not set. Please set it to run this test.")
            return
        
        # Test data
        test_data = {
            "__node_name": "TestGemini",
            "params": {
                "model": "gemini-1.5-pro",
                "prompt": "Explain quantum computing in simple terms.",
                "temperature": 0.7,
                "max_output_tokens": 200,
                "stream": False
            }
        }
        
        # Execute
        print("\nExecuting node...")
        result = await node.execute(test_data)
        
        # Print result
        print("\nResult:")
        print(f"Status: {result.get('status')}")
        print(f"Message: {result.get('message')}")
        print("\nGenerated text:")
        print("----------------------------")
        print(result.get('result', {}).get('result_text', 'No text generated'))
        print("----------------------------")
    
    asyncio.run(test_gemini())