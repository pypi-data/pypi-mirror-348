# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['langchain_stackspot_ai',
 'langchain_stackspot_ai.adapters',
 'langchain_stackspot_ai.agents',
 'langchain_stackspot_ai.models',
 'langchain_stackspot_ai.utils']

package_data = \
{'': ['*']}

install_requires = \
['langchain-core>=0.1.10,<0.2.0',
 'langchain>=0.1.0,<0.2.0',
 'pydantic>=2.5.0,<3.0.0',
 'python-dotenv>=1.1.0,<2.0.0',
 'requests>=2.31.0,<3.0.0']

setup_kwargs = {
    'name': 'langchain-stackspot-ai',
    'version': '0.0.1',
    'description': 'A library for integrating StackSpot AI with LangChain',
    'long_description': '# LangChain StackSpot AI\n\n[![PyPI version](https://badge.fury.io/py/langchain-stackspot-ai.svg)](https://badge.fury.io/py/langchain-stackspot-ai)\n[![Python Version](https://img.shields.io/pypi/pyversions/langchain-stackspot-ai)](https://pypi.org/project/langchain-stackspot-ai/)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n[![Documentation Status](https://readthedocs.org/projects/langchain-stackspot-ai/badge/?version=latest)](https://langchain-stackspot-ai.readthedocs.io/en/latest/?badge=latest)\n\nA Python library for seamless integration between StackSpot AI and LangChain, enabling developers to leverage StackSpot AI\'s capabilities within the LangChain ecosystem.\n\n## Features\n\n- Easy-to-use StackSpot AI chat model implementation for LangChain\n- Function calling support with StackSpot AI\n- Agent executors that work with StackSpot AI\n- Adapters for converting between LangChain and StackSpot AI formats\n- Comprehensive documentation and examples\n\n## Installation\n\n### From PyPI\n\n```bash\npip install langchain-stackspot-ai\n```\n\n### Using Poetry\n\n```bash\npoetry add langchain-stackspot-ai\n```\n\n## Quick Start\n\n```python\nfrom langchain_stackspot_ai.models import ChatStackSpotAI\nfrom langchain_core.messages import HumanMessage, SystemMessage\n\n# Initialize the StackSpot AI chat model\nchat = ChatStackSpotAI(\n    client_id="your-client-id",\n    client_secret="your-client-secret",\n    slug="your-slug"\n)\n\n# Use the model\nmessages = [\n    SystemMessage(content="You are a helpful assistant."),\n    HumanMessage(content="What is LangChain?")\n]\n\nresponse = chat.invoke(messages)\nprint(response.content)\n```\n\n### Using with Tools and Agents\n\n```python\nfrom langchain_stackspot_ai.models import ChatStackSpotAI\nfrom langchain_stackspot_ai.agents import create_stackspot_agent_executor\nfrom langchain_core.tools import Tool\n\n# Define tools\ntools = [\n    Tool(\n        name="search",\n        func=lambda query: f"Search results for: {query}",\n        description="Search the web for information."\n    )\n]\n\n# Initialize the StackSpot AI chat model\nchat = ChatStackSpotAI(\n    client_id="your-client-id",\n    client_secret="your-client-secret",\n    slug="your-slug"\n)\n\n# Create an agent executor\nagent_executor = create_stackspot_agent_executor(\n    llm=chat,\n    tools=tools,\n    system_message="You are a helpful assistant with access to tools."\n)\n\n# Use the agent\nresult = agent_executor.invoke({"input": "What\'s the weather in New York?"})\nprint(result["output"])\n```\n\n## Documentation\n\nFor detailed documentation, visit [https://langchain-stackspot-ai.readthedocs.io](https://langchain-stackspot-ai.readthedocs.io).\n\n## Development\n\nThis project uses Poetry for dependency management and packaging.\n\n### Setting up the development environment\n\n```bash\n# Clone the repository\ngit clone https://github.com/stackspot/langchain-stackspot-ai.git\ncd langchain-stackspot-ai\n\n# Install dependencies\npoetry install\n\n# Activate the virtual environment\npoetry shell\n```\n\n### Running tests\n\n```bash\npytest\n```\n\n### Code quality\n\n```bash\n# Format code\nblack langchain_stackspot_ai tests\n\n# Sort imports\nisort langchain_stackspot_ai tests\n\n# Type checking\nmypy langchain_stackspot_ai\n\n# Linting\nflake8 langchain_stackspot_ai tests\n```\n\n### Building documentation\n\n```bash\ncd docs\nmake html\n```\n\n## Publishing to PyPI\n\n### Test PyPI\n\n```bash\npoetry config repositories.testpypi https://test.pypi.org/legacy/\npoetry publish --build --repository testpypi\n```\n\n### Production PyPI\n\n```bash\npoetry publish --build\n```\n\n## License\n\nThis project is licensed under the MIT License - see the LICENSE file for details.\n\n## Contributing\n\nContributions are welcome! Please feel free to submit a Pull Request.\n\n1. Fork the repository\n2. Create your feature branch (`git checkout -b feature/amazing-feature`)\n3. Commit your changes (`git commit -m \'Add some amazing feature\'`)\n4. Push to the branch (`git push origin feature/amazing-feature`)\n5. Open a Pull Request\n',
    'author': 'Guilherme Chafy',
    'author_email': 'guichafy@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/stackspot/langchain-stackspot-ai',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
