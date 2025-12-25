from typing import Dict
from google.adk.agents import Agent
from .weather_agent import weather_agent
from .time_agent import time_agent
from .broker_agent import broker_agent


AGENT_REGISTRY: Dict[str, Agent] = {
    "weather_agent": weather_agent,
    "time_agent": time_agent,
    "broker_agent": broker_agent,
}
