# AutoAI-AgentRAG

AutoAI-AgentRAG is an open-source PyPI library designed to enhance automation workflows by integrating AI Agents, Retrieval-Augmented Generation (RAG), and Machine Learning (ML). It empowers developers to build intelligent automation systems that efficiently manage complex tasks with minimal manual intervention.

[![PyPI version](https://img.shields.io/pypi/v/autoai-agentrag.svg)](https://pypi.org/project/autoai-agentrag/)
[![Python Version](https://img.shields.io/pypi/pyversions/autoai-agentrag.svg)](https://pypi.org/project/autoai-agentrag/)
[![Documentation Status](https://readthedocs.org/projects/autoai-agentrag/badge/?version=latest)](https://autoai-agentrag.readthedocs.io/en/latest/?badge=latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- **AI Agent Framework**: A modular system for designing and managing AI Agents that autonomously execute tasks and make context-informed decisions.
- **Retrieval-Augmented Generation (RAG) Integration**: Connects to external knowledge bases (APIs, databases, web sources) for real-time data retrieval, enhancing contextual awareness.
- **Machine Learning Models**: Offers pre-trained and customizable ML models compatible with TensorFlow, PyTorch, and other frameworks for predictive analytics and pattern recognition.
- **Command-Line Interface (CLI)**: A user-friendly CLI for initializing projects, training models, and deploying agents, facilitating ease of use for developers.
- **Extensible Plugin System**: Enables users to add custom data sources, ML models, or agent behaviors to adapt the library to specific use cases.
- **Comprehensive Documentation**: Detailed guides, API references, and tutorials hosted on ReadTheDocs to accelerate user onboarding and development.
- **Unit Testing and CI/CD**: Built-in unit tests and GitHub Actions for continuous integration and deployment, ensuring code reliability and maintainability.
- **Cross-Platform Compatibility**: Optimized for Windows, macOS, and Linux, with Docker support for flexible deployment across environments.
- **Real-Time Monitoring Dashboard**: An optional web interface to track agent performance, task progress, and ML model metrics for better visibility and control.
- **Community Support**: A Discord server and GitHub Issues page for collaboration, troubleshooting, and feature requests to foster an active user community.

## Installation

```bash
pip install autoai-agentrag
```

## Quick Start

```python
from autoai_agentrag import Agent, RAGConnector, MLModel

# Initialize an AI agent
agent = Agent("my_agent")

# Connect to knowledge sources
rag = RAGConnector()
rag.add_source("web", url="https://example.com/api")
rag.add_source("database", connection_string="sqlite:///my_data.db")

# Attach RAG to the agent
agent.add_rag(rag)

# Add ML capabilities
model = MLModel.from_pretrained("text-classification")
agent.add_model(model)

# Define agent behavior
@agent.task
def analyze_data(input_text):
    # Retrieve relevant information
    context = agent.rag.query(input_text)
    
    # Process with ML model
    result = agent.model.predict(input_text, context=context)
    
    return result

# Run the agent
response = agent.run("Analyze the latest market trends")
print(response)
```

## Command Line Interface

```bash
# Initialize a new project
autoai init my_project

# Create a new agent
autoai create agent my_agent

# Add RAG capabilities
autoai add rag --source web --url https://example.com/api

# Train or use a model
autoai add model --type text-classification

# Run your agent
autoai run my_agent --input "Analyze the latest market trends"

# Start monitoring dashboard
autoai dashboard
```

## Documentation

For detailed documentation, visit [https://autoai-agentrag.readthedocs.io](https://autoai-agentrag.readthedocs.io)

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 