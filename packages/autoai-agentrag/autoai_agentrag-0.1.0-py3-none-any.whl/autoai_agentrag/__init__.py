"""
AutoAI-AgentRAG: An open-source library integrating AI Agents, RAG, and ML for intelligent automation
"""

__version__ = "0.1.0"

from autoai_agentrag.agent import Agent
from autoai_agentrag.rag import RAGConnector
from autoai_agentrag.ml import MLModel
from autoai_agentrag.plugins import PluginManager

__all__ = ["Agent", "RAGConnector", "MLModel", "PluginManager"] 