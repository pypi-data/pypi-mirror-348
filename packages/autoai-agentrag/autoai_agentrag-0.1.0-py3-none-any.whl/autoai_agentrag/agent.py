"""
Agent module for creating and managing AI agents that can perform tasks autonomously.
"""

from typing import Any, Callable, Dict, List, Optional, Union
import uuid
import logging
from functools import wraps

from pydantic import BaseModel, Field

from autoai_agentrag.rag import RAGConnector
from autoai_agentrag.ml import MLModel

logger = logging.getLogger(__name__)

class TaskDefinition(BaseModel):
    """Definition of a task that can be performed by an agent."""
    name: str
    function: Callable
    description: Optional[str] = None


class Agent(BaseModel):
    """
    An AI agent that can perform tasks autonomously using RAG and ML capabilities.
    
    Attributes:
        name: The name of the agent
        description: A description of the agent's purpose
        rag: Optional RAG connector for knowledge retrieval
        models: Dictionary of ML models available to the agent
        tasks: Dictionary of tasks the agent can perform
        config: Additional configuration options
    """
    name: str
    description: Optional[str] = None
    rag: Optional[RAGConnector] = None
    models: Dict[str, MLModel] = Field(default_factory=dict)
    tasks: Dict[str, TaskDefinition] = Field(default_factory=dict)
    config: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        arbitrary_types_allowed = True
    
    def add_rag(self, rag: RAGConnector) -> None:
        """Add a RAG connector to the agent."""
        self.rag = rag
        logger.info(f"Added RAG connector to agent {self.name}")
    
    def add_model(self, model: MLModel, name: Optional[str] = None) -> None:
        """Add an ML model to the agent."""
        model_name = name or model.name or f"model_{len(self.models)}"
        self.models[model_name] = model
        logger.info(f"Added model {model_name} to agent {self.name}")
    
    def task(self, func: Callable) -> Callable:
        """
        Decorator to register a function as a task for this agent.
        
        Example:
            @agent.task
            def analyze_data(input_text):
                # Task implementation
                return result
        """
        task_name = func.__name__
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"Executing task {task_name}")
            return func(*args, **kwargs)
        
        self.tasks[task_name] = TaskDefinition(
            name=task_name,
            function=wrapper,
            description=func.__doc__
        )
        
        logger.info(f"Registered task {task_name} for agent {self.name}")
        return wrapper
    
    def run(self, input_data: Any, task_name: Optional[str] = None) -> Any:
        """
        Run the agent on the given input data.
        
        If task_name is provided, that specific task will be executed.
        Otherwise, the agent will try to determine the appropriate task.
        """
        if not self.tasks:
            raise ValueError("No tasks defined for this agent")
        
        if task_name:
            if task_name not in self.tasks:
                raise ValueError(f"Task {task_name} not found")
            
            task = self.tasks[task_name]
            logger.info(f"Running task {task_name} for agent {self.name}")
            return task.function(input_data)
        
        # If no task specified, use the first one (in future, could implement task selection)
        default_task = next(iter(self.tasks.values()))
        logger.info(f"Running default task {default_task.name} for agent {self.name}")
        return default_task.function(input_data)
    
    def get_available_tasks(self) -> List[Dict[str, str]]:
        """Get a list of available tasks with their descriptions."""
        return [
            {"name": name, "description": task.description or "No description"}
            for name, task in self.tasks.items()
        ] 