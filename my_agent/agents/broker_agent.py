from google.adk.agents import Agent
from ..config import get_settings


def create_broker_agent() -> Agent:
    """Create broker agent instance."""
    settings = get_settings()
    return Agent(
        name="broker_agent",
        model=settings.model_name,
        description="Coordinates time and weather responses from multiple agents.",
        instruction=(
            "You coordinate information from time_agent and weather_agent. "
            "When asked for combined information, synthesize responses clearly."
        ),
        tools=[],
    )
