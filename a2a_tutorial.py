"""A2A (Agent-to-Agent) Communication System Tutorial

This demonstrates how multiple agents can communicate and coordinate
to answer complex queries using Google ADK.

"""

from my_agent import (
    root_agent,
    time_agent,
    weather_agent,
    broker_agent,
    AGENT_REGISTRY,
)

def demonstrate_a2a_communication():
    """Demonstrate agent-to-agent communication."""
    print("=" * 60)
    print("A2A (Agent-to-Agent) Communication System Demo")
    print("=" * 60)
    
    # Scenario 1: Time Agent responds
    print("\n[Scenario 1] User asks: What's the time in Seoul?")
    print("-" * 60)
    print("Root Agent → Time Agent: Get current time in Seoul")
    time_response = time_agent.generate_content(
        "What is the current time in Seoul?"
    )
    print(f"Time Agent Response: {time_response}")
    
    # Scenario 2: Weather Agent responds
    print("\n[Scenario 2] User asks: How's the weather in New York?")
    print("-" * 60)
    print("Root Agent → Weather Agent: Get weather in New York")
    weather_response = weather_agent.generate_content(
        "What's the current weather in New York?"
    )
    print(f"Weather Agent Response: {weather_response}")
    
    # Scenario 3: Broker Agent coordinates
    print("\n[Scenario 3] Complex Query: Tell me about Tokyo (time & weather)")
    print("-" * 60)
    print("Root Agent → Broker Agent: Coordinate information")
    print("Broker Agent → Time Agent: Get Tokyo time")
    print("Broker Agent → Weather Agent: Get Tokyo weather")
    broker_response = broker_agent.generate_content(
        "Provide me with time and weather information about Tokyo by coordinating with other agents."
    )
    print(f"Broker Agent Response: {broker_response}")
    
    # Scenario 4: Agent Registry
    print("\n[Scenario 4] Available Agents in Registry:")
    print("-" * 60)
    for agent_name, agent_obj in AGENT_REGISTRY.items():
        print(f"  • {agent_name}: {agent_obj.description}")
    
    # Scenario 5: Multi-agent coordination
    print("\n[Scenario 5] Comprehensive World Tour Information")
    print("-" * 60)
    print("Root Agent orchestrating information from multiple sources...")
    comprehensive = root_agent.generate_content(
        "I need comprehensive information about Seoul and London. "
        "Please coordinate with time_agent and weather_agent to get both "
        "current time and weather for these cities."
    )
    print(f"Root Agent Final Response: {comprehensive}")

def show_agent_details():
    """Display detailed information about each agent."""
    print("\n" + "=" * 60)
    print("Agent Details")
    print("=" * 60)
    
    agents = [
        ("Time Agent", time_agent),
        ("Weather Agent", weather_agent),
        ("Broker Agent", broker_agent),
        ("Root Agent", root_agent),
    ]
    
    for agent_name, agent in agents:
        print(f"\n[{agent_name}]")
        print(f"  Name: {agent.name}")
        print(f"  Model: {agent.model}")
        print(f"  Description: {agent.description}")
        print(f"  Available Tools: {len(agent.tools) if agent.tools else 0}")

if __name__ == "__main__":
    # Show agent information
    show_agent_details()
    
    # Run A2A communication demo
    print("\n" + "=" * 60)
    print("Starting A2A Communication Demo...")
    print("=" * 60)
    demonstrate_a2a_communication()
    
    print("\n" + "=" * 60)
    print("Demo Complete!")
    print("=" * 60)