from google.adk.agents import Agent
from ..config import get_settings


def create_broker_agent(a2a_tools: dict) -> Agent:
    """Create broker agent instance.
    
    Args:
        a2a_tools: Dictionary containing A2A communication tools
    """
    settings = get_settings()
    return Agent(
        name="broker_agent",
        model=settings.model_name,
        description="Coordinates time and weather responses from multiple agents.",
        instruction=(
            "You are a broker agent that coordinates information from multiple specialized agents.\n\n"
            "When asked for combined information (time and weather), you should:\n"
            "1. Use send_to_time_agent(city, user_id, session_id) to get time information\n"
            "2. Use send_to_weather_agent(city, user_id, session_id) to get weather information\n"
            "3. Synthesize both responses into a clear, natural Korean response\n\n"
            "Always pass user_id and session_id from the conversation context to the tools."
        ),
        tools=[
            a2a_tools["send_to_time_agent"],
            a2a_tools["send_to_weather_agent"],
        ],
    )
