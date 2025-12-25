from typing import Dict, Tuple
from google.adk.sessions import InMemorySessionService
from .memory import UserMemory
from ..config import get_settings


class SessionManager:
    """Manages user sessions and memory."""
    
    def __init__(self, session_service: InMemorySessionService):
        self.session_service = session_service
        self._memory_store: Dict[Tuple[str, str], UserMemory] = {}
        self.settings = get_settings()
    
    async def ensure_session(self, app_name: str, user_id: str, session_id: str) -> None:
        """Create session if it doesn't exist."""
        await self.session_service.create_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id
        )
        # Initialize memory with defaults
        if (user_id, session_id) not in self._memory_store:
            self._memory_store[(user_id, session_id)] = UserMemory(
                user_name=self.settings.default_user_name,
                home_city=self.settings.default_home_city,
                preferred_units=self.settings.default_units,
            )
    
    def get_memory(self, user_id: str, session_id: str) -> UserMemory:
        """Get user memory for session."""
        key = (user_id, session_id)
        if key not in self._memory_store:
            self._memory_store[key] = UserMemory(
                user_name=self.settings.default_user_name,
                home_city=self.settings.default_home_city,
                preferred_units=self.settings.default_units,
            )
        return self._memory_store[key]
    
    def update_memory(self, user_id: str, session_id: str, **updates) -> None:
        """Update user memory."""
        memory = self.get_memory(user_id, session_id)
        memory.update(**updates)
