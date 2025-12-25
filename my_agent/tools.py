from typing import Dict


def get_current_time(city: str) -> Dict[str, str]:
    cities_time = {
        "Seoul": "10:30 AM",
        "New York": "6:30 PM",
        "London": "11:30 PM",
        "Tokyo": "4:30 AM",
    }
    time = cities_time.get(city, "Unknown")
    return {"status": "success", "city": city, "time": time}


def get_weather(city: str, units: str = "C") -> Dict[str, str]:
    data_c = {
        "Seoul": 5,
        "New York": 15,
        "London": 8,
        "Tokyo": 3,
    }
    desc = {
        "Seoul": "Cloudy",
        "New York": "Sunny",
        "London": "Rainy",
        "Tokyo": "Clear",
    }
    if city not in data_c:
        return {"status": "error", "error_message": f"No weather for '{city}'."}
    temp_c = data_c[city]
    if units.upper() == "F":
        temp = round((temp_c * 9 / 5) + 32)
        unit = "°F"
    else:
        temp = temp_c
        unit = "°C"
    return {"status": "success", "city": city, "weather": f"{desc[city]}, {temp}{unit}"}


# ============================================================
# Agent-to-Agent Communication Tools
# ============================================================

def create_a2a_tools(a2a_service, session_manager):
    """Create A2A communication tool functions.
    
    These tools allow agents to communicate with each other.
    Each tool is a closure that captures the service dependencies.
    """
    
    async def send_to_weather_agent(city: str, user_id: str, session_id: str) -> str:
        """Send request to weather agent.
        
        Args:
            city: City name to get weather for
            user_id: User ID for session context
            session_id: Session ID for session context
            
        Returns:
            Weather information from weather agent
        """
        memory = session_manager.get_memory(user_id, session_id)
        context = memory.get_context_prefix()
        return await a2a_service.send_to_agent(
            agent_name="weather_agent",
            message=f"Provide weather for {city} in {memory.preferred_units}. Use get_weather tool.",
            user_id=user_id,
            session_id=session_id,
            context_prefix=context
        )
    
    async def send_to_time_agent(city: str, user_id: str, session_id: str) -> str:
        """Send request to time agent.
        
        Args:
            city: City name to get time for
            user_id: User ID for session context
            session_id: Session ID for session context
            
        Returns:
            Time information from time agent
        """
        memory = session_manager.get_memory(user_id, session_id)
        context = memory.get_context_prefix()
        return await a2a_service.send_to_agent(
            agent_name="time_agent",
            message=f"Provide current time in {city}. Use get_current_time tool.",
            user_id=user_id,
            session_id=session_id,
            context_prefix=context
        )
    
    async def send_to_broker_agent(city: str, user_id: str, session_id: str) -> str:
        """Send request to broker agent for combined information.
        
        Args:
            city: City name to get combined time and weather for
            user_id: User ID for session context
            session_id: Session ID for session context
            
        Returns:
            Combined time and weather information from broker agent
        """
        memory = session_manager.get_memory(user_id, session_id)
        context = memory.get_context_prefix()
        return await a2a_service.send_to_agent(
            agent_name="broker_agent",
            message=f"Coordinate time and weather information for {city}.",
            user_id=user_id,
            session_id=session_id,
            context_prefix=context
        )
    
    def update_user_name(name: str, user_id: str, session_id: str) -> str:
        """Update user's name preference.
        
        Args:
            name: User's name
            user_id: User ID
            session_id: Session ID
            
        Returns:
            Confirmation message
        """
        session_manager.update_memory(user_id, session_id, user_name=name)
        return f"알겠습니다, {name}님."
    
    def update_preferred_units(units: str, user_id: str, session_id: str) -> str:
        """Update user's preferred temperature units.
        
        Args:
            units: 'C' for Celsius or 'F' for Fahrenheit
            user_id: User ID
            session_id: Session ID
            
        Returns:
            Confirmation message
        """
        unit_char = units.upper()[0] if units else "C"
        session_manager.update_memory(user_id, session_id, preferred_units=unit_char)
        unit_name = "화씨(°F)" if unit_char == "F" else "섭씨(°C)"
        return f"단위를 {unit_name}로 설정했습니다."
    
    return {
        "send_to_weather_agent": send_to_weather_agent,
        "send_to_time_agent": send_to_time_agent,
        "send_to_broker_agent": send_to_broker_agent,
        "update_user_name": update_user_name,
        "update_preferred_units": update_preferred_units,
    }
