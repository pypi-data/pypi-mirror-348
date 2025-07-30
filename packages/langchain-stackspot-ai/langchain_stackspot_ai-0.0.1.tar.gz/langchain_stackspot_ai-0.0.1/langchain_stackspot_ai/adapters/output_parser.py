"""Output parser for StackSpot AI responses.

This module provides classes and functions to parse the output of StackSpot AI
and convert it to the format expected by LangChain's AgentExecutor.
"""

from typing import Union, List, Dict, Any, Optional, Type
import re
import json
import logging

from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.output_parsers.base import BaseOutputParser
from langchain_core.runnables import Runnable, RunnableConfig

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("langchain_stackspot_ai.output_parser")

class StackSpotFunctionsAgentOutputParser(BaseOutputParser, Runnable):
    """
    Output parser for StackSpot AI that identifies tool calls
    and converts them to the format expected by AgentExecutor.
    Implements the LangChain Runnable interface for compatibility with AgentExecutor.
    """

    def parse(self, text: str) -> Union[AgentAction, AgentFinish]:
        """
        Parse StackSpot AI output text and identify if it's a tool call
        or a final response.

        Args:
            text: StackSpot AI output text

        Returns:
            AgentAction if it's a tool call, AgentFinish if it's a final response
        """
        # Log the full text for debugging
        logger.info(f"Parsing text to identify tool calls: {text[:200]}..." if len(text) > 200 else text)

        # Pattern to identify tool calls in format:
        # Use tool: tool_name({"param1": "value1", "param2": "value2"})
        pattern = r'(?:Use|Usar) (?:tool|ferramenta):\s*(\w+)\s*\(\s*(\{.*?\})\s*\)'

        # Look for ALL patterns in the text (multiple tool calls)
        matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)

        if matches:
            actions = []
            for tool_name, args_str in matches:
                logger.info(f"Tool call pattern found: {tool_name}")
                try:
                    args = json.loads(args_str)
                    logger.info(f"Tool call identified: {tool_name} with arguments: {args}")
                    actions.append(AgentAction(tool=tool_name, tool_input=args, log=text))
                except json.JSONDecodeError as e:
                    logger.error(f"Error parsing arguments for tool {tool_name}: {e}")
                    try:
                        fixed_args_str = args_str.replace("'", '"')
                        args = json.loads(fixed_args_str)
                        logger.info(f"JSON fixed successfully for tool {tool_name}")
                        actions.append(AgentAction(tool=tool_name, tool_input=args, log=text))
                    except Exception as e2:
                        logger.error(f"Failed to fix JSON for tool {tool_name}: {e2}")
            if actions:
                # If there are multiple actions, return the list (or adapt for the executor)
                return actions[0] if len(actions) == 1 else actions

        # Try alternative patterns for tool calls
        # Alternative pattern that might appear in some models
        alt_pattern = r'(?:usar|use|execute|chamar|call)\s+(?:a\s+)?(?:ferramenta|tool)?\s*[\'"]?(\w+)[\'"]?\s*(?:com|with)?\s*(?:os\s+)?(?:parâmetros|parameters|args|arguments)?:?\s*(?:\{(.*?)\}|latitude\s*[=:]\s*(-?\d+\.?\d*)\s*(?:e|and|,)\s*longitude\s*[=:]\s*(-?\d+\.?\d*))'

        alt_match = re.search(alt_pattern, text.lower(), re.DOTALL | re.IGNORECASE)

        if alt_match:
            tool_name = alt_match.group(1)

            # Check if we have a JSON object or separate parameters
            if alt_match.group(2):  # We have a JSON object
                args_str = "{" + alt_match.group(2) + "}"
                try:
                    args = json.loads(args_str)

                    logger.info(f"Alternative tool call identified: {tool_name} with arguments: {args}")

                    return AgentAction(tool=tool_name, tool_input=args, log=text)
                except Exception as e:
                    logger.error(f"Error parsing alternative arguments: {e}")
            elif alt_match.group(3) and alt_match.group(4):  # We have latitude and longitude
                latitude = float(alt_match.group(3))
                longitude = float(alt_match.group(4))
                args = {"latitude": latitude, "longitude": longitude}

                logger.info(f"Alternative tool call identified: {tool_name} with lat/long: {args}")

                return AgentAction(tool=tool_name, tool_input=args, log=text)

        # If it's not a tool call, it's a final response
        logger.info("Final response identified")

        return AgentFinish(return_values={"output": text}, log=text)

    def parse_message(self, message: BaseMessage) -> Union[AgentAction, AgentFinish]:
        """
        Parse a LangChain message and identify if it's a tool call
        or a final response.

        Args:
            message: LangChain message

        Returns:
            AgentAction if it's a tool call, AgentFinish if it's a final response
        """
        if not isinstance(message, AIMessage):
            raise ValueError(f"Expected an AIMessage, got {type(message)}")

        return self.parse(message.content)

    @property
    def _type(self) -> str:
        """Return the type of the output parser."""
        return "stackspot-functions-agent-output-parser"

    def invoke(self, input_data, config: Optional[RunnableConfig] = None) -> Union[AgentAction, AgentFinish]:
        """
        Invoke the parser with an assistant message.

        Args:
            input_data: Assistant message or text
            config: Runnable configuration (optional)

        Returns:
            AgentAction if it's a tool call, AgentFinish if it's a final response
        """
        if isinstance(input_data, AIMessage):
            return self.parse_message(input_data)
        elif isinstance(input_data, str):
            return self.parse(input_data)
        else:
            raise ValueError(f"Expected an AIMessage or str, got {type(input_data)}")

    def batch(self, inputs, config: Optional[RunnableConfig] = None) -> List[Union[AgentAction, AgentFinish]]:
        """
        Process a batch of assistant messages or texts.

        Args:
            inputs: List of assistant messages or texts
            config: Runnable configuration (optional)

        Returns:
            List of AgentAction or AgentFinish
        """
        return [self.invoke(input_item, config) for input_item in inputs]

    @property
    def InputType(self) -> Type:
        """Input type for the Runnable."""
        return Union[AIMessage, str]

    @property
    def OutputType(self) -> Type:
        """Output type for the Runnable."""
        return Union[AgentAction, AgentFinish]
