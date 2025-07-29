"""
Dashboard module for monitoring agent performance and metrics.
"""

import os
import json
import logging
import threading
import time
from typing import Dict, List, Any, Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

logger = logging.getLogger(__name__)

# Models for API
class AgentStatus(BaseModel):
    """Status information for an agent."""
    name: str
    status: str
    last_run: Optional[str] = None
    tasks_completed: int = 0
    tasks_failed: int = 0
    uptime: int = 0  # in seconds


class TaskMetrics(BaseModel):
    """Metrics for a task execution."""
    task_id: str
    agent_name: str
    task_name: str
    start_time: str
    end_time: Optional[str] = None
    duration: Optional[float] = None  # in seconds
    status: str
    input_summary: Optional[str] = None
    output_summary: Optional[str] = None


class DashboardConfig(BaseModel):
    """Configuration for the dashboard."""
    host: str = "127.0.0.1"
    port: int = 8000
    refresh_interval: int = 5  # in seconds
    data_retention_days: int = 7


class Dashboard:
    """
    Dashboard for monitoring agent performance and metrics.
    """
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = DashboardConfig(**(config or {}))
        self.agents: Dict[str, AgentStatus] = {}
        self.tasks: List[TaskMetrics] = []
        self.app = FastAPI(title="AutoAI-AgentRAG Dashboard")
        self._setup_routes()
        self._running = False
        self._server_thread = None
        logger.info("Initialized dashboard")
    
    def _setup_routes(self) -> None:
        """Set up API routes."""
        @self.app.get("/", response_class=HTMLResponse)
        async def get_dashboard():
            """Return the dashboard HTML."""
            return """
            <!DOCTYPE html>
            <html>
            <head>
                <title>AutoAI-AgentRAG Dashboard</title>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body {
                        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                        line-height: 1.6;
                        color: #333;
                        max-width: 1200px;
                        margin: 0 auto;
                        padding: 20px;
                    }
                    h1, h2 {
                        color: #0066cc;
                    }
                    .card {
                        border: 1px solid #ddd;
                        border-radius: 4px;
                        padding: 15px;
                        margin-bottom: 20px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    }
                    .grid {
                        display: grid;
                        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                        grid-gap: 20px;
                    }
                    table {
                        width: 100%;
                        border-collapse: collapse;
                    }
                    th, td {
                        padding: 8px;
                        text-align: left;
                        border-bottom: 1px solid #ddd;
                    }
                    th {
                        background-color: #f2f2f2;
                    }
                    .status-active {
                        color: green;
                        font-weight: bold;
                    }
                    .status-inactive {
                        color: red;
                    }
                    .status-pending {
                        color: orange;
                    }
                </style>
                <script>
                    // Function to refresh agent data
                    function refreshAgents() {
                        fetch('/api/agents')
                            .then(response => response.json())
                            .then(data => {
                                const agentGrid = document.getElementById('agent-grid');
                                agentGrid.innerHTML = '';
                                
                                data.forEach(agent => {
                                    const card = document.createElement('div');
                                    card.className = 'card';
                                    
                                    let statusClass = 'status-inactive';
                                    if (agent.status === 'active') {
                                        statusClass = 'status-active';
                                    } else if (agent.status === 'pending') {
                                        statusClass = 'status-pending';
                                    }
                                    
                                    card.innerHTML = `
                                        <h3>${agent.name}</h3>
                                        <p>Status: <span class="${statusClass}">${agent.status}</span></p>
                                        <p>Tasks completed: ${agent.tasks_completed}</p>
                                        <p>Tasks failed: ${agent.tasks_failed}</p>
                                        <p>Last run: ${agent.last_run || 'Never'}</p>
                                        <p>Uptime: ${formatUptime(agent.uptime)}</p>
                                    `;
                                    
                                    agentGrid.appendChild(card);
                                });
                            })
                            .catch(error => console.error('Error fetching agents:', error));
                    }
                    
                    // Function to refresh task data
                    function refreshTasks() {
                        fetch('/api/tasks')
                            .then(response => response.json())
                            .then(data => {
                                const taskTable = document.getElementById('task-table');
                                const tbody = taskTable.querySelector('tbody');
                                tbody.innerHTML = '';
                                
                                data.forEach(task => {
                                    const row = document.createElement('tr');
                                    
                                    let statusClass = '';
                                    if (task.status === 'completed') {
                                        statusClass = 'status-active';
                                    } else if (task.status === 'failed') {
                                        statusClass = 'status-inactive';
                                    } else {
                                        statusClass = 'status-pending';
                                    }
                                    
                                    row.innerHTML = `
                                        <td>${task.task_id.substring(0, 8)}...</td>
                                        <td>${task.agent_name}</td>
                                        <td>${task.task_name}</td>
                                        <td>${task.start_time}</td>
                                        <td>${task.end_time || '-'}</td>
                                        <td>${task.duration !== null ? task.duration.toFixed(2) + 's' : '-'}</td>
                                        <td class="${statusClass}">${task.status}</td>
                                    `;
                                    
                                    tbody.appendChild(row);
                                });
                            })
                            .catch(error => console.error('Error fetching tasks:', error));
                    }
                    
                    // Format uptime in seconds to a readable format
                    function formatUptime(seconds) {
                        if (!seconds) return '0s';
                        
                        const days = Math.floor(seconds / 86400);
                        const hours = Math.floor((seconds % 86400) / 3600);
                        const minutes = Math.floor((seconds % 3600) / 60);
                        const secs = seconds % 60;
                        
                        let result = '';
                        if (days > 0) result += days + 'd ';
                        if (hours > 0) result += hours + 'h ';
                        if (minutes > 0) result += minutes + 'm ';
                        if (secs > 0 || result === '') result += secs + 's';
                        
                        return result;
                    }
                    
                    // Refresh data periodically
                    document.addEventListener('DOMContentLoaded', function() {
                        refreshAgents();
                        refreshTasks();
                        
                        setInterval(() => {
                            refreshAgents();
                            refreshTasks();
                        }, 5000); // Refresh every 5 seconds
                    });
                </script>
            </head>
            <body>
                <h1>AutoAI-AgentRAG Dashboard</h1>
                
                <h2>Agents</h2>
                <div id="agent-grid" class="grid">
                    <!-- Agent cards will be inserted here -->
                    <div class="card">
                        <p>Loading agent data...</p>
                    </div>
                </div>
                
                <h2>Recent Tasks</h2>
                <table id="task-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Agent</th>
                            <th>Task</th>
                            <th>Start Time</th>
                            <th>End Time</th>
                            <th>Duration</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <!-- Task rows will be inserted here -->
                        <tr>
                            <td colspan="7">Loading task data...</td>
                        </tr>
                    </tbody>
                </table>
            </body>
            </html>
            """
        
        @self.app.get("/api/agents")
        async def get_agents():
            """Get all agent statuses."""
            return list(self.agents.values())
        
        @self.app.get("/api/agents/{agent_name}")
        async def get_agent(agent_name: str):
            """Get a specific agent's status."""
            if agent_name not in self.agents:
                raise HTTPException(status_code=404, detail=f"Agent {agent_name} not found")
            return self.agents[agent_name]
        
        @self.app.get("/api/tasks")
        async def get_tasks():
            """Get all task metrics."""
            return self.tasks
        
        @self.app.get("/api/tasks/{task_id}")
        async def get_task(task_id: str):
            """Get a specific task's metrics."""
            for task in self.tasks:
                if task.task_id == task_id:
                    return task
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    
    def register_agent(self, agent_name: str) -> None:
        """
        Register an agent with the dashboard.
        
        Args:
            agent_name: Name of the agent to register
        """
        if agent_name in self.agents:
            logger.warning(f"Agent {agent_name} already registered")
            return
        
        self.agents[agent_name] = AgentStatus(
            name=agent_name,
            status="inactive"
        )
        logger.info(f"Registered agent: {agent_name}")
    
    def update_agent_status(self, agent_name: str, status: str) -> None:
        """
        Update an agent's status.
        
        Args:
            agent_name: Name of the agent to update
            status: New status ("active", "inactive", "pending")
        """
        if agent_name not in self.agents:
            self.register_agent(agent_name)
        
        self.agents[agent_name].status = status
        if status == "active":
            self.agents[agent_name].last_run = time.strftime("%Y-%m-%d %H:%M:%S")
        
        logger.info(f"Updated agent {agent_name} status to {status}")
    
    def record_task(
        self,
        agent_name: str,
        task_name: str,
        task_id: Optional[str] = None,
        input_summary: Optional[str] = None
    ) -> str:
        """
        Record the start of a task.
        
        Args:
            agent_name: Name of the agent running the task
            task_name: Name of the task
            task_id: Optional ID for the task (generated if not provided)
            input_summary: Optional summary of the task input
            
        Returns:
            The task ID
        """
        if agent_name not in self.agents:
            self.register_agent(agent_name)
        
        task_id = task_id or f"{int(time.time())}-{len(self.tasks)}"
        
        task = TaskMetrics(
            task_id=task_id,
            agent_name=agent_name,
            task_name=task_name,
            start_time=time.strftime("%Y-%m-%d %H:%M:%S"),
            status="running",
            input_summary=input_summary
        )
        
        self.tasks.append(task)
        logger.info(f"Started task {task_id} for agent {agent_name}")
        
        # Update agent status
        self.update_agent_status(agent_name, "active")
        
        return task_id
    
    def complete_task(
        self,
        task_id: str,
        status: str = "completed",
        output_summary: Optional[str] = None
    ) -> None:
        """
        Mark a task as completed.
        
        Args:
            task_id: ID of the task to complete
            status: Status of the completed task ("completed", "failed")
            output_summary: Optional summary of the task output
        """
        for i, task in enumerate(self.tasks):
            if task.task_id == task_id:
                task.end_time = time.strftime("%Y-%m-%d %H:%M:%S")
                
                # Calculate duration
                try:
                    start_time = time.strptime(task.start_time, "%Y-%m-%d %H:%M:%S")
                    end_time = time.strptime(task.end_time, "%Y-%m-%d %H:%M:%S")
                    task.duration = time.mktime(end_time) - time.mktime(start_time)
                except:
                    task.duration = 0
                
                task.status = status
                task.output_summary = output_summary
                
                # Update agent metrics
                agent = self.agents.get(task.agent_name)
                if agent:
                    if status == "completed":
                        agent.tasks_completed += 1
                    elif status == "failed":
                        agent.tasks_failed += 1
                
                logger.info(f"Completed task {task_id} with status {status}")
                return
        
        logger.warning(f"Task {task_id} not found")
    
    def start(self) -> None:
        """Start the dashboard server."""
        if self._running:
            logger.warning("Dashboard already running")
            return
        
        def run_server():
            uvicorn.run(
                self.app,
                host=self.config.host,
                port=self.config.port,
                log_level="info"
            )
        
        self._server_thread = threading.Thread(target=run_server)
        self._server_thread.daemon = True
        self._server_thread.start()
        self._running = True
        
        logger.info(f"Started dashboard server at http://{self.config.host}:{self.config.port}")
    
    def stop(self) -> None:
        """Stop the dashboard server."""
        if not self._running:
            logger.warning("Dashboard not running")
            return
        
        # In a real implementation, would need to properly shut down uvicorn
        self._running = False
        logger.info("Stopped dashboard server")
    
    def is_running(self) -> bool:
        """Check if the dashboard is running."""
        return self._running


# Singleton instance
_dashboard_instance = None

def get_dashboard(config: Optional[Dict[str, Any]] = None) -> Dashboard:
    """
    Get the dashboard instance.
    
    Args:
        config: Optional configuration for the dashboard
        
    Returns:
        The dashboard instance
    """
    global _dashboard_instance
    if _dashboard_instance is None:
        _dashboard_instance = Dashboard(config)
    return _dashboard_instance 