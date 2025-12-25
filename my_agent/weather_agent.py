from google.adk.agents import Agent
from .tools import get_weather


weather_agent = Agent(
    name="weather_agent",
    model="gemini-2.0-flash",
    description="Provides weather information for cities.",
    instruction=(
        "Use the 'get_weather' tool. If city is omitted, default to the user's home city. "
        "Respect preferred units (C/F)."
    ),
    tools=[get_weather],
)
