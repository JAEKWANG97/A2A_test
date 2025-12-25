from .intent_classifier import IntentClassifier, Intent
from .a2a_service import A2AService
from ..core.session_manager import SessionManager


class QueryRouter:
    """Routes user queries to appropriate agents."""
    
    def __init__(
        self,
        a2a_service: A2AService,
        session_manager: SessionManager,
        intent_classifier: IntentClassifier
    ):
        self.a2a_service = a2a_service
        self.session_manager = session_manager
        self.intent_classifier = intent_classifier
    
    async def route(self, query: str, user_id: str, session_id: str) -> str:
        """Route query to appropriate handler.
        
        Args:
            query: User query
            user_id: User ID
            session_id: Session ID
        
        Returns:
            Response text
        """
        intent, entity = self.intent_classifier.classify(query)
        memory = self.session_manager.get_memory(user_id, session_id)
        
        # Handle preference updates
        if intent == Intent.SET_NAME:
            self.session_manager.update_memory(user_id, session_id, user_name=entity)
            return f"알겠습니다, {entity}님."
        
        if intent == Intent.SET_UNITS:
            self.session_manager.update_memory(user_id, session_id, preferred_units=entity)
            unit_name = "화씨(°F)" if entity == "F" else "섭씨(°C)"
            return f"단위를 {unit_name}로 설정했습니다."
        
        # Default to home city if no city specified
        city = entity or memory.home_city
        context = memory.get_context_prefix()
        
        # Route to agents
        try:
            if intent == Intent.WEATHER:
                return await self.a2a_service.send_to_agent(
                    agent_name="weather_agent",
                    message=f"Provide weather for {city} in {memory.preferred_units}. Use get_weather tool.",
                    user_id=user_id,
                    session_id=session_id,
                    context_prefix=context
                )
            
            elif intent == Intent.TIME:
                return await self.a2a_service.send_to_agent(
                    agent_name="time_agent",
                    message=f"Provide current time in {city}. Use get_current_time tool.",
                    user_id=user_id,
                    session_id=session_id,
                    context_prefix=context
                )
            
            elif intent == Intent.COMBINED:
                return await self.a2a_service.send_to_agent(
                    agent_name="broker_agent",
                    message=f"Coordinate time and weather information for {city}.",
                    user_id=user_id,
                    session_id=session_id,
                    context_prefix=context
                )
            
            else:
                return "원하시는 정보를 알려주세요 (예: '서울 날씨', '도쿄 시간', '런던 시간과 날씨')."
        
        except Exception as e:
            return f"오류가 발생했습니다: {str(e)}"
