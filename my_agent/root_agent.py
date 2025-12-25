from google.adk.agents import Agent
from .router import send_message_to_agent


root_agent = Agent(
    name="root_agent",
    model="gemini-2.0-flash",
    description="Orchestrates user requests and delegates to sub-agents.",
    instruction=(
        "Understand user intent and delegate: time queries → time_agent, weather queries → weather_agent, "
        "combined → broker_agent. Use session preferences when responding."
    ),
    tools=[send_message_to_agent],
)
