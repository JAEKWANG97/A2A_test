from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from .agents import create_weather_agent, create_time_agent, create_root_agent
from .services import RunnerPool, A2AService
from .core import SessionManager
from .tools import create_a2a_tools


class AgentTeam:
    """Manages the full agent team and orchestration."""
    
    def __init__(self, session_service: InMemorySessionService, app_name: str):
        self.session_service = session_service
        self.app_name = app_name
        
        # Initialize core services
        self.session_manager = SessionManager(session_service)
        self.runner_pool = RunnerPool(session_service, app_name)
        self.a2a_service = A2AService(self.runner_pool, self.session_manager)
        
        # Create A2A tools with service dependencies
        a2a_tools = create_a2a_tools(self.a2a_service, self.session_manager)
        
        # Create agents
        self.weather_agent = create_weather_agent()
        self.time_agent = create_time_agent()
        self.root_agent = create_root_agent(a2a_tools)
        
        # Register all agents in runner pool
        self.runner_pool.register_agent(self.weather_agent)
        self.runner_pool.register_agent(self.time_agent)
        
        # Create root runner (main entry point)
        self.root_runner = Runner(
            agent=self.root_agent,
            app_name=app_name,
            session_service=session_service
        )


def build_agent_team(session_service: InMemorySessionService, app_name: str) -> AgentTeam:
    """Build and return configured agent team."""
    return AgentTeam(session_service, app_name)
