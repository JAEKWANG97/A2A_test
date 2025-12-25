from google.adk.agents import Agent
from ..config import get_settings


def create_root_agent(a2a_tools: dict) -> Agent:
    """Create root orchestrator agent instance.
    
    Args:
        a2a_tools: Dictionary containing A2A communication tools
    """
    settings = get_settings()
    return Agent(
        name="root_agent",
        model=settings.model_name,
        description="Main orchestrator that coordinates user requests and delegates to specialized agents.",
        instruction=(
            "You are the root orchestrator agent. Your role is to:\n\n"
            "1. Understand user queries and identify their intent\n"
            "2. Use the appropriate tools to delegate work to specialized agents:\n"
            "   - send_to_weather_agent(city, user_id, session_id): Get weather information\n"
            "   - send_to_time_agent(city, user_id, session_id): Get time information\n"
            "   - send_to_broker_agent(city, user_id, session_id): Get combined time+weather\n"
            "   - update_user_name(name, user_id, session_id): Update user's name preference\n"
            "   - update_preferred_units(units, user_id, session_id): Update temperature units (C or F)\n\n"
            "3. Default city is 'Seoul' if not specified by user\n"
            "4. Always pass user_id and session_id from the conversation context\n"
            "5. Respond naturally in Korean, presenting agent responses to the user\n\n"
            "Examples:\n"
            "- User: '서울 날씨' → Use send_to_weather_agent('Seoul', user_id, session_id)\n"
            "- User: '도쿄 시간' → Use send_to_time_agent('Tokyo', user_id, session_id)\n"
            "- User: '런던 시간과 날씨' → Use send_to_broker_agent('London', user_id, session_id)\n"
            "- User: '내 이름은 홍길동' → Use update_user_name('홍길동', user_id, session_id)\n"
            "- User: '단위를 화씨로' → Use update_preferred_units('F', user_id, session_id)"
        ),
        tools=[
            a2a_tools["send_to_weather_agent"],
            a2a_tools["send_to_time_agent"],
            a2a_tools["send_to_broker_agent"],
            a2a_tools["update_user_name"],
            a2a_tools["update_preferred_units"],
        ],
    )
