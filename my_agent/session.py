from google.adk.sessions import InMemorySessionService


async def ensure_session(session_service: InMemorySessionService, app_name: str, user_id: str, session_id: str) -> None:
    await session_service.create_session(app_name=app_name, user_id=user_id, session_id=session_id)
