"""
Unit tests for the RAG module.
"""

import unittest
from unittest.mock import MagicMock, patch

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from autoai_agentrag.rag import RAGConnector, DataSource


class TestRAGConnector(unittest.TestCase):
    """Tests for the RAGConnector class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.rag = RAGConnector()
    
    def test_initialization(self):
        """Test RAG initialization."""
        self.assertEqual(len(self.rag.sources), 0)
        self.assertEqual(len(self.rag.config), 0)
    
    def test_add_source(self):
        """Test adding a data source."""
        # Add a web source
        source_name = self.rag.add_source("web", url="https://example.com/api")
        self.assertEqual(len(self.rag.sources), 1)
        self.assertIn(source_name, self.rag.sources)
        self.assertEqual(self.rag.sources[source_name].source_type, "web")
        self.assertEqual(self.rag.sources[source_name].config["url"], "https://example.com/api")
        
        # Add a database source
        source_name = self.rag.add_source("database", name="db_source", connection_string="sqlite:///test.db")
        self.assertEqual(len(self.rag.sources), 2)
        self.assertEqual(source_name, "db_source")
        self.assertIn(source_name, self.rag.sources)
        self.assertEqual(self.rag.sources[source_name].source_type, "database")
        self.assertEqual(self.rag.sources[source_name].config["connection_string"], "sqlite:///test.db")
    
    def test_remove_source(self):
        """Test removing a data source."""
        # Add a source
        source_name = self.rag.add_source("web", name="test_source", url="https://example.com/api")
        self.assertEqual(len(self.rag.sources), 1)
        
        # Remove the source
        self.rag.remove_source(source_name)
        self.assertEqual(len(self.rag.sources), 0)
        self.assertNotIn(source_name, self.rag.sources)
        
        # Try to remove a non-existent source
        self.rag.remove_source("nonexistent_source")  # Should not raise an exception
    
    def test_query_all_sources(self):
        """Test querying all data sources."""
        # Create mock sources
        source1 = MagicMock(spec=DataSource)
        source1.query.return_value = {"source": "source1", "data": {"result": "data1"}}
        
        source2 = MagicMock(spec=DataSource)
        source2.query.return_value = {"source": "source2", "data": {"result": "data2"}}
        
        # Add the sources to the RAG connector
        self.rag.sources = {"source1": source1, "source2": source2}
        
        # Query all sources
        results = self.rag.query("test query")
        
        # Check results
        self.assertEqual(len(results), 2)
        self.assertIn({"source": "source1", "data": {"result": "data1"}}, results)
        self.assertIn({"source": "source2", "data": {"result": "data2"}}, results)
        
        # Verify mock calls
        source1.query.assert_called_once_with("test query")
        source2.query.assert_called_once_with("test query")
    
    def test_query_specific_sources(self):
        """Test querying specific data sources."""
        # Create mock sources
        source1 = MagicMock(spec=DataSource)
        source1.query.return_value = {"source": "source1", "data": {"result": "data1"}}
        
        source2 = MagicMock(spec=DataSource)
        source2.query.return_value = {"source": "source2", "data": {"result": "data2"}}
        
        # Add the sources to the RAG connector
        self.rag.sources = {"source1": source1, "source2": source2}
        
        # Query only source1
        results = self.rag.query("test query", sources=["source1"])
        
        # Check results
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], {"source": "source1", "data": {"result": "data1"}})
        
        # Verify mock calls
        source1.query.assert_called_once_with("test query")
        source2.query.assert_not_called()
    
    def test_query_nonexistent_sources(self):
        """Test querying non-existent sources."""
        # Create a mock source
        source1 = MagicMock(spec=DataSource)
        source1.query.return_value = {"source": "source1", "data": {"result": "data1"}}
        
        # Add the source to the RAG connector
        self.rag.sources = {"source1": source1}
        
        # Query a non-existent source
        results = self.rag.query("test query", sources=["nonexistent_source"])
        
        # Check results (should be empty)
        self.assertEqual(len(results), 0)
        
        # Verify mock calls
        source1.query.assert_not_called()
    
    def test_query_error_handling(self):
        """Test error handling during queries."""
        # Create a mock source that raises an exception
        source1 = MagicMock(spec=DataSource)
        source1.query.side_effect = Exception("Test error")
        
        # Add the source to the RAG connector
        self.rag.sources = {"source1": source1}
        
        # Query the source (should not raise an exception)
        results = self.rag.query("test query")
        
        # Check results
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["source"], "source1")
        self.assertEqual(results[0]["error"], "Test error")
        
        # Verify mock calls
        source1.query.assert_called_once_with("test query")
    
    def test_get_available_sources(self):
        """Test getting available data sources."""
        # Create mock sources
        source1 = MagicMock(spec=DataSource)
        source1.source_type = "web"
        
        source2 = MagicMock(spec=DataSource)
        source2.source_type = "database"
        
        # Add the sources to the RAG connector
        self.rag.sources = {"source1": source1, "source2": source2}
        
        # Get available sources
        sources = self.rag.get_available_sources()
        
        # Check results
        self.assertEqual(len(sources), 2)
        
        source1_info = next(s for s in sources if s["name"] == "source1")
        self.assertEqual(source1_info["type"], "web")
        
        source2_info = next(s for s in sources if s["name"] == "source2")
        self.assertEqual(source2_info["type"], "database")


class TestDataSource(unittest.TestCase):
    """Tests for the DataSource class."""
    
    def test_web_source(self):
        """Test a web data source."""
        source = DataSource(
            name="test_web",
            source_type="web",
            config={"url": "https://example.com/api"}
        )
        
        with patch('requests.get') as mock_get:
            # Configure the mock
            mock_response = MagicMock()
            mock_response.json.return_value = {"test": "data"}
            mock_get.return_value = mock_response
            
            # Query the source
            result = source.query("test query")
            
            # Check the result
            self.assertEqual(result["source"], "test_web")
            self.assertEqual(result["data"], {"test": "data"})
            
            # Verify mock calls
            mock_get.assert_called_once()
            self.assertEqual(mock_get.call_args[1]["url"], "https://example.com/api")
            self.assertEqual(mock_get.call_args[1]["params"]["query"], "test query")
    
    def test_web_source_error(self):
        """Test error handling for web data source."""
        source = DataSource(
            name="test_web",
            source_type="web",
            config={"url": "https://example.com/api"}
        )
        
        with patch('requests.get') as mock_get:
            # Configure the mock to raise an exception
            mock_get.side_effect = Exception("Test error")
            
            # Query the source
            result = source.query("test query")
            
            # Check the result
            self.assertEqual(result["source"], "test_web")
            self.assertEqual(result["error"], "Test error")
            
            # Verify mock calls
            mock_get.assert_called_once()
    
    def test_unsupported_source_type(self):
        """Test querying an unsupported source type."""
        source = DataSource(
            name="test_unsupported",
            source_type="unsupported",
            config={}
        )
        
        # Query the source (should raise ValueError)
        with self.assertRaises(ValueError):
            source.query("test query")


if __name__ == "__main__":
    unittest.main() 