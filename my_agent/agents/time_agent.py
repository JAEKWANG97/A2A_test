from google.adk.agents import Agent
from ..tools import get_current_time
from ..config import get_settings


def create_time_agent() -> Agent:
    """Create time agent instance."""
    settings = get_settings()
    return Agent(
        name="time_agent",
        model=settings.model_name,
        description="Provides current time for cities.",
        instruction="Use the 'get_current_time' tool to answer city time queries.",
        tools=[get_current_time],
    )
