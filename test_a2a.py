import os
from dotenv import load_dotenv
load_dotenv()

import asyncio
from google.genai import types
from google.adk.sessions import InMemorySessionService
from my_agent.team import build_agent_team

APP_NAME = "test_app"
USER_ID = "test_user"
SESSION_ID = "test_session"


async def test_a2a():
    """Test true A2A architecture."""
    print("=" * 60)
    print("Testing True Agent-to-Agent Communication")
    print("=" * 60)
    
    # Initialize
    session_service = InMemorySessionService()
    team = build_agent_team(session_service, APP_NAME)
    await team.session_manager.ensure_session(APP_NAME, USER_ID, SESSION_ID)
    print("✓ Session created\n")
    
    # Test queries
    test_queries = [
        "서울 날씨",
        "도쿄 시간",
        "런던 시간과 날씨",
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print('='*60)
        
        content = types.Content(role="user", parts=[types.Part(text=query)])
        
        response_texts = []
        async for event in team.root_runner.run_async(
            user_id=USER_ID,
            session_id=SESSION_ID,
            new_message=content
        ):
            # Collect text parts
            if hasattr(event, 'candidate') and event.candidate:
                if hasattr(event.candidate, 'content') and event.candidate.content:
                    for part in event.candidate.content.parts:
                        if hasattr(part, 'text') and part.text:
                            response_texts.append(part.text)
        
        answer = ''.join(response_texts).strip()
        print(f"\nResponse: {answer}\n")
    
    print("\n" + "="*60)
    print("✓ All tests completed!")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(test_a2a())
