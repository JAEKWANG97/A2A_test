from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from .agents import create_weather_agent, create_time_agent, create_broker_agent, create_root_agent
from .services import RunnerPool, A2AService, IntentClassifier, QueryRouter
from .core import SessionManager


class AgentTeam:
    """Manages the full agent team and orchestration."""
    
    def __init__(self, session_service: InMemorySessionService, app_name: str):
        self.session_service = session_service
        self.app_name = app_name
        
        # Initialize core services
        self.session_manager = SessionManager(session_service)
        self.runner_pool = RunnerPool(session_service, app_name)
        
        # Create agents
        self.weather_agent = create_weather_agent()
        self.time_agent = create_time_agent()
        self.broker_agent = create_broker_agent()
        self.root_agent = create_root_agent()
        
        # Register sub-agents in runner pool
        self.runner_pool.register_agent(self.weather_agent)
        self.runner_pool.register_agent(self.time_agent)
        self.runner_pool.register_agent(self.broker_agent)
        
        # Create root runner (for conversation tracking)
        self.root_runner = Runner(
            agent=self.root_agent,
            app_name=app_name,
            session_service=session_service
        )
        
        # Initialize routing
        self.a2a_service = A2AService(self.runner_pool)
        self.intent_classifier = IntentClassifier()
        self.query_router = QueryRouter(
            a2a_service=self.a2a_service,
            session_manager=self.session_manager,
            intent_classifier=self.intent_classifier
        )


def build_agent_team(session_service: InMemorySessionService, app_name: str) -> AgentTeam:
    """Build and return configured agent team."""
    return AgentTeam(session_service, app_name)
