"""
Plugin system for extending AutoAI-AgentRAG functionality.
"""

from typing import Any, Callable, Dict, List, Optional, Type, Union
import logging
import os
import importlib
import inspect
from abc import ABC, abstractmethod

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class Plugin(BaseModel, ABC):
    """
    Base class for all plugins.
    
    Attributes:
        name: Name of the plugin
        version: Version of the plugin
        description: Description of the plugin's functionality
        config: Configuration options for the plugin
    """
    name: str
    version: str = "0.1.0"
    description: Optional[str] = None
    config: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        arbitrary_types_allowed = True
    
    @abstractmethod
    def initialize(self) -> None:
        """Initialize the plugin."""
        pass
    
    @abstractmethod
    def shutdown(self) -> None:
        """Clean up resources when shutting down."""
        pass


class DataSourcePlugin(Plugin):
    """
    Plugin for adding custom data sources to RAG.
    
    This plugin type allows users to implement custom data retrieval logic.
    """
    source_type: str
    
    @abstractmethod
    def query(self, query_text: str, **kwargs) -> Dict[str, Any]:
        """
        Query this data source with the given text.
        
        Args:
            query_text: The text to query for
            **kwargs: Additional query parameters
            
        Returns:
            A dictionary containing the query results
        """
        pass


class ModelPlugin(Plugin):
    """
    Plugin for adding custom ML models.
    
    This plugin type allows users to implement custom model logic.
    """
    model_type: str
    
    @abstractmethod
    def predict(self, input_data: Any, **kwargs) -> Any:
        """
        Make predictions using the model.
        
        Args:
            input_data: The input data to make predictions on
            **kwargs: Additional arguments for prediction
            
        Returns:
            The model's predictions
        """
        pass
    
    @abstractmethod
    def train(self, training_data: Any, **kwargs) -> Dict[str, Any]:
        """
        Train the model on the given data.
        
        Args:
            training_data: The data to train on
            **kwargs: Additional arguments for training
            
        Returns:
            Training metrics
        """
        pass


class AgentPlugin(Plugin):
    """
    Plugin for extending agent capabilities.
    
    This plugin type allows users to implement custom agent behaviors.
    """
    
    @abstractmethod
    def process(self, agent: Any, input_data: Any, **kwargs) -> Any:
        """
        Process input data using custom logic.
        
        Args:
            agent: The agent instance
            input_data: The input data to process
            **kwargs: Additional processing parameters
            
        Returns:
            The processing results
        """
        pass


class PluginManager:
    """
    Manager for loading, registering, and using plugins.
    """
    def __init__(self):
        self.plugins: Dict[str, Plugin] = {}
        self.plugin_types: Dict[str, Type[Plugin]] = {
            "data_source": DataSourcePlugin,
            "model": ModelPlugin,
            "agent": AgentPlugin
        }
        logger.info("Initialized PluginManager")
    
    def register_plugin(self, plugin: Plugin) -> None:
        """
        Register a plugin with the manager.
        
        Args:
            plugin: The plugin to register
        """
        if plugin.name in self.plugins:
            logger.warning(f"Plugin {plugin.name} already registered, replacing")
        
        self.plugins[plugin.name] = plugin
        plugin.initialize()
        logger.info(f"Registered plugin: {plugin.name} (v{plugin.version})")
    
    def unregister_plugin(self, plugin_name: str) -> None:
        """
        Unregister a plugin by name.
        
        Args:
            plugin_name: Name of the plugin to unregister
        """
        if plugin_name in self.plugins:
            plugin = self.plugins[plugin_name]
            plugin.shutdown()
            del self.plugins[plugin_name]
            logger.info(f"Unregistered plugin: {plugin_name}")
        else:
            logger.warning(f"Plugin not found: {plugin_name}")
    
    def get_plugin(self, plugin_name: str) -> Optional[Plugin]:
        """
        Get a plugin by name.
        
        Args:
            plugin_name: Name of the plugin to get
            
        Returns:
            The plugin if found, None otherwise
        """
        return self.plugins.get(plugin_name)
    
    def load_plugin_from_path(self, path: str) -> Optional[Plugin]:
        """
        Load a plugin from a Python file or module.
        
        Args:
            path: Path to the plugin file or module name
            
        Returns:
            The loaded plugin if successful, None otherwise
        """
        try:
            if os.path.exists(path):
                # Load from file path
                module_name = os.path.basename(path).replace(".py", "")
                spec = importlib.util.spec_from_file_location(module_name, path)
                if spec is None or spec.loader is None:
                    logger.error(f"Failed to load plugin spec from {path}")
                    return None
                
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
            else:
                # Try to load as a module name
                module = importlib.import_module(path)
            
            # Find plugin classes in the module
            for name, obj in inspect.getmembers(module):
                if (inspect.isclass(obj) and issubclass(obj, Plugin) and 
                    obj is not Plugin and obj is not DataSourcePlugin and 
                    obj is not ModelPlugin and obj is not AgentPlugin):
                    
                    # Create an instance of the plugin
                    plugin = obj()
                    self.register_plugin(plugin)
                    return plugin
            
            logger.warning(f"No plugin class found in {path}")
            return None
        
        except Exception as e:
            logger.error(f"Error loading plugin from {path}: {e}")
            return None
    
    def load_plugins_from_directory(self, directory: str) -> List[Plugin]:
        """
        Load all plugins from a directory.
        
        Args:
            directory: Directory containing plugin files
            
        Returns:
            List of successfully loaded plugins
        """
        loaded_plugins = []
        
        if not os.path.isdir(directory):
            logger.error(f"Plugin directory not found: {directory}")
            return loaded_plugins
        
        for filename in os.listdir(directory):
            if filename.endswith(".py") and not filename.startswith("__"):
                path = os.path.join(directory, filename)
                plugin = self.load_plugin_from_path(path)
                if plugin:
                    loaded_plugins.append(plugin)
        
        logger.info(f"Loaded {len(loaded_plugins)} plugins from {directory}")
        return loaded_plugins
    
    def get_plugins_by_type(self, plugin_type: str) -> List[Plugin]:
        """
        Get all plugins of a specific type.
        
        Args:
            plugin_type: Type of plugins to get ("data_source", "model", "agent")
            
        Returns:
            List of plugins of the specified type
        """
        if plugin_type not in self.plugin_types:
            logger.warning(f"Unknown plugin type: {plugin_type}")
            return []
        
        plugin_class = self.plugin_types[plugin_type]
        return [p for p in self.plugins.values() if isinstance(p, plugin_class)]
    
    def get_available_plugins(self) -> Dict[str, Dict[str, str]]:
        """
        Get information about all available plugins.
        
        Returns:
            Dictionary mapping plugin names to their information
        """
        return {
            name: {
                "version": plugin.version,
                "description": plugin.description or "No description",
                "type": self._get_plugin_type(plugin)
            }
            for name, plugin in self.plugins.items()
        }
    
    def _get_plugin_type(self, plugin: Plugin) -> str:
        """Determine the type of a plugin."""
        if isinstance(plugin, DataSourcePlugin):
            return "data_source"
        elif isinstance(plugin, ModelPlugin):
            return "model"
        elif isinstance(plugin, AgentPlugin):
            return "agent"
        else:
            return "unknown" 