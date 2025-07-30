"""Agent executor implementation for StackSpot AI.

This module provides an implementation of the AgentExecutor for LangChain
that uses StackSpot AI as the language model.
"""

from typing import List, Dict, Any, Optional, Union, Callable
import logging

from langchain_core.tools import BaseTool
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage, SystemMessage, FunctionMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain.agents import AgentExecutor
from langchain.memory import ConversationBufferMemory

from langchain_stackspot_ai.models import ChatStackSpotAI
from langchain_stackspot_ai.adapters import StackSpotFunctionCallAdapter, StackSpotFunctionsAgentOutputParser

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("langchain_stackspot_ai.agent_executor")

def create_stackspot_agent_executor(
    llm: ChatStackSpotAI,
    tools: List[BaseTool],
    system_message: str,
    memory: Optional[ConversationBufferMemory] = None,
    verbose: bool = False
) -> AgentExecutor:
    """
    Create an AgentExecutor that uses StackSpot AI as the language model.

    Args:
        llm: StackSpot AI language model
        tools: List of LangChain tools
        system_message: System message for the agent
        memory: Conversation memory (optional)
        verbose: Whether to display detailed logs

    Returns:
        Configured AgentExecutor for StackSpot AI
    """
    # Create the adapter for StackSpot AI
    stackspot_adapter = StackSpotFunctionCallAdapter(llm, tools)

    # Create the output parser for StackSpot AI
    output_parser = StackSpotFunctionsAgentOutputParser()

    # Create the prompt for the agent
    prompt_messages = []
    prompt_messages.append(("system", system_message))

    # Add placeholder for conversation history if memory is provided
    if memory:
        prompt_messages.append(MessagesPlaceholder(variable_name="chat_history"))

    # Add placeholder for user input
    prompt_messages.append(("user", "{input}"))

    # Add placeholder for agent scratchpad (intermediate results)
    prompt_messages.append(MessagesPlaceholder(variable_name="agent_scratchpad"))

    # Create the prompt
    prompt = ChatPromptTemplate.from_messages(prompt_messages)

    # Create the agent chain
    def _format_intermediate_steps(intermediate_steps):
        """Format intermediate steps for the agent scratchpad."""
        messages = []
        for action, observation in intermediate_steps:
            messages.append(AIMessage(content=action.log))
            
            # Handle structured results (dict/list) appropriately
            if isinstance(observation, (dict, list)):
                import json
                # Serialize to JSON string for compatibility with FunctionMessage
                obs_str = json.dumps(observation, ensure_ascii=False, indent=2)
                messages.append(FunctionMessage(name=action.tool, content=obs_str))
            else:
                messages.append(FunctionMessage(name=action.tool, content=str(observation)))
        return messages

    # Create the RunnablePassthrough to pass intermediate steps
    agent_chain = (
        RunnablePassthrough.assign(
            agent_scratchpad=lambda x: _format_intermediate_steps(x["intermediate_steps"])
        )
        | prompt
        | stackspot_adapter
        | output_parser
    )

    # Create the AgentExecutor
    agent_executor = AgentExecutor(
        agent=agent_chain,
        tools=tools,
        memory=memory,
        verbose=verbose,
        handle_parsing_errors=True,
        return_intermediate_steps=True  # Return intermediate steps
    )

    return agent_executor
