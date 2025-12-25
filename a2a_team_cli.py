import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

import asyncio
from google.genai import types
from google.adk.sessions import InMemorySessionService
from my_agent.team import build_agent_team
from my_agent.config import get_settings


APP_NAME = "a2a_team_app"
USER_ID = "user_1"
SESSION_ID = "sess_001"


async def talk_to_agent(team, user_text: str):
    """Send user message directly to root agent and get response."""
    content = types.Content(role="user", parts=[types.Part(text=user_text)])
    
    response_texts = []
    async for event in team.root_runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=content
    ):
        # Collect text parts from response
        if hasattr(event, 'candidate') and event.candidate:
            if hasattr(event.candidate, 'content') and event.candidate.content:
                for part in event.candidate.content.parts:
                    if hasattr(part, 'text') and part.text:
                        response_texts.append(part.text)
    
    # Combine and display response
    answer = ''.join(response_texts).strip()
    if answer:
        print(f">>> {user_text}\n<<< {answer}\n")
    else:
        print(f">>> {user_text}\n<<< (응답 없음)\n")


async def main():
    """Main CLI loop."""
    # Validate settings
    try:
        settings = get_settings()
        print(f"✓ API Key: {settings.google_api_key[:20]}...")
        print(f"✓ Model: {settings.model_name}")
        print(f"✓ Use Vertex AI: {settings.google_genai_use_vertexai}\n")
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("\nPlease set GOOGLE_API_KEY in .env file or environment variables.")
        return
    
    # Initialize session service and team
    session_service = InMemorySessionService()
    team = build_agent_team(session_service, APP_NAME)
    
    # Create session
    await team.session_manager.ensure_session(APP_NAME, USER_ID, SESSION_ID)
    print(f"✓ Session created: {APP_NAME}/{USER_ID}/{SESSION_ID}\n")
    
    print("=" * 60)
    print("A2A (Agent-to-Agent) Communication System")
    print("=" * 60)
    print("\n사용 가능한 명령:")
    print("  - '서울 날씨' / '도쿄 시간' / '런던 시간과 날씨'")
    print("  - '내 이름은 <이름>' - 이름 설정")
    print("  - '단위를 섭씨로' / '단위를 화씨로' - 온도 단위 설정")
    print("  - 'exit' / 'quit' - 종료\n")
    
    # Interactive loop
    while True:
        try:
            text = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n종료합니다.")
            break
        
        if not text:
            continue
        
        if text.lower() in {"exit", "quit", "종료"}:
            print("종료합니다.")
            break
        
        await talk_to_agent(team, text)


if __name__ == "__main__":
    asyncio.run(main())
