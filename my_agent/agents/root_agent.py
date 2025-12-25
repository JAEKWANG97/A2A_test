from google.adk.agents import Agent
from ..config import get_settings


def create_root_agent() -> Agent:
    """Create root orchestrator agent instance."""
    settings = get_settings()
    return Agent(
        name="root_agent",
        model=settings.model_name,
        description="Main orchestrator that coordinates user requests.",
        instruction=(
            "You are the main orchestrator. Understand user intent and maintain conversation context. "
            "Delegate to appropriate sub-agents as needed."
        ),
        tools=[],
    )
