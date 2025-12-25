from google.adk.agents import Agent


broker_agent = Agent(
    name="broker_agent",
    model="gemini-2.0-flash",
    description="Coordinates time and weather responses.",
    instruction=(
        "Coordinate with time_agent and weather_agent to synthesize combined answers."
    ),
    tools=[],
)
