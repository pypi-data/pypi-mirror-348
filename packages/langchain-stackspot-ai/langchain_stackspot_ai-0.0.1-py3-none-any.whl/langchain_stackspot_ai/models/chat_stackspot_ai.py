"""ChatStackSpotAI model implementation for LangChain."""

from typing import List, Optional, Dict, Any, Union
import requests
import time
import logging
import json
import re

from pydantic import Field
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, SystemMessage, HumanMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.tools import BaseTool
from langchain_core.callbacks.manager import CallbackManagerForLLMRun

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("langchain_stackspot_ai")

class ChatStackSpotAI(BaseChatModel):
    """LangChain chat model implementation for StackSpot AI.
    
    This class implements the LangChain BaseChatModel interface for StackSpot AI,
    allowing it to be used as a language model in LangChain applications.
    
    Attributes:
        client_id: StackSpot AI client ID for authentication
        client_secret: StackSpot AI client secret for authentication
        slug: StackSpot AI slug identifier
        realm: StackSpot AI realm (default: "stackspot-freemium")
        base_url: StackSpot AI API base URL
        auth_url: StackSpot AI authentication URL
        polling_interval: Interval between polling requests in seconds
        timeout: Maximum time to wait for a response in seconds
        token: Authentication token (will be obtained automatically)
        tools: List of LangChain tools that can be used with the model
    """
    
    client_id: str = Field(..., description="StackSpot AI client ID for authentication")
    client_secret: str = Field(..., description="StackSpot AI client secret for authentication")
    slug: str = Field(..., description="StackSpot AI slug identifier")
    realm: str = Field(default="stackspot-freemium", description="StackSpot AI realm")
    base_url: str = Field(
        default="https://genai-code-buddy-api.stackspot.com/v1/quick-commands",
        description="StackSpot AI API base URL"
    )
    auth_url: str = Field(
        default="https://idm.stackspot.com",
        description="StackSpot AI authentication URL"
    )
    polling_interval: float = Field(
        default=1.0,
        description="Interval between polling requests in seconds"
    )
    timeout: float = Field(
        default=60.0,
        description="Maximum time to wait for a response in seconds"
    )
    token: Optional[str] = Field(
        default=None,
        exclude=True,
        description="Authentication token (will be obtained automatically)"
    )
    tools: List[BaseTool] = Field(
        default_factory=list,
        description="List of LangChain tools that can be used with the model"
    )

    def _get_token(self) -> str:
        """Get authentication token from StackSpot API."""
        # Safely access auth_url attribute
        if hasattr(self, "auth_url") and isinstance(self.auth_url, str):
            auth_url = self.auth_url
        else:
            # Default auth_url if not properly set
            auth_url = "https://idm.stackspot.com"
            
        # Safely access realm attribute
        if hasattr(self, "realm") and isinstance(self.realm, str):
            realm = self.realm
        else:
            # Default realm if not properly set
            realm = "stackspot-freemium"
            
        url = f"{auth_url}/{realm}/oidc/oauth/token"
        
        # Safely access client_id and client_secret
        if not hasattr(self, "client_id") or not isinstance(self.client_id, str):
            raise ValueError("client_id must be a string")
            
        if not hasattr(self, "client_secret") or not isinstance(self.client_secret, str):
            raise ValueError("client_secret must be a string")
            
        data = {
            "client_id": self.client_id,
            "grant_type": "client_credentials",
            "client_secret": self.client_secret,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        
        # Debug logs
        logger.debug(f"[DEBUG] Auth URL: {url}")
        logger.debug(f"[DEBUG] Client ID: {self.client_id}")
        logger.debug(f"[DEBUG] Headers: {headers}")
        logger.debug(f"[DEBUG] Data: {data}")
        
        logger.info(f"Requesting access token from {url}")
        try:
            response = requests.post(url, data=data, headers=headers)
            
            # Debug logs for response
            logger.debug(f"[DEBUG] Response status code: {response.status_code}")
            logger.debug(f"[DEBUG] Response headers: {response.headers}")
            logger.debug(f"[DEBUG] Response content: {response.text}")
            
            response.raise_for_status()
            token = response.json()["access_token"]
            logger.info("Access token obtained successfully")
            return token
        except Exception as e:
            logger.error(f"Error obtaining access token: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response status code: {e.response.status_code}")
                logger.error(f"Response content: {e.response.text}")
            raise

    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests including authentication."""
        # Safely access token attribute
        token = None
        if hasattr(self, "token") and isinstance(self.token, str):
            token = self.token
        
        # If token is not set or not a string, get a new token
        if not token:
            token = self._get_token()
            # Store the token for future use
            self.token = token
            
        logger.debug(f"[DEBUG] Using token: {token[:10]}...")
        
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    def _create_quick_command(self, prompt: str) -> str:
        """Execute a quick command in StackSpot AI.
        
        Args:
            prompt: The prompt to send to StackSpot AI
            
        Returns:
            The execution ID for polling the result
        """
        try:
            # Use the correct URL for executing a quick command
            base_url = "https://genai-code-buddy-api.stackspot.com/v1/quick-commands"
            url = f"{base_url}/create-execution/{self.slug}"
            
            # Debug logs for URL and slug
            logger.debug(f"[DEBUG] Execution URL: {url}")
            logger.debug(f"[DEBUG] Using Slug: {self.slug}")
                
            headers = self._get_headers()
            # Debug logs for headers
            logger.debug(f"[DEBUG] Headers: {headers}")
            
            # Prepare the payload according to the API documentation
            payload = {
                "input_data": prompt
            }
            
            # Debug logs for payload
            logger.debug(f"[DEBUG] Payload: {payload}")
            
            logger.info(f"Executing quick command for slug: {self.slug}")
            response = requests.post(url, json=payload, headers=headers)
            
            # Debug logs for response
            logger.debug(f"[DEBUG] Response status code: {response.status_code}")
            logger.debug(f"[DEBUG] Response headers: {response.headers}")
            logger.debug(f"[DEBUG] Response content: {response.text}")
            
            response.raise_for_status()
            
            # The response is a string with double quotes that needs to be stripped
            execution_id = response.text.strip('"')
            logger.info(f"Quick command execution started with ID: {execution_id}")
            return execution_id
        except Exception as e:
            logger.error(f"Error executing quick command: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response status code: {e.response.status_code}")
                logger.error(f"Response content: {e.response.text}")
            raise

    def _poll_quick_command(self, execution_id: str) -> Dict[str, Any]:
        """Poll for quick command execution results.
        
        Args:
            execution_id: The ID of the execution to poll
            
        Returns:
            The response data from StackSpot AI
            
        Raises:
            TimeoutError: If the polling exceeds the timeout duration
        """
        # Use the correct URL for polling execution results
        base_url = "https://genai-code-buddy-api.stackspot.com/v1/quick-commands"
        url = f"{base_url}/callback/{execution_id}"
        
        # Debug logs for URL
        logger.debug(f"[DEBUG] Poll URL: {url}")
        logger.debug(f"[DEBUG] Execution ID: {execution_id}")
            
        headers = self._get_headers()
        
        # Debug logs for headers
        logger.debug(f"[DEBUG] Poll headers: {headers}")
        
        start_time = time.time()
        
        # Safely access timeout attribute
        if hasattr(self, "timeout") and isinstance(self.timeout, (int, float)):
            timeout = self.timeout
        else:
            # Default timeout if timeout is not properly set
            timeout = 60.0
            
        # Safely access polling_interval attribute
        if hasattr(self, "polling_interval") and isinstance(self.polling_interval, (int, float)):
            polling_interval = self.polling_interval
        else:
            # Default polling_interval if not properly set
            polling_interval = 1.0
        
        # Debug logs for timeout and polling interval
        logger.debug(f"[DEBUG] Poll timeout: {timeout}")
        logger.debug(f"[DEBUG] Poll interval: {polling_interval}")
            
        while time.time() - start_time < timeout:
            try:
                logger.debug(f"[DEBUG] Polling URL: {url}")
                response = requests.get(url, headers=headers)
                
                # Debug logs for poll response
                logger.debug(f"[DEBUG] Poll response status code: {response.status_code}")
                logger.debug(f"[DEBUG] Poll response headers: {response.headers}")
                logger.debug(f"[DEBUG] Poll response content: {response.text}")
                
                response.raise_for_status()
                data = response.json()
                
                # Check if the execution is completed
                if data["progress"]["status"] == "COMPLETED":
                    logger.info(f"Execution {execution_id} completed")
                    return data
                elif data["progress"]["status"] == "FAILED":
                    logger.error(f"Execution {execution_id} failed")
                    raise Exception(f"Execution failed: {data.get('result', 'Unknown error')}")
                
                logger.info(f"Execution {execution_id} status: {data['progress']['status']}")
                logger.debug(f"[DEBUG] Poll data: {data}")
                time.sleep(polling_interval)
            except Exception as e:
                logger.error(f"Error polling execution: {e}")
                if hasattr(e, 'response') and e.response is not None:
                    logger.error(f"Response status code: {e.response.status_code}")
                    logger.error(f"Response content: {e.response.text}")
                time.sleep(polling_interval)
                
        raise TimeoutError(f"Polling for execution {execution_id} timed out after {timeout} seconds")

    def _format_messages_to_prompt(self, messages: List[BaseMessage]) -> str:
        """Format LangChain messages to a prompt string for StackSpot AI.
        
        Args:
            messages: List of LangChain messages
            
        Returns:
            Formatted prompt string
        """
        formatted_parts = []
        
        for msg in messages:
            if isinstance(msg, SystemMessage):
                formatted_parts.append(f"System: {msg.content}")
            elif isinstance(msg, HumanMessage):
                formatted_parts.append(f"User: {msg.content}")
            elif isinstance(msg, AIMessage):
                formatted_parts.append(f"Assistant: {msg.content}")
            else:
                formatted_parts.append(f"{msg.type}: {msg.content}")
        
        return "\n\n".join(formatted_parts)

    def _format_tool_descriptions(self) -> str:
        """Format tool descriptions for StackSpot AI.
        
        Returns:
            Formatted string with tool descriptions
        """
        # Safely access tools attribute
        try:
            # Check if tools is a proper list and not empty
            if not hasattr(self, "tools") or not isinstance(self.tools, list):
                return ""
                
            if not self.tools:
                return ""
                
            tool_descriptions = []
            for tool in self.tools:
                description = f"- {tool.name}: {tool.description}"
                if hasattr(tool, 'args_schema') and tool.args_schema:
                    # Add information about tool parameters
                    schema_props = tool.args_schema.model_json_schema().get("properties", {})
                    if schema_props:
                        description += "\n  Parameters:"
                        for param_name, param_info in schema_props.items():
                            param_desc = param_info.get("description", "")
                            required = param_name in tool.args_schema.model_json_schema().get("required", [])
                            description += f"\n  - {param_name}: {param_desc}" + (" (required)" if required else "")
                tool_descriptions.append(description)
                
            return "\n\n".join(tool_descriptions)
        except (TypeError, AttributeError):
            # Handle any errors when accessing or iterating over tools
            return ""

    def _parse_tool_calls(self, response: str) -> List[Dict[str, Any]]:
        """Parse tool calls from StackSpot AI response.
        
        Args:
            response: StackSpot AI response text
            
        Returns:
            List of dictionaries with tool call information
        """
        # Pattern to identify tool calls in format:
        # Use tool: tool_name({"param1": "value1", "param2": "value2"})
        tool_call_pattern = r'(?:Use|Usar) (?:tool|ferramenta):\s*(\w+)\s*\(\s*({.*?})\s*\)'

        tool_calls = []
        matches = re.finditer(tool_call_pattern, response, re.DOTALL | re.IGNORECASE)

        for match in matches:
            tool_name = match.group(1)
            args_str = match.group(2)

            try:
                args = json.loads(args_str)
                tool_calls.append({
                    "name": tool_name,
                    "arguments": args
                })
            except json.JSONDecodeError:
                logger.warning(f"Could not parse tool arguments: {args_str}")
                # Try to fix common JSON formatting issues
                try:
                    fixed_args_str = args_str.replace("'", '"')
                    args = json.loads(fixed_args_str)
                    tool_calls.append({
                        "name": tool_name,
                        "arguments": args
                    })
                    logger.info(f"Fixed JSON parsing for tool {tool_name}")
                except json.JSONDecodeError:
                    logger.error(f"Failed to parse arguments for tool {tool_name} even after fixing")

        return tool_calls

    def _execute_tool_call(self, tool_call: Dict[str, Any]) -> str:
        """Execute a tool call.
        
        Args:
            tool_call: Dictionary with tool call information
            
        Returns:
            Result of the tool execution
        """
        tool_name = tool_call["name"]
        arguments = tool_call["arguments"]

        # Look for the tool by name
        for tool in self.tools:
            if tool.name == tool_name:
                try:
                    logger.info(f"Executing tool {tool_name} with arguments {arguments}")
                    result = tool.invoke(arguments)
                    logger.info(f"Tool {tool_name} execution successful")
                    return result
                except Exception as e:
                    error_msg = f"Error executing tool {tool_name}: {e}"
                    logger.error(error_msg)
                    return error_msg

        logger.error(f"Tool '{tool_name}' not found")
        return f"Tool '{tool_name}' not found."

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Generate a chat response.
        
        Args:
            messages: List of LangChain messages
            stop: List of stop sequences (not used by StackSpot AI)
            run_manager: Callback manager for the run
            **kwargs: Additional keyword arguments
            
        Returns:
            ChatResult with the generated response
        """
        # Format messages to prompt
        prompt = self._format_messages_to_prompt(messages)
        
        # Add tool descriptions if tools are available
        if self.tools:
            tool_descriptions = self._format_tool_descriptions()
            tool_instructions = f"""
You have access to the following tools:

{tool_descriptions}

To use a tool, respond with:
Use tool: tool_name({{"param1": "value1", "param2": "value2"}})

Only use tools when necessary and only when the user requests information that requires using a tool.
After receiving the tool result, continue the conversation normally.
"""
            # Add tool instructions before the last message (usually the user message)
            message_parts = prompt.split("\n\n")
            if len(message_parts) > 1:
                prompt = "\n\n".join(message_parts[:-1]) + "\n\n" + tool_instructions + "\n\n" + message_parts[-1]
            else:
                prompt += "\n\n" + tool_instructions
        
        # Execute quick command and get execution ID
        execution_id = self._create_quick_command(prompt)
        result = self._poll_quick_command(execution_id)
        
        # Extract response text from the correct fields according to the API documentation
        response_text = ""
        if "steps" in result and result["steps"] and len(result["steps"]) > 0:
            for step in result["steps"]:
                if step["type"] == "LLM" and "step_result" in step and "answer" in step["step_result"]:
                    response_text = step["step_result"]["answer"]
                    break
        
        # Fallback if no answer found in steps
        if not response_text and "result" in result and result["result"]:
            response_text = result["result"]
        
        if not response_text:
            response_text = "No valid response received from StackSpot AI."
        
        # Check for tool calls in the response
        tool_calls = self._parse_tool_calls(response_text)
        
        # If there are tool calls, execute them and append results
        if tool_calls and kwargs.get("execute_tools", True):
            for tool_call in tool_calls:
                tool_result = self._execute_tool_call(tool_call)
                tool_name = tool_call["name"]
                response_text += f"\n\nTool {tool_name} result:\n{tool_result}"
        
        # Create a ChatGeneration object
        generation = ChatGeneration(
            message=AIMessage(content=response_text),
            generation_info={"execution_id": execution_id}
        )
        
        return ChatResult(generations=[generation])

    @property
    def _llm_type(self) -> str:
        """Return the type of LLM."""
        return "stackspot-ai"
