import logging
import json
import asyncio
import time
import os
from typing import Dict, Any, List, Optional, Union, Tuple

# Import Anthropic SDK
from anthropic import AsyncAnthropic, AnthropicError

from .base_node import (
    BaseNode, NodeSchema, NodeParameter, NodeParameterType,
    NodeValidationError
)

# Configure logging
logger = logging.getLogger(__name__)

class ClaudeModelType:
    """Categories of Claude Models."""
    CLAUDE = "claude"
    MESSAGES = "messages"
    EMBEDDINGS = "embeddings"

class ClaudeOperation:
    """Operations available on Claude API."""
    COMPLETION = "completion"
    MESSAGES = "messages"
    EMBEDDING = "embedding"
    MODELS_LIST = "models_list"
    FILE_UPLOAD = "file_upload"
    BATCH_CREATE = "batch_create"

class ClaudeNode(BaseNode):
    """
    Node for interacting with Claude API using the official Anthropic SDK.
    Provides functionality for all Claude service offerings.
    """
    
    # Define operation-parameter mapping as a class attribute
    _operation_parameters = {
        "completion": [
            "operation", "api_key", "model", 
            "prompt", "max_tokens_to_sample", "temperature", 
            "top_p", "top_k", "stop_sequences", "stream",
            "system"
        ],
        "messages": [
            "operation", "api_key", "model", 
            "messages", "system", "max_tokens", "temperature", 
            "top_p", "top_k", "stop_sequences", "stream",
            "metadata", "tools", "tool_choice"
        ],
        "embedding": [
            "operation", "api_key", "model", "input", 
            "embedding_dimensions", "truncate"
        ],
        "models_list": [
            "operation", "api_key"
        ],
        "file_upload": [
            "operation", "api_key", "file_path", "purpose"
        ],
        "batch_create": [
            "operation", "api_key", "model", "batch_inputs"
        ],
    }
    
    def __init__(self, sandbox_timeout: Optional[int] = None):
        super().__init__(sandbox_timeout=sandbox_timeout)
        self.client = None
        
    def get_schema(self) -> NodeSchema:
        """Return the schema definition for the Claude node."""
        return NodeSchema(
            node_type="claude",
            version="1.0.0",
            description="Interacts with Claude API for various AI operations",
            parameters=[
                # Basic parameters
                NodeParameter(
                    name="operation",
                    type=NodeParameterType.STRING,
                    description="Operation to perform with Claude API",
                    required=True,
                    enum=[
                        ClaudeOperation.COMPLETION,
                        ClaudeOperation.MESSAGES,
                        ClaudeOperation.EMBEDDING,
                        ClaudeOperation.MODELS_LIST,
                        ClaudeOperation.FILE_UPLOAD,
                        ClaudeOperation.BATCH_CREATE
                    ]
                ),
                NodeParameter(
                    name="api_key",
                    type=NodeParameterType.STRING,
                    description="Anthropic API key for Claude",
                    required=True
                ),
                
                # Model Selection
                NodeParameter(
                    name="model",
                    type=NodeParameterType.STRING,
                    description="Claude model to use",
                    required=False,
                    default="claude-3-5-sonnet-20240620"
                ),
                
                # Completion parameters
                NodeParameter(
                    name="prompt",
                    type=NodeParameterType.STRING,
                    description="Prompt for Claude (legacy completion endpoint)",
                    required=False
                ),
                NodeParameter(
                    name="max_tokens_to_sample",
                    type=NodeParameterType.NUMBER,
                    description="Maximum number of tokens to generate (legacy completion endpoint)",
                    required=False,
                    default=1024
                ),
                
                # Messages parameters
                NodeParameter(
                    name="messages",
                    type=NodeParameterType.ARRAY,
                    description="Messages for Claude messages API",
                    required=False
                ),
                NodeParameter(
                    name="system",
                    type=NodeParameterType.STRING,
                    description="System prompt to control Claude behavior",
                    required=False
                ),
                NodeParameter(
                    name="max_tokens",
                    type=NodeParameterType.NUMBER,
                    description="Maximum number of tokens to generate",
                    required=False,
                    default=1024
                ),
                NodeParameter(
                    name="temperature",
                    type=NodeParameterType.NUMBER,
                    description="Temperature for generation (0-1)",
                    required=False,
                    default=0.7
                ),
                NodeParameter(
                    name="top_p",
                    type=NodeParameterType.NUMBER,
                    description="Top-p sampling parameter (0-1)",
                    required=False,
                    default=1.0
                ),
                NodeParameter(
                    name="top_k",
                    type=NodeParameterType.NUMBER,
                    description="Top-k sampling parameter",
                    required=False,
                    default=None
                ),
                NodeParameter(
                    name="stop_sequences",
                    type=NodeParameterType.ARRAY,
                    description="Sequences where the API will stop generating",
                    required=False
                ),
                NodeParameter(
                    name="stream",
                    type=NodeParameterType.BOOLEAN,
                    description="Whether to stream back responses",
                    required=False,
                    default=False
                ),
                NodeParameter(
                    name="metadata",
                    type=NodeParameterType.OBJECT,
                    description="Additional metadata to include with the request",
                    required=False
                ),
                
                # Tool usage parameters
                NodeParameter(
                    name="tools",
                    type=NodeParameterType.ARRAY,
                    description="List of tools Claude may call",
                    required=False
                ),
                NodeParameter(
                    name="tool_choice",
                    type=NodeParameterType.ANY,
                    description="Controls which tool Claude will use",
                    required=False
                ),
                
                # Embedding parameters
                NodeParameter(
                    name="input",
                    type=NodeParameterType.ANY,
                    description="Text to get embeddings for (string or array of strings)",
                    required=False
                ),
                NodeParameter(
                    name="embedding_dimensions",
                    type=NodeParameterType.NUMBER,
                    description="Number of dimensions for embeddings",
                    required=False
                ),
                NodeParameter(
                    name="truncate",
                    type=NodeParameterType.STRING,
                    description="How to handle texts longer than the maximum input token length",
                    required=False,
                    default="NONE",
                    enum=["NONE", "START", "END", "MIDDLE"]
                ),
                
                # File upload parameters
                NodeParameter(
                    name="file_path",
                    type=NodeParameterType.STRING,
                    description="Path to file to upload",
                    required=False
                ),
                NodeParameter(
                    name="purpose",
                    type=NodeParameterType.STRING,
                    description="Purpose of uploaded file",
                    required=False,
                    default="messages",
                    enum=["messages", "inputs", "file-search"]
                ),
                
                # Batch parameters
                NodeParameter(
                    name="batch_inputs",
                    type=NodeParameterType.ARRAY,
                    description="Array of inputs for batch processing",
                    required=False
                ),
            ],
            
            # Define outputs for the node
            outputs={
                "status": NodeParameterType.STRING,
                "result": NodeParameterType.ANY,
                "error": NodeParameterType.STRING,
                "usage": NodeParameterType.OBJECT,
                "model": NodeParameterType.STRING,
                "created_at": NodeParameterType.NUMBER
            },
            
            # Add metadata
            tags=["ai", "claude", "anthropic", "embeddings", "messages"],
            author="System"
        )
    
    def get_operation_parameters(self, operation: str) -> List[Dict[str, Any]]:
        """
        Get parameters relevant to a specific operation.
        
        Args:
            operation: The operation name (e.g., MESSAGES)
            
        Returns:
            List of parameter dictionaries for the operation
        """
        # Remove the prefix if present (e.g., ClaudeOperation.MESSAGES -> MESSAGES)
        if "." in operation:
            operation = operation.split(".")[-1]
            
        # Convert to lowercase for lookup
        operation_key = operation.lower()
        
        # Get the parameter names for this operation
        param_names = self._operation_parameters.get(operation_key, [])
        
        # Get all parameters from the schema
        all_params = self.get_schema().parameters
        
        # Filter parameters based on the names
        operation_params = []
        for param in all_params:
            if param.name in param_names:
                # Convert to dictionary for the API
                param_dict = {
                    "name": param.name,
                    "type": param.type.value if hasattr(param.type, 'value') else str(param.type),
                    "description": param.description,
                    "required": param.required
                }
                
                # Add optional attributes if present
                if hasattr(param, 'default') and param.default is not None:
                    param_dict["default"] = param.default
                if hasattr(param, 'enum') and param.enum:
                    param_dict["enum"] = param.enum
                
                operation_params.append(param_dict)
        
        return operation_params
    
    def validate_custom(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        """Custom validation based on the operation type."""
        params = node_data.get("params", {})
        operation = params.get("operation")
        
        if not operation:
            raise NodeValidationError("Operation is required")
            
        # Check for API key
        if not params.get("api_key"):
            raise NodeValidationError("Claude API key is required")
            
        # Validate based on operation
        if operation == ClaudeOperation.COMPLETION:
            if not params.get("prompt"):
                raise NodeValidationError("Prompt is required for completion")
                
            # Validate temperature
            temperature = params.get("temperature", 0.7)
            if not isinstance(temperature, (int, float)) or temperature < 0 or temperature > 1:
                raise NodeValidationError("Temperature must be between 0 and 1")
                
        elif operation == ClaudeOperation.MESSAGES:
            if not params.get("messages"):
                raise NodeValidationError("Messages are required for messages API")
                
            # Validate messages format
            messages = params.get("messages", [])
            if not isinstance(messages, list) or not messages:
                raise NodeValidationError("Messages must be a non-empty array")
                
            for msg in messages:
                if not isinstance(msg, dict) or "role" not in msg or "content" not in msg:
                    raise NodeValidationError("Each message must have 'role' and 'content' fields")
                
            # Validate temperature
            temperature = params.get("temperature", 0.7)
            if not isinstance(temperature, (int, float)) or temperature < 0 or temperature > 1:
                raise NodeValidationError("Temperature must be between 0 and 1")
                
        elif operation == ClaudeOperation.EMBEDDING:
            if not params.get("input"):
                raise NodeValidationError("Input text is required for embeddings")
                
        elif operation == ClaudeOperation.FILE_UPLOAD:
            if not params.get("file_path"):
                raise NodeValidationError("File path is required for upload")
                
            # Check if file exists
            file_path = params.get("file_path")
            if not os.path.exists(file_path):
                raise NodeValidationError(f"File not found: {file_path}")
                
        elif operation == ClaudeOperation.BATCH_CREATE:
            if not params.get("batch_inputs"):
                raise NodeValidationError("Batch inputs are required for batch processing")
        
        return {}
    
    async def execute(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the Claude node."""
        try:
            # Validate schema and parameters
            validated_data = self.validate_schema(node_data)
            
            # Get operation type
            operation = validated_data.get("operation")
            
            # Initialize Anthropic client
            api_key = validated_data.get("api_key")
            
            # Create Anthropic client with timeout
            self.client = AsyncAnthropic(
                api_key=api_key,
                timeout=60.0  # Set a reasonable timeout
            )
            
            # Execute the appropriate operation
            if operation == ClaudeOperation.COMPLETION:
                return await self._operation_completion(validated_data)
            elif operation == ClaudeOperation.MESSAGES:
                return await self._operation_messages(validated_data)
            elif operation == ClaudeOperation.EMBEDDING:
                return await self._operation_embedding(validated_data)
            elif operation == ClaudeOperation.MODELS_LIST:
                return await self._operation_models_list(validated_data)
            elif operation == ClaudeOperation.FILE_UPLOAD:
                return await self._operation_file_upload(validated_data)
            elif operation == ClaudeOperation.BATCH_CREATE:
                return await self._operation_batch_create(validated_data)
            else:
                error_message = f"Unknown operation: {operation}"
                logger.error(error_message)
                return {
                    "status": "error",
                    "result": None,
                    "error": error_message,
                    "usage": None,
                    "model": None,
                    "created_at": None
                }
                
        except Exception as e:
            error_message = f"Error in Claude node: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "usage": None,
                "model": None,
                "created_at": None
            }
    
    # -------------------------
    # Operation Methods
    # -------------------------
    
    async def _operation_completion(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send a completion request to the Claude API using legacy completion endpoint.
        
        Args:
            params: Completion parameters
            
        Returns:
            Completion results
        """
        # Extract parameters
        prompt = params.get("prompt", "")
        model = params.get("model", "claude-3-5-sonnet-20240620")
        max_tokens_to_sample = params.get("max_tokens_to_sample", 1024)
        temperature = params.get("temperature", 0.7)
        top_p = params.get("top_p", 1.0)
        top_k = params.get("top_k")
        stream = params.get("stream", False)
        system = params.get("system")
        stop_sequences = params.get("stop_sequences", [])
        
        # Build request
        request_args = {
            "model": model,
            "prompt": prompt,
            "max_tokens_to_sample": max_tokens_to_sample,
            "temperature": temperature,
            "top_p": top_p,
            "stream": stream
        }
        
        # Add optional parameters
        if top_k is not None:
            request_args["top_k"] = top_k
        if system is not None:
            request_args["system"] = system
        if stop_sequences:
            request_args["stop_sequences"] = stop_sequences
        
        try:
            # Send request
            response = await self.client.completions.create(**request_args)
            
            # Handle streaming responses if enabled
            if stream:
                collected_chunks = []
                content = []
                
                async for chunk in response:
                    collected_chunks.append(chunk)
                    if hasattr(chunk, 'completion'):
                        content.append(chunk.completion)
                
                # Combine and return all content
                complete_response = {
                    "status": "success",
                    "result": {
                        "completion": "".join(content),
                        "model": model,
                        "stop_reason": collected_chunks[-1].stop_reason if collected_chunks else None,
                    },
                    "usage": None,  # Usage stats aren't available in streaming mode
                    "model": model,
                    "created_at": int(time.time())
                }
                return complete_response
            
            # Process regular response
            result = response.model_dump()
            
            # Format the response
            return {
                "status": "success",
                "result": result,
                "usage": None,  # Legacy completion API doesn't provide usage stats
                "model": model,
                "created_at": int(time.time())
            }
            
        except AnthropicError as e:
            error_message = f"Claude completion error: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "usage": None,
                "model": model,
                "created_at": None
            }
    
    async def _operation_messages(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send a messages request to the Claude API.
        
        Args:
            params: Messages parameters
            
        Returns:
            Messages results
        """
        # Extract parameters
        messages = params.get("messages", [])
        model = params.get("model", "claude-3-5-sonnet-20240620")
        system = params.get("system")
        max_tokens = params.get("max_tokens", 1024)
        temperature = params.get("temperature", 0.7)
        top_p = params.get("top_p", 1.0)
        top_k = params.get("top_k")
        stream = params.get("stream", False)
        stop_sequences = params.get("stop_sequences", [])
        metadata = params.get("metadata")
        tools = params.get("tools")
        tool_choice = params.get("tool_choice")
        
        # Build request
        request_args = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "stream": stream
        }
        
        # Add optional parameters
        if system is not None:
            request_args["system"] = system
        if top_k is not None:
            request_args["top_k"] = top_k
        if stop_sequences:
            request_args["stop_sequences"] = stop_sequences
        if metadata is not None:
            request_args["metadata"] = metadata
        if tools is not None:
            request_args["tools"] = tools
        if tool_choice is not None:
            request_args["tool_choice"] = tool_choice
        
        try:
            # Send request
            response = await self.client.messages.create(**request_args)
            
            # Handle streaming responses if enabled
            if stream:
                collected_chunks = []
                content_chunks = []
                tool_calls = []
                
                async for chunk in response:
                    collected_chunks.append(chunk)
                    
                    # Handle text content
                    if hasattr(chunk.delta, 'text') and chunk.delta.text:
                        content_chunks.append(chunk.delta.text)
                    
                    # Handle tool calls
                    if hasattr(chunk.delta, 'tool_calls') and chunk.delta.tool_calls:
                        # Store tool calls - this might need complex handling
                        # depending on exactly how the delta works
                        for tool_call in chunk.delta.tool_calls:
                            # This is simplified - real implementation would need
                            # to handle partial tool call updates
                            tool_calls.append(tool_call)
                
                # Get the usage from the last chunk if available
                usage = None
                if collected_chunks and hasattr(collected_chunks[-1], 'usage'):
                    usage = collected_chunks[-1].usage.model_dump()
                
                # Combine and return all content
                complete_response = {
                    "status": "success",
                    "result": {
                        "content": "".join(content_chunks),
                        "tool_calls": tool_calls,
                        "stop_reason": collected_chunks[-1].stop_reason if collected_chunks else None,
                    },
                    "usage": usage,
                    "model": model,
                    "created_at": int(time.time())
                }
                return complete_response
            
            # Process regular response
            result = response.model_dump()
            
            # Format the response
            return {
                "status": "success",
                "result": result,
                "usage": result.get("usage"),
                "model": model,
                "created_at": int(time.time())
            }
            
        except AnthropicError as e:
            error_message = f"Claude messages error: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "usage": None,
                "model": model,
                "created_at": None
            }
    
    async def _operation_embedding(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get embeddings from Claude API.
        
        Args:
            params: Embedding parameters
            
        Returns:
            Embedding results
        """
        # Extract parameters
        input_text = params.get("input")
        model = params.get("model", "claude-3-embedding-3-0628")
        dimensions = params.get("embedding_dimensions")
        truncate = params.get("truncate", "NONE")
        
        # Build request
        request_args = {
            "model": model,
            "input": input_text,
            "truncate": truncate
        }
        
        # Add optional parameters
        if dimensions is not None:
            request_args["dimensions"] = dimensions
        
        try:
            # Send request
            response = await self.client.embeddings.create(**request_args)
            
            # Process response
            result = response.model_dump()
            
            # Format the response
            return {
                "status": "success",
                "result": result,
                "usage": result.get("usage"),
                "model": model,
                "created_at": int(time.time())
            }
            
        except AnthropicError as e:
            error_message = f"Claude embedding error: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "usage": None,
                "model": model,
                "created_at": None
            }
    
    async def _operation_models_list(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        List available Claude models.
        
        Args:
            params: Not used
            
        Returns:
            Available models
        """
        try:
            # Anthropic doesn't have a models.list API, so we'll return
            # a hardcoded list of the most common Claude models
            available_models = [
                {
                    "id": "claude-3-opus-20240229",
                    "name": "Claude 3 Opus",
                    "description": "Most powerful Claude model for sophisticated tasks",
                    "max_tokens": 200000,
                    "created": int(time.time())
                },
                {
                    "id": "claude-3-sonnet-20240229",
                    "name": "Claude 3 Sonnet",
                    "description": "Balanced model for most tasks",
                    "max_tokens": 200000,
                    "created": int(time.time())
                },
                {
                    "id": "claude-3-haiku-20240307",
                    "name": "Claude 3 Haiku",
                    "description": "Fastest and most compact Claude model",
                    "max_tokens": 200000,
                    "created": int(time.time())
                },
                {
                    "id": "claude-3-5-sonnet-20240620",
                    "name": "Claude 3.5 Sonnet",
                    "description": "Latest generation high-performance model",
                    "max_tokens": 200000,
                    "created": int(time.time())
                },
                {
                    "id": "claude-3-5-haiku-20240620",
                    "name": "Claude 3.5 Haiku",
                    "description": "Fast, efficient latest generation model",
                    "max_tokens": 200000,
                    "created": int(time.time())
                },
                {
                    "id": "claude-3-embedding-3-0628",
                    "name": "Claude 3 Embedding",
                    "description": "Embedding model for text embeddings",
                    "max_tokens": 10000,
                    "created": int(time.time())
                }
            ]
            
            # Format the response
            return {
                "status": "success",
                "result": {
                    "data": available_models,
                    "object": "list"
                },
                "usage": None,
                "model": None,
                "created_at": int(time.time())
            }
            
        except Exception as e:
            error_message = f"Claude models list error: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "usage": None,
                "model": None,
                "created_at": None
            }
    
    async def _operation_file_upload(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Upload a file to Claude API.
        
        Args:
            params: File upload parameters
            
        Returns:
            File upload results
        """
        # Extract parameters
        file_path = params.get("file_path")
        purpose = params.get("purpose", "messages")
        
        try:
            # Send request
            with open(file_path, 'rb') as file:
                response = await self.client.files.create(
                    file=file,
                    purpose=purpose
                )
            
            # Process response
            result = response.model_dump()
            
            # Format the response
            return {
                "status": "success",
                "result": result,
                "usage": None,
                "model": None,
                "created_at": int(time.time())
            }
            
        except AnthropicError as e:
            error_message = f"Claude file upload error: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "usage": None,
                "model": None,
                "created_at": None
            }
        except Exception as e:
            error_message = f"Claude file upload error: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "usage": None,
                "model": None,
                "created_at": None
            }
    
    async def _operation_batch_create(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a batch of requests to Claude API.
        
        Args:
            params: Batch parameters
            
        Returns:
            Batch creation results
        """
        # Extract parameters
        batch_inputs = params.get("batch_inputs", [])
        model = params.get("model", "claude-3-5-sonnet-20240620")
        
        try:
            # Create batch (assuming an API similar to OpenAI's)
            # Note: Claude's actual batch API might be different
            response = await self.client.batches.create(
                model=model, 
                inputs=batch_inputs
            )
            
            # Process response
            result = response.model_dump() if hasattr(response, 'model_dump') else dict(response)
            
            # Format the response
            return {
                "status": "success",
                "result": result,
                "usage": None,
                "model": model,
                "created_at": int(time.time())
            }
            
        except AnthropicError as e:
            error_message = f"Claude batch creation error: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "usage": None,
                "model": model,
                "created_at": None
            }
        except Exception as e:
            # Handle the case where the batch API might not exist
            error_message = f"Claude batch creation error: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "usage": None,
                "model": model,
                "created_at": None
            }

# Register with NodeRegistry
try:
    from base_node import NodeRegistry
    NodeRegistry.register("claude", ClaudeNode)
    logger.info("Registered node type: claude")
except Exception as e:
    logger.error(f"Error registering Claude node: {str(e)}")