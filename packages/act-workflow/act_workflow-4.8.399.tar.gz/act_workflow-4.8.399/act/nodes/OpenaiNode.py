# === File: act/nodes/openai_node.py ===

import logging
import os
import json
from typing import Dict, Any, Optional, List, Union

# Assuming base_node.py is in the same directory or accessible via the package structure
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
    # Fallback for running standalone or if structure is different
    print("Warning: Could not import from .base_node. Using placeholder BaseNode.")
    # Define dummy classes if BaseNode cannot be imported
    class NodeValidationError(Exception): pass
    class NodeExecutionError(Exception): pass
    class NodeParameterType: ANY="any"; STRING="string"; BOOLEAN="boolean"; NUMBER="number"; ARRAY="array"; OBJECT="object"; SECRET="secret"
    class NodeParameter:
        def __init__(self, name, type, description, required=True, default=None, enum=None):
            self.name = name
            self.type = type
            self.description = description
            self.required = required
            self.default = default
            self.enum = enum
    class NodeSchema:
        def __init__(self, node_type, version, description, parameters, outputs, tags=None, author=None):
            self.node_type = node_type
            self.version = version
            self.description = description
            self.parameters = parameters
            self.outputs = outputs
            self.tags = tags
            self.author = author
    class BaseNode:
        def get_schema(self): raise NotImplementedError
        async def execute(self, data): raise NotImplementedError
        def validate_schema(self, data): return data.get("params", {}) # Simplistic
        def handle_error(self, error, context=""):
             logger = logging.getLogger(__name__) # Need logger in fallback too
             logger.error(f"Error in {context}: {error}", exc_info=True)
             return {"status": "error", "message": f"Error in {context}: {error}", "error_type": type(error).__name__}

# --- OpenAI Specific Imports ---
try:
    # Use the async client from openai v1.0+
    from openai import AsyncOpenAI, OpenAIError
    # Specific error types can be useful
    from openai import APIConnectionError, RateLimitError, APIStatusError, BadRequestError
    OPENAI_SDK_AVAILABLE = True
except ImportError:
    print("Warning: 'openai' package not found. OpenAINode will not function.")
    print("Install it using: pip install openai")
    # Define dummy classes/exceptions if openai is not installed
    class OpenAIError(Exception): pass
    class APIConnectionError(OpenAIError): pass
    class RateLimitError(OpenAIError): pass
    class APIStatusError(OpenAIError): pass
    class BadRequestError(OpenAIError): pass
    class AsyncOpenAI: # Dummy client
         def __init__(self, api_key=None): pass
         # Add dummy methods if needed for type checking, though execute will fail first
         class Chat:
             class Completions:
                 async def create(self, *args, **kwargs): raise OpenAIError("OpenAI SDK not installed")
             completions = Completions()
         chat = Chat()
    OPENAI_SDK_AVAILABLE = False

# --- Node Logger ---
logger = logging.getLogger(__name__)
# Example: logger = logging.getLogger("act.nodes.OpenAINode")

# --- Node Implementation ---

class OpenAINode(BaseNode):
    """
    Interacts with the OpenAI API (v1.0+ SDK) to perform operations like chat completions.
    Requires an API key provided via parameters or environment variables (resolved by ExecutionManager).
    """

    SUPPORTED_OPERATIONS = ["chat_completion"] # Extend later with "embedding", etc.

    def get_schema(self) -> NodeSchema:
        """Returns the schema definition for the OpenAINode."""
        return NodeSchema(
            node_type="openai", # Or "OpenAINode" if preferred
            version="1.0.0",
            description="Calls the OpenAI API for tasks like chat completion.",
            parameters=[
                NodeParameter(
                    name="api_key",
                    type=NodeParameterType.SECRET,
                    description="OpenAI API Key. Best practice: Use ${ENV_VAR} placeholder resolved by the manager.",
                    required=True
                ),
                NodeParameter(
                    name="operation",
                    type=NodeParameterType.STRING,
                    description="The OpenAI operation to perform.",
                    required=True,
                    enum=self.SUPPORTED_OPERATIONS,
                    default="chat_completion"
                ),
                NodeParameter(
                    name="model",
                    type=NodeParameterType.STRING,
                    description="The OpenAI model to use (e.g., 'gpt-4o', 'gpt-3.5-turbo').",
                    required=True,
                    default="gpt-4o" # Set a sensible default
                ),
                NodeParameter(
                    name="messages",
                    type=NodeParameterType.ARRAY, # Expecting list of dicts
                    description="A list of message objects for chat completion (e.g., [{'role': 'user', 'content': '...'}]). Required for 'chat_completion'.",
                    required=False # Required based on operation check later
                ),
                NodeParameter(
                    name="prompt",
                    type=NodeParameterType.STRING,
                    description="A simple prompt string (alternative to 'messages' for basic user input). If provided and 'messages' is not, it will be wrapped as a user message.",
                    required=False
                ),
                NodeParameter(
                    name="temperature",
                    type=NodeParameterType.NUMBER,
                    description="Sampling temperature (0-2). Higher values make output more random.",
                    required=False,
                    default=0.7
                ),
                NodeParameter(
                    name="max_tokens",
                    type=NodeParameterType.NUMBER,
                    description="Maximum number of tokens to generate.",
                    required=False,
                    default=None # Let OpenAI use its default if not specified
                ),
                # Add other common OpenAI parameters as needed (e.g., top_p, frequency_penalty)
            ],
            outputs={
                "result_text": NodeParameterType.STRING, # The primary text output
                "finish_reason": NodeParameterType.STRING, # e.g., 'stop', 'length'
                "usage": NodeParameterType.OBJECT, # Dictionary with token counts
                "full_response": NodeParameterType.OBJECT # The complete, raw response object from OpenAI SDK
            },
            tags=["ai", "llm", "openai", "language", "generation"],
            author="ACT Framework" # Or your name/org
        )

    async def execute(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        """Executes the specified OpenAI API operation."""
        node_name = node_data.get('__node_name', 'OpenAINode')
        logger.debug(f"Executing OpenAINode: {node_name}")

        if not OPENAI_SDK_AVAILABLE:
             return self.handle_error(NodeExecutionError("OpenAI SDK is not installed."), context=node_name)

        try:
            # 1. Extract and Validate Parameters
            params = node_data.get("params", {})
            api_key = params.get("api_key")
            operation = params.get("operation", "chat_completion")
            model = params.get("model", "gpt-4o")
            messages = params.get("messages") # Should be list of dicts if provided
            prompt = params.get("prompt") # Simple string prompt
            temperature = params.get("temperature", 0.7)
            max_tokens = params.get("max_tokens") # Can be None

            # --- Input Validation ---
            if not api_key:
                raise NodeValidationError("Missing required parameter 'api_key'.")
            if operation not in self.SUPPORTED_OPERATIONS:
                 raise NodeValidationError(f"Unsupported operation '{operation}'. Supported: {self.SUPPORTED_OPERATIONS}")

            # Prepare messages for chat completion
            message_list: Optional[List[Dict[str, str]]] = None
            if operation == "chat_completion":
                if isinstance(messages, list) and messages:
                    # Validate basic message structure (can be more thorough)
                    if not all(isinstance(m, dict) and 'role' in m and 'content' in m for m in messages):
                         raise NodeValidationError("Invalid 'messages' format. Expected list of {'role': str, 'content': str} dictionaries.")
                    message_list = messages
                    logger.debug(f"{node_name} - Using provided 'messages' list ({len(message_list)} messages).")
                elif isinstance(prompt, str) and prompt:
                    # If only prompt is given, wrap it in a user message
                    message_list = [{"role": "user", "content": prompt}]
                    logger.debug(f"{node_name} - Using 'prompt' converted to single user message.")
                else:
                    raise NodeValidationError("Missing required input for 'chat_completion': Provide either 'messages' (list) or 'prompt' (string).")

            # --- (Add validation for other operations here if implemented) ---

            # Log parameters (excluding API key)
            log_params = params.copy()
            log_params['api_key'] = '[REDACTED]'
            logger.info(f"{node_name} - Executing operation '{operation}' with model '{model}' and params: {json.dumps(log_params, default=str)}")


            # 2. Initialize OpenAI Async Client
            # Initialized per-execution to use the provided key
            try:
                client = AsyncOpenAI(api_key=api_key)
                logger.debug(f"{node_name} - AsyncOpenAI client initialized.")
            except Exception as client_err: # Catch potential init errors
                 raise NodeExecutionError(f"Failed to initialize OpenAI client: {client_err}")


            # 3. Perform API Call based on Operation
            response = None
            if operation == "chat_completion":
                logger.debug(f"{node_name} - Calling chat.completions.create...")
                api_call_params = {
                    "model": model,
                    "messages": message_list,
                    "temperature": temperature,
                }
                # Add max_tokens only if it's provided and valid
                if isinstance(max_tokens, (int, float)) and max_tokens >= 1:
                    api_call_params["max_tokens"] = int(max_tokens)
                elif max_tokens is not None:
                     logger.warning(f"{node_name} - Invalid 'max_tokens' value ({max_tokens}), ignoring.")

                # --- API Call ---
                response = await client.chat.completions.create(**api_call_params)
                logger.debug(f"{node_name} - OpenAI API call successful.")

            # --- (Add elif blocks for other operations like embeddings) ---
            # elif operation == "embedding":
            #     # ... implementation ...
            #     pass

            else:
                 # Should be caught by validation earlier, but safeguard
                 raise NodeExecutionError(f"Operation '{operation}' logic not implemented.")


            # 4. Process Successful Response
            if response:
                # Use model_dump() for Pydantic V2+ compatibility in openai SDK >= 1.0
                full_response_dict = response.model_dump() if hasattr(response, 'model_dump') else response.dict()

                result_text = None
                finish_reason = None
                usage = None

                if operation == "chat_completion":
                    if response.choices:
                        first_choice = response.choices[0]
                        finish_reason = first_choice.finish_reason
                        if first_choice.message:
                            result_text = first_choice.message.content
                    if response.usage:
                         # Extract usage if available
                         usage = response.usage.model_dump() if hasattr(response.usage, 'model_dump') else response.usage.dict()

                # --- (Add result extraction for other operations here) ---

                logger.info(f"{node_name} - Operation successful. Finish reason: {finish_reason}. Result text starts with: '{str(result_text)[:50]}...'")

                return {
                    "status": "success",
                    "message": f"OpenAI operation '{operation}' completed successfully.",
                    "result": {
                        "result_text": result_text,
                        "finish_reason": finish_reason,
                        "usage": usage,
                        "full_response": full_response_dict # Include the full response object
                    }
                }
            else:
                 # Should not happen if operations are handled correctly
                 raise NodeExecutionError("API call executed but no response object was processed.")


        # 5. Handle Errors (Validation, API, Connection, etc.)
        except NodeValidationError as e:
             logger.error(f"Validation Error in {node_name}: {e}")
             return self.handle_error(e, context=f"{node_name} Validation")
        except BadRequestError as e: # Specific OpenAI error for bad input (400)
             logger.error(f"OpenAI BadRequestError in {node_name}: {e.status_code} - {e.response.text}", exc_info=True)
             return self.handle_error(e, context=f"{node_name} OpenAI API Request")
        except APIConnectionError as e:
             logger.error(f"OpenAI API Connection Error in {node_name}: {e}", exc_info=True)
             return self.handle_error(e, context=f"{node_name} OpenAI Connection")
        except RateLimitError as e:
             logger.error(f"OpenAI Rate Limit Error in {node_name}: {e}", exc_info=True)
             return self.handle_error(e, context=f"{node_name} OpenAI Rate Limit")
        except APIStatusError as e: # Other non-2xx status codes
             logger.error(f"OpenAI API Status Error in {node_name}: {e.status_code} - {e.response.text}", exc_info=True)
             return self.handle_error(e, context=f"{node_name} OpenAI API Status")
        except OpenAIError as e: # Catch other general OpenAI SDK errors
             logger.error(f"OpenAI SDK Error in {node_name}: {e}", exc_info=True)
             return self.handle_error(e, context=f"{node_name} OpenAI SDK")
        except NodeExecutionError as e: # Catch errors raised internally
             logger.error(f"Execution Error in {node_name}: {e}")
             return self.handle_error(e, context=f"{node_name} Execution")
        except Exception as e:
            # Catch any other unexpected errors
            logger.error(f"Unexpected Error in {node_name} execute method: {e}", exc_info=True)
            return self.handle_error(e, context=f"{node_name} Unexpected")


# --- Main Block for Standalone Testing ---
if __name__ == "__main__":
    import asyncio

    # Configure logging for direct script execution testing
    logging.basicConfig(
        level=logging.DEBUG, # Set to DEBUG to see detailed node logs
        format='%(asctime)s - %(name)s [%(levelname)s] - %(message)s'
    )

    async def run_test():
        print("\n--- Testing OpenAINode Standalone ---")

        # --- IMPORTANT: Set API Key for testing ---
        # Best practice: Use environment variable
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            print("\n🛑 ERROR: OPENAI_API_KEY environment variable not set.")
            print("   Please set it to run the standalone test.")
            print("   export OPENAI_API_KEY='your-key-here'")
            return

        openai_node = OpenAINode()

        # --- Test Case 1: Simple Prompt ---
        print("\n--- Test Case 1: Simple Prompt ---")
        test_data_1 = {
            "params": {
                "api_key": api_key,
                "operation": "chat_completion",
                "model": "gpt-3.5-turbo", # Use a cheaper/faster model for testing
                "prompt": "Tell me a short, one-sentence joke about computers.",
                "temperature": 0.7,
                "max_tokens": 50
            },
            "__node_name": "TestSimplePrompt"
        }
        result_1 = await openai_node.execute(test_data_1)
        print(f"Result 1: {json.dumps(result_1, indent=2)}")
        assert result_1["status"] == "success"
        assert "result_text" in result_1["result"] and result_1["result"]["result_text"]

        # --- Test Case 2: Using Messages ---
        print("\n--- Test Case 2: Using Messages ---")
        test_data_2 = {
            "params": {
                "api_key": api_key,
                "operation": "chat_completion",
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant that translates English to French."},
                    {"role": "user", "content": "Hello, how are you?"}
                ],
                "temperature": 0.5,
                "max_tokens": 60
            },
            "__node_name": "TestMessages"
        }
        result_2 = await openai_node.execute(test_data_2)
        print(f"Result 2: {json.dumps(result_2, indent=2)}")
        assert result_2["status"] == "success"
        assert "result_text" in result_2["result"] and result_2["result"]["result_text"]
        # Check if the response seems like French (basic check)
        assert any(c in result_2["result"]["result_text"].lower() for c in ['bonjour', 'ça va', 'comment allez'])


        # --- Test Case 3: Missing Input (should fail validation) ---
        print("\n--- Test Case 3: Missing Input ---")
        test_data_3 = {
            "params": {
                "api_key": api_key,
                "operation": "chat_completion",
                "model": "gpt-3.5-turbo",
                # Missing 'messages' and 'prompt'
            },
            "__node_name": "TestMissingInput"
        }
        result_3 = await openai_node.execute(test_data_3)
        print(f"Result 3: {json.dumps(result_3, indent=2)}")
        assert result_3["status"] == "error"
        assert "Missing required input" in result_3["message"]

        # --- Test Case 4: Invalid API Key (should fail API call) ---
        print("\n--- Test Case 4: Invalid API Key ---")
        test_data_4 = {
            "params": {
                "api_key": "invalid-fake-key", # Intentionally wrong key
                "operation": "chat_completion",
                "model": "gpt-3.5-turbo",
                "prompt": "This should fail."
            },
            "__node_name": "TestInvalidKey"
        }
        result_4 = await openai_node.execute(test_data_4)
        print(f"Result 4: {json.dumps(result_4, indent=2)}")
        assert result_4["status"] == "error"
        # Error message might vary slightly depending on OpenAI API changes
        assert "Incorrect API key" in result_4["message"] or "authentication" in result_4["message"].lower()


    # Run the async test function
    if OPENAI_SDK_AVAILABLE:
        asyncio.run(run_test())
    else:
        print("\nSkipping standalone tests because OpenAI SDK is not available.")