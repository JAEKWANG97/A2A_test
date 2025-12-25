from typing import Dict
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.agents import Agent
from ..core.exceptions import AgentNotFoundError


class RunnerPool:
    """Manages Runner instances for each agent."""
    
    def __init__(self, session_service: InMemorySessionService, app_name: str):
        self.session_service = session_service
        self.app_name = app_name
        self._runners: Dict[str, Runner] = {}
    
    def register_agent(self, agent: Agent) -> None:
        """Register an agent and create its runner."""
        runner = Runner(
            agent=agent,
            app_name=self.app_name,
            session_service=self.session_service
        )
        self._runners[agent.name] = runner
    
    def get_runner(self, agent_name: str) -> Runner:
        """Get runner for agent by name."""
        if agent_name not in self._runners:
            raise AgentNotFoundError(f"Agent '{agent_name}' not found in runner pool")
        return self._runners[agent_name]
    
    def has_agent(self, agent_name: str) -> bool:
        """Check if agent is registered."""
        return agent_name in self._runners
