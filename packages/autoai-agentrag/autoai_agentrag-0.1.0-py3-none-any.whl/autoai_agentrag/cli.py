"""
Command-line interface for AutoAI-AgentRAG.
"""

import os
import sys
import json
import logging
import time
from typing import Optional, List, Dict, Any

import click

from autoai_agentrag import Agent, RAGConnector, MLModel, PluginManager
from autoai_agentrag.ml import TextClassificationModel, TextGenerationModel, EmbeddingModel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Default project structure
DEFAULT_PROJECT_STRUCTURE = {
    "agents": {},
    "models": {},
    "rag": {
        "sources": {}
    },
    "plugins": []
}

# CLI context for sharing data between commands
class CLIContext:
    def __init__(self):
        self.project_path = None
        self.config = None
        self.plugin_manager = PluginManager()


# Create a Click context object
pass_context = click.make_pass_decorator(CLIContext, ensure=True)


@click.group()
@click.version_option()
@click.option(
    "--project", "-p",
    help="Path to project directory",
    type=click.Path(file_okay=False),
    default="."
)
@pass_context
def main(ctx: CLIContext, project: str):
    """
    AutoAI-AgentRAG: AI Agents with RAG and ML capabilities.
    
    This CLI tool helps you create, manage, and run AI agents with
    Retrieval-Augmented Generation and Machine Learning capabilities.
    """
    ctx.project_path = os.path.abspath(project)
    
    # Load project config if it exists
    config_path = os.path.join(ctx.project_path, "autoai_config.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                ctx.config = json.load(f)
            logger.info(f"Loaded project config from {config_path}")
        except Exception as e:
            logger.error(f"Error loading project config: {e}")
            ctx.config = DEFAULT_PROJECT_STRUCTURE.copy()
    else:
        ctx.config = DEFAULT_PROJECT_STRUCTURE.copy()


@main.command()
@click.argument("project_name")
@pass_context
def init(ctx: CLIContext, project_name: str):
    """
    Initialize a new AutoAI-AgentRAG project.
    
    PROJECT_NAME is the name of the new project directory.
    """
    project_dir = os.path.join(ctx.project_path, project_name)
    
    if os.path.exists(project_dir):
        if not click.confirm(f"Directory {project_name} already exists. Continue?"):
            click.echo("Aborted.")
            return
    else:
        os.makedirs(project_dir)
    
    # Create project structure
    os.makedirs(os.path.join(project_dir, "agents"), exist_ok=True)
    os.makedirs(os.path.join(project_dir, "models"), exist_ok=True)
    os.makedirs(os.path.join(project_dir, "plugins"), exist_ok=True)
    os.makedirs(os.path.join(project_dir, "data"), exist_ok=True)
    
    # Create config file
    config = DEFAULT_PROJECT_STRUCTURE.copy()
    config["project_name"] = project_name
    config["created_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
    
    config_path = os.path.join(project_dir, "autoai_config.json")
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    
    # Create example agent file
    example_agent_path = os.path.join(project_dir, "agents", "example_agent.py")
    with open(example_agent_path, "w") as f:
        f.write('''"""
Example agent for AutoAI-AgentRAG.
"""

from autoai_agentrag import Agent, RAGConnector, MLModel

def create_agent():
    """Create and configure the example agent."""
    agent = Agent(name="example_agent", description="An example agent")
    
    # Add a RAG connector
    rag = RAGConnector()
    # Add sources as needed
    # rag.add_source("web", url="https://example.com/api")
    agent.add_rag(rag)
    
    # Add an ML model
    # model = MLModel.from_pretrained("text-classification")
    # agent.add_model(model)
    
    # Define agent tasks
    @agent.task
    def greet(name):
        """Greet the user by name."""
        return f"Hello, {name}!"
    
    @agent.task
    def analyze(text):
        """Analyze the given text."""
        # In a real agent, this would use RAG and ML capabilities
        return {
            "length": len(text),
            "sentiment": "positive" if "good" in text.lower() else "negative"
        }
    
    return agent

# Create the agent when this module is imported
example_agent = create_agent()
''')
    
    click.echo(f"Initialized AutoAI-AgentRAG project in {project_dir}")
    click.echo("Project structure:")
    click.echo(f"  {project_name}/")
    click.echo(f"  ├── agents/")
    click.echo(f"  │   └── example_agent.py")
    click.echo(f"  ├── models/")
    click.echo(f"  ├── plugins/")
    click.echo(f"  ├── data/")
    click.echo(f"  └── autoai_config.json")


@main.group()
def create():
    """Create new components (agent, model, etc.)."""
    pass


@create.command("agent")
@click.argument("name")
@click.option("--description", "-d", help="Description of the agent")
@pass_context
def create_agent(ctx: CLIContext, name: str, description: Optional[str] = None):
    """
    Create a new agent.
    
    NAME is the name of the new agent.
    """
    agent_file = f"{name.lower().replace(' ', '_')}_agent.py"
    agent_path = os.path.join(ctx.project_path, "agents", agent_file)
    
    if os.path.exists(agent_path):
        if not click.confirm(f"Agent file {agent_file} already exists. Overwrite?"):
            click.echo("Aborted.")
            return
    
    os.makedirs(os.path.dirname(agent_path), exist_ok=True)
    
    with open(agent_path, "w") as f:
        f.write(f'''"""
{name} agent for AutoAI-AgentRAG.
"""

from autoai_agentrag import Agent, RAGConnector, MLModel

def create_agent():
    """Create and configure the {name} agent."""
    agent = Agent(
        name="{name}",
        description="{description or f'The {name} agent'}"
    )
    
    # Add a RAG connector
    rag = RAGConnector()
    # Add sources as needed
    # rag.add_source("web", url="https://example.com/api")
    agent.add_rag(rag)
    
    # Define agent tasks
    @agent.task
    def process(input_data):
        """Process the input data."""
        # Implement your agent logic here
        return {{"result": f"Processed: {{input_data}}"}}
    
    return agent

# Create the agent when this module is imported
{name.lower().replace(' ', '_')}_agent = create_agent()
''')
    
    # Update config
    if "agents" not in ctx.config:
        ctx.config["agents"] = {}
    
    ctx.config["agents"][name] = {
        "file": agent_file,
        "description": description or f"The {name} agent"
    }
    
    config_path = os.path.join(ctx.project_path, "autoai_config.json")
    with open(config_path, "w") as f:
        json.dump(ctx.config, f, indent=2)
    
    click.echo(f"Created agent: {name}")
    click.echo(f"Agent file: {agent_path}")


@main.group()
def add():
    """Add components to existing agents."""
    pass


@add.command("rag")
@click.option("--agent", "-a", help="Agent to add RAG to", required=True)
@click.option("--source", "-s", help="Source type (web, database, file)", required=True)
@click.option("--name", "-n", help="Name for the source")
@click.option("--url", help="URL for web sources")
@click.option("--connection", help="Connection string for database sources")
@click.option("--file-path", help="File path for file sources")
@pass_context
def add_rag(
    ctx: CLIContext,
    agent: str,
    source: str,
    name: Optional[str] = None,
    url: Optional[str] = None,
    connection: Optional[str] = None,
    file_path: Optional[str] = None
):
    """
    Add a RAG source to an agent.
    """
    if agent not in ctx.config.get("agents", {}):
        click.echo(f"Agent {agent} not found.")
        return
    
    source_config = {}
    if source == "web" and url:
        source_config["url"] = url
    elif source == "database" and connection:
        source_config["connection_string"] = connection
    elif source == "file" and file_path:
        source_config["file_path"] = file_path
    else:
        click.echo(f"Missing required parameters for source type: {source}")
        return
    
    source_name = name or f"{source}_{len(ctx.config['rag']['sources'])}"
    
    # Update config
    if "rag" not in ctx.config:
        ctx.config["rag"] = {"sources": {}}
    
    ctx.config["rag"]["sources"][source_name] = {
        "type": source,
        "config": source_config
    }
    
    if "agents" not in ctx.config:
        ctx.config["agents"] = {}
    
    if agent not in ctx.config["agents"]:
        ctx.config["agents"][agent] = {}
    
    if "rag_sources" not in ctx.config["agents"][agent]:
        ctx.config["agents"][agent]["rag_sources"] = []
    
    ctx.config["agents"][agent]["rag_sources"].append(source_name)
    
    config_path = os.path.join(ctx.project_path, "autoai_config.json")
    with open(config_path, "w") as f:
        json.dump(ctx.config, f, indent=2)
    
    click.echo(f"Added {source} source '{source_name}' to agent '{agent}'")


@add.command("model")
@click.option("--agent", "-a", help="Agent to add model to", required=True)
@click.option("--type", "-t", help="Model type (text-classification, text-generation, embedding)", required=True)
@click.option("--name", "-n", help="Name for the model")
@click.option("--pretrained", "-p", help="Pretrained model name")
@pass_context
def add_model(
    ctx: CLIContext,
    agent: str,
    type: str,
    name: Optional[str] = None,
    pretrained: Optional[str] = None
):
    """
    Add an ML model to an agent.
    """
    if agent not in ctx.config.get("agents", {}):
        click.echo(f"Agent {agent} not found.")
        return
    
    model_name = name or f"{type}_{len(ctx.config.get('models', {}))}"
    
    # Update config
    if "models" not in ctx.config:
        ctx.config["models"] = {}
    
    ctx.config["models"][model_name] = {
        "type": type,
        "pretrained": pretrained or type
    }
    
    if "agents" not in ctx.config:
        ctx.config["agents"] = {}
    
    if agent not in ctx.config["agents"]:
        ctx.config["agents"][agent] = {}
    
    if "models" not in ctx.config["agents"][agent]:
        ctx.config["agents"][agent]["models"] = []
    
    ctx.config["agents"][agent]["models"].append(model_name)
    
    config_path = os.path.join(ctx.project_path, "autoai_config.json")
    with open(config_path, "w") as f:
        json.dump(ctx.config, f, indent=2)
    
    click.echo(f"Added {type} model '{model_name}' to agent '{agent}'")


@main.command()
@click.argument("agent_name")
@click.option("--input", "-i", help="Input text for the agent")
@click.option("--task", "-t", help="Specific task to run")
@pass_context
def run(ctx: CLIContext, agent_name: str, input: Optional[str] = None, task: Optional[str] = None):
    """
    Run an agent on the given input.
    
    AGENT_NAME is the name of the agent to run.
    """
    if agent_name not in ctx.config.get("agents", {}):
        click.echo(f"Agent {agent_name} not found.")
        return
    
    agent_config = ctx.config["agents"][agent_name]
    agent_file = agent_config.get("file")
    
    if not agent_file:
        click.echo(f"Agent file not specified for {agent_name}.")
        return
    
    agent_path = os.path.join(ctx.project_path, "agents", agent_file)
    if not os.path.exists(agent_path):
        click.echo(f"Agent file not found: {agent_path}")
        return
    
    # Import the agent module
    sys.path.append(ctx.project_path)
    try:
        module_name = f"agents.{os.path.splitext(agent_file)[0]}"
        agent_module = __import__(module_name, fromlist=["*"])
        
        # Find the agent instance
        agent_instance = None
        for attr_name in dir(agent_module):
            attr = getattr(agent_module, attr_name)
            if isinstance(attr, Agent) and attr.name == agent_name:
                agent_instance = attr
                break
        
        if not agent_instance:
            # Try to find a function that creates the agent
            for attr_name in dir(agent_module):
                attr = getattr(agent_module, attr_name)
                if callable(attr) and attr_name.startswith("create_"):
                    try:
                        agent_instance = attr()
                        if isinstance(agent_instance, Agent) and agent_instance.name == agent_name:
                            break
                        agent_instance = None
                    except:
                        pass
        
        if not agent_instance:
            click.echo(f"Could not find agent instance for {agent_name} in {agent_file}")
            return
        
        # Run the agent
        if not input:
            input = click.prompt("Enter input for the agent")
        
        click.echo(f"Running agent: {agent_name}")
        result = agent_instance.run(input, task_name=task)
        click.echo("Result:")
        click.echo(json.dumps(result, indent=2) if isinstance(result, dict) else result)
        
    except Exception as e:
        click.echo(f"Error running agent: {e}")


@main.command()
@pass_context
def dashboard(ctx: CLIContext):
    """
    Start the monitoring dashboard.
    """
    click.echo("Starting monitoring dashboard...")
    click.echo("Dashboard functionality to be implemented.")
    click.echo("This would typically start a web server with a monitoring interface.")


@main.command()
@click.option("--agent", "-a", help="Show details for a specific agent")
@pass_context
def info(ctx: CLIContext, agent: Optional[str] = None):
    """
    Show information about the project or a specific agent.
    """
    if agent:
        if agent not in ctx.config.get("agents", {}):
            click.echo(f"Agent {agent} not found.")
            return
        
        agent_config = ctx.config["agents"][agent]
        click.echo(f"Agent: {agent}")
        click.echo(f"Description: {agent_config.get('description', 'No description')}")
        click.echo(f"File: {agent_config.get('file', 'Not specified')}")
        
        if "rag_sources" in agent_config and agent_config["rag_sources"]:
            click.echo("RAG Sources:")
            for source_name in agent_config["rag_sources"]:
                source_info = ctx.config.get("rag", {}).get("sources", {}).get(source_name, {})
                click.echo(f"  - {source_name} ({source_info.get('type', 'unknown')})")
        
        if "models" in agent_config and agent_config["models"]:
            click.echo("Models:")
            for model_name in agent_config["models"]:
                model_info = ctx.config.get("models", {}).get(model_name, {})
                click.echo(f"  - {model_name} ({model_info.get('type', 'unknown')})")
        
        # Try to load the agent to get available tasks
        agent_file = agent_config.get("file")
        if agent_file:
            agent_path = os.path.join(ctx.project_path, "agents", agent_file)
            if os.path.exists(agent_path):
                sys.path.append(ctx.project_path)
                try:
                    module_name = f"agents.{os.path.splitext(agent_file)[0]}"
                    agent_module = __import__(module_name, fromlist=["*"])
                    
                    # Find the agent instance
                    agent_instance = None
                    for attr_name in dir(agent_module):
                        attr = getattr(agent_module, attr_name)
                        if isinstance(attr, Agent) and attr.name == agent:
                            agent_instance = attr
                            break
                    
                    if agent_instance:
                        tasks = agent_instance.get_available_tasks()
                        if tasks:
                            click.echo("Available Tasks:")
                            for task in tasks:
                                click.echo(f"  - {task['name']}: {task['description']}")
                except Exception as e:
                    click.echo(f"Error loading agent: {e}")
    else:
        # Show project info
        project_name = ctx.config.get("project_name", "Unnamed Project")
        created_at = ctx.config.get("created_at", "Unknown")
        
        click.echo(f"Project: {project_name}")
        click.echo(f"Created: {created_at}")
        
        agents = ctx.config.get("agents", {})
        if agents:
            click.echo(f"Agents ({len(agents)}):")
            for name, info in agents.items():
                click.echo(f"  - {name}: {info.get('description', 'No description')}")
        else:
            click.echo("No agents defined.")
        
        models = ctx.config.get("models", {})
        if models:
            click.echo(f"Models ({len(models)}):")
            for name, info in models.items():
                click.echo(f"  - {name}: {info.get('type', 'unknown')}")
        
        rag_sources = ctx.config.get("rag", {}).get("sources", {})
        if rag_sources:
            click.echo(f"RAG Sources ({len(rag_sources)}):")
            for name, info in rag_sources.items():
                click.echo(f"  - {name}: {info.get('type', 'unknown')}")


if __name__ == "__main__":
    main() 