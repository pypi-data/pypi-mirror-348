"""Function adapter for StackSpot AI to work with OpenAI function format."""

from typing import List, Dict, Any, Optional, Union, Callable, Type
import json
import re
import logging

from langchain_core.tools import BaseTool
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage, SystemMessage, FunctionMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.runnables import Runnable, RunnableConfig

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("langchain_stackspot_ai.function_adapter")

def convert_to_stackspot_function(tool: BaseTool) -> Dict[str, Any]:
    """
    Convert a LangChain tool to StackSpot AI function format.

    Args:
        tool: LangChain tool

    Returns:
        Dictionary with tool description in StackSpot AI format
    """
    schema = tool.args_schema.schema() if tool.args_schema else {"properties": {}}

    return {
        "name": tool.name,
        "description": tool.description,
        "parameters": schema
    }

def format_tool_descriptions(tools: List[BaseTool]) -> str:
    """
    Format tool descriptions for StackSpot AI.

    Args:
        tools: List of LangChain tools

    Returns:
        Formatted string with tool descriptions
    """
    if not tools:
        return ""

    tool_descriptions = []
    for tool in tools:
        parameters = ""
        if tool.args_schema:
            schema = tool.args_schema.schema()
            if "properties" in schema:
                params = []
                for name, prop in schema["properties"].items():
                    param_desc = prop.get("description", "")
                    params.append(f"- {name}: {param_desc}")
                if params:
                    parameters = "\nParameters:\n" + "\n".join(params)

        tool_descriptions.append(f"### {tool.name}\n{tool.description}{parameters}")

    return "\n\n".join(tool_descriptions)

def parse_tool_calls(text: str) -> List[Dict[str, Any]]:
    """
    Parse StackSpot AI response text to identify tool calls.

    Args:
        text: StackSpot AI response text

    Returns:
        List of dictionaries with identified tool calls
    """
    # Pattern to identify tool calls in format:
    # Use tool: tool_name({"param1": "value1", "param2": "value2"})
    pattern = r'(?:Use|Usar) (?:tool|ferramenta):\s*(\w+)\s*\(\s*(\{.*?\})\s*\)'

    # Find all occurrences of the pattern in the text
    matches = re.finditer(pattern, text, re.DOTALL | re.IGNORECASE)

    tool_calls = []
    for match in matches:
        tool_name = match.group(1)
        args_str = match.group(2)

        try:
            # Try to parse arguments as JSON
            args = json.loads(args_str)

            tool_calls.append({
                "name": tool_name,
                "arguments": args
            })
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing tool arguments for {tool_name}: {e}")
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

def format_to_stackspot_messages(messages: List[BaseMessage]) -> str:
    """
    Format a list of LangChain messages to StackSpot AI text format.

    Args:
        messages: List of LangChain messages

    Returns:
        Formatted string with messages
    """
    formatted_messages = []

    for msg in messages:
        if isinstance(msg, SystemMessage):
            formatted_messages.append(f"System: {msg.content}")
        elif isinstance(msg, HumanMessage):
            formatted_messages.append(f"User: {msg.content}")
        elif isinstance(msg, AIMessage):
            formatted_messages.append(f"Assistant: {msg.content}")
        elif isinstance(msg, FunctionMessage):
            formatted_messages.append(f"Tool result {msg.name}: {msg.content}")
        else:
            formatted_messages.append(f"{msg.type}: {msg.content}")

    return "\n\n".join(formatted_messages)

class StackSpotFunctionCallAdapter(Runnable):
    """
    Adapter for StackSpot AI that enables using the OpenAI function format.
    Implements the LangChain Runnable interface for compatibility with AgentExecutor.
    """

    def __init__(self, llm: BaseChatModel, tools: List[BaseTool]):
        """
        Initialize the adapter.

        Args:
            llm: StackSpot AI language model
            tools: List of LangChain tools
        """
        self.llm = llm
        self.tools = tools
        self.tool_map = {tool.name: tool for tool in tools}

    def invoke(self, input_data, config: Optional[RunnableConfig] = None, **kwargs) -> AIMessage:
        """
        Invoke the model with messages.

        Args:
            input_data: Input for the model (can be a list of messages or a ChatPromptValue)
            config: Runnable configuration (optional)

        Returns:
            Assistant message with the result
        """
        # Check if input has to_messages() method (like ChatPromptValue)
        if hasattr(input_data, 'to_messages') and callable(getattr(input_data, 'to_messages')):
            messages = input_data.to_messages()
        else:
            messages = input_data

        # Log available tools
        available_tools = [
            {
                "name": tool.name,
                "description": tool.description,
                "args_schema": tool.args_schema.__name__ if hasattr(tool, 'args_schema') and tool.args_schema else None
            }
            for tool in self.tools
        ]
        logger.info(f"Available tools in adapter: {len(self.tools)}")

        # Add information about available tools
        tool_descriptions = format_tool_descriptions(self.tools)

        # Build prompt with messages and tool descriptions
        if tool_descriptions:
            # Add tool instructions before the last message
            system_message = None
            for i, msg in enumerate(messages):
                if isinstance(msg, SystemMessage):
                    system_message = msg
                    break

            if system_message:
                # Update system message to include tool instructions
                updated_content = system_message.content
                if "Available tools:" not in updated_content:
                    updated_content += f"\n\nAvailable tools:\n\n{tool_descriptions}\n\n"
                    updated_content += '\nTo use a tool, respond with: Use tool: tool_name({"param1": "value1", ...})'
                    
                    # Replace the system message with updated content
                    for i, msg in enumerate(messages):
                        if isinstance(msg, SystemMessage):
                            messages[i] = SystemMessage(content=updated_content)
                            break
            else:
                # If no system message exists, add one with tool instructions
                tool_system_message = SystemMessage(content=f"You have access to the following tools:\n\n{tool_descriptions}\n\n"
                                                  f'To use a tool, respond with: Use tool: tool_name({{"param1": "value1", ...}})')
                messages = [tool_system_message] + messages

        # Call the LLM with the messages
        result = self.llm.invoke(messages)
        
        return result

    def batch(self, inputs, config: Optional[RunnableConfig] = None) -> List[AIMessage]:
        """
        Process a batch of inputs.

        Args:
            inputs: List of inputs for the model
            config: Runnable configuration (optional)

        Returns:
            List of assistant messages with results
        """
        return [self.invoke(input_item, config) for input_item in inputs]

    @property
    def InputType(self) -> Type:
        """Input type for the Runnable."""
        return Union[List[BaseMessage], Any]

    @property
    def OutputType(self) -> Type:
        """Output type for the Runnable."""
        return AIMessage
