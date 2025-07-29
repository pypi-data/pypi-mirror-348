"""
Unit tests for the Agent module.
"""

import unittest
from unittest.mock import MagicMock, patch

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from autoai_agentrag import Agent, RAGConnector, MLModel
from autoai_agentrag.ml import TextClassificationModel


class TestAgent(unittest.TestCase):
    """Tests for the Agent class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.agent = Agent(name="test_agent", description="Test agent")
    
    def test_initialization(self):
        """Test agent initialization."""
        self.assertEqual(self.agent.name, "test_agent")
        self.assertEqual(self.agent.description, "Test agent")
        self.assertIsNone(self.agent.rag)
        self.assertEqual(len(self.agent.models), 0)
        self.assertEqual(len(self.agent.tasks), 0)
    
    def test_add_rag(self):
        """Test adding a RAG connector."""
        rag = RAGConnector()
        self.agent.add_rag(rag)
        self.assertEqual(self.agent.rag, rag)
    
    def test_add_model(self):
        """Test adding an ML model."""
        # Create a mock model
        model = MagicMock(spec=MLModel)
        model.name = "test_model"
        
        # Add the model
        self.agent.add_model(model)
        self.assertEqual(len(self.agent.models), 1)
        self.assertIn("test_model", self.agent.models)
        self.assertEqual(self.agent.models["test_model"], model)
        
        # Add another model with a custom name
        model2 = MagicMock(spec=MLModel)
        model2.name = "model2"
        self.agent.add_model(model2, name="custom_name")
        self.assertEqual(len(self.agent.models), 2)
        self.assertIn("custom_name", self.agent.models)
        self.assertEqual(self.agent.models["custom_name"], model2)
    
    def test_task_decorator(self):
        """Test the task decorator."""
        @self.agent.task
        def test_task(input_data):
            """Test task."""
            return f"Processed: {input_data}"
        
        self.assertEqual(len(self.agent.tasks), 1)
        self.assertIn("test_task", self.agent.tasks)
        self.assertEqual(self.agent.tasks["test_task"].name, "test_task")
        self.assertEqual(self.agent.tasks["test_task"].description, "Test task.")
    
    def test_run_with_task_name(self):
        """Test running the agent with a specific task name."""
        # Define a task
        @self.agent.task
        def test_task(input_data):
            return f"Processed: {input_data}"
        
        # Run the agent with the task name
        result = self.agent.run("test_input", task_name="test_task")
        self.assertEqual(result, "Processed: test_input")
    
    def test_run_without_task_name(self):
        """Test running the agent without specifying a task name."""
        # Define a task
        @self.agent.task
        def test_task(input_data):
            return f"Processed: {input_data}"
        
        # Run the agent without specifying the task name
        result = self.agent.run("test_input")
        self.assertEqual(result, "Processed: test_input")
    
    def test_run_with_invalid_task_name(self):
        """Test running the agent with an invalid task name."""
        # Define a task
        @self.agent.task
        def test_task(input_data):
            return f"Processed: {input_data}"
        
        # Run the agent with an invalid task name
        with self.assertRaises(ValueError):
            self.agent.run("test_input", task_name="nonexistent_task")
    
    def test_run_with_no_tasks(self):
        """Test running the agent with no tasks defined."""
        # Run the agent with no tasks defined
        with self.assertRaises(ValueError):
            self.agent.run("test_input")
    
    def test_get_available_tasks(self):
        """Test getting available tasks."""
        # Define tasks
        @self.agent.task
        def task1(input_data):
            """Task 1 description."""
            return f"Task 1: {input_data}"
        
        @self.agent.task
        def task2(input_data):
            """Task 2 description."""
            return f"Task 2: {input_data}"
        
        # Get available tasks
        tasks = self.agent.get_available_tasks()
        self.assertEqual(len(tasks), 2)
        
        # Check task information
        task1_info = next(t for t in tasks if t["name"] == "task1")
        self.assertEqual(task1_info["description"], "Task 1 description.")
        
        task2_info = next(t for t in tasks if t["name"] == "task2")
        self.assertEqual(task2_info["description"], "Task 2 description.")
    
    @patch('autoai_agentrag.rag.RAGConnector')
    @patch('autoai_agentrag.ml.TextClassificationModel')
    def test_integration_with_rag_and_ml(self, mock_model_class, mock_rag_class):
        """Test integration with RAG and ML components."""
        # Set up mocks
        mock_rag = mock_rag_class.return_value
        mock_rag.query.return_value = [{"source": "test", "data": {"result": "test_data"}}]
        
        mock_model = mock_model_class.return_value
        mock_model.predict.return_value = {"class": "positive", "probabilities": {"positive": 0.8, "negative": 0.2}}
        
        # Add RAG and ML to agent
        self.agent.add_rag(mock_rag)
        self.agent.add_model(mock_model, name="classifier")
        
        # Define a task that uses both RAG and ML
        @self.agent.task
        def analyze(input_data):
            context = self.agent.rag.query(input_data)
            classification = self.agent.models["classifier"].predict(input_data)
            return {
                "input": input_data,
                "context": context,
                "classification": classification
            }
        
        # Run the agent
        result = self.agent.run("test_input")
        
        # Check the result
        self.assertEqual(result["input"], "test_input")
        self.assertEqual(result["context"], [{"source": "test", "data": {"result": "test_data"}}])
        self.assertEqual(result["classification"], {"class": "positive", "probabilities": {"positive": 0.8, "negative": 0.2}})
        
        # Verify mock calls
        mock_rag.query.assert_called_once_with("test_input")
        mock_model.predict.assert_called_once_with("test_input")


if __name__ == "__main__":
    unittest.main() 