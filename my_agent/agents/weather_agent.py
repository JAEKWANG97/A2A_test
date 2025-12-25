from google.adk.agents import Agent
from ..tools import get_weather
from ..config import get_settings


def create_weather_agent() -> Agent:
    """Create weather agent instance."""
    settings = get_settings()
    return Agent(
        name="weather_agent",
        model=settings.model_name,
        description="Provides weather information for cities.",
        instruction=(
            "Use the 'get_weather' tool to fetch weather data. "
            "If city is omitted, default to the user's home city. "
            "Respect preferred units (C/F) from context."
        ),
        tools=[get_weather],
    )
