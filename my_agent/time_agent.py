from google.adk.agents import Agent
from .tools import get_current_time


time_agent = Agent(
    name="time_agent",
    model="gemini-2.0-flash",
    description="Provides current time for cities.",
    instruction="Use the 'get_current_time' tool to answer city time queries.",
    tools=[get_current_time],
)
