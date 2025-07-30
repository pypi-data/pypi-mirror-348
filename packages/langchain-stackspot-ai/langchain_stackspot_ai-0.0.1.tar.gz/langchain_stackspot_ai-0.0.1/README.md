# LangChain StackSpot AI

[![PyPI version](https://badge.fury.io/py/langchain-stackspot-ai.svg)](https://badge.fury.io/py/langchain-stackspot-ai)
[![Python Version](https://img.shields.io/pypi/pyversions/langchain-stackspot-ai)](https://pypi.org/project/langchain-stackspot-ai/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation Status](https://readthedocs.org/projects/langchain-stackspot-ai/badge/?version=latest)](https://langchain-stackspot-ai.readthedocs.io/en/latest/?badge=latest)

A Python library for seamless integration between StackSpot AI and LangChain, enabling developers to leverage StackSpot AI's capabilities within the LangChain ecosystem.

## Features

- Easy-to-use StackSpot AI chat model implementation for LangChain
- Function calling support with StackSpot AI
- Agent executors that work with StackSpot AI
- Adapters for converting between LangChain and StackSpot AI formats
- Comprehensive documentation and examples

## Installation

### From PyPI

```bash
pip install langchain-stackspot-ai
```

### Using Poetry

```bash
poetry add langchain-stackspot-ai
```

## Quick Start

```python
from langchain_stackspot_ai.models import ChatStackSpotAI
from langchain_core.messages import HumanMessage, SystemMessage

# Initialize the StackSpot AI chat model
chat = ChatStackSpotAI(
    client_id="your-client-id",
    client_secret="your-client-secret",
    slug="your-slug"
)

# Use the model
messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="What is LangChain?")
]

response = chat.invoke(messages)
print(response.content)
```

### Using with Tools and Agents

```python
from langchain_stackspot_ai.models import ChatStackSpotAI
from langchain_stackspot_ai.agents import create_stackspot_agent_executor
from langchain_core.tools import Tool

# Define tools
tools = [
    Tool(
        name="search",
        func=lambda query: f"Search results for: {query}",
        description="Search the web for information."
    )
]

# Initialize the StackSpot AI chat model
chat = ChatStackSpotAI(
    client_id="your-client-id",
    client_secret="your-client-secret",
    slug="your-slug"
)

# Create an agent executor
agent_executor = create_stackspot_agent_executor(
    llm=chat,
    tools=tools,
    system_message="You are a helpful assistant with access to tools."
)

# Use the agent
result = agent_executor.invoke({"input": "What's the weather in New York?"})
print(result["output"])
```

## Documentation

For detailed documentation, visit [https://langchain-stackspot-ai.readthedocs.io](https://langchain-stackspot-ai.readthedocs.io).

## Development

This project uses Poetry for dependency management and packaging.

### Setting up the development environment

```bash
# Clone the repository
git clone https://github.com/stackspot/langchain-stackspot-ai.git
cd langchain-stackspot-ai

# Install dependencies
poetry install

# Activate the virtual environment
poetry shell
```

### Running tests

```bash
pytest
```

### Code quality

```bash
# Format code
black langchain_stackspot_ai tests

# Sort imports
isort langchain_stackspot_ai tests

# Type checking
mypy langchain_stackspot_ai

# Linting
flake8 langchain_stackspot_ai tests
```

### Building documentation

```bash
cd docs
make html
```

## Publishing to PyPI

### Test PyPI

```bash
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry publish --build --repository testpypi
```

### Production PyPI

```bash
poetry publish --build
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
