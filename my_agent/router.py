from typing import Dict, Tuple
from google.genai import types
from .registry import AGENT_REGISTRY


SESSION_MEMORY: Dict[Tuple[str, str], Dict] = {}


def get_memory(user_id: str, session_id: str) -> Dict:
    key = (user_id, session_id)
    if key not in SESSION_MEMORY:
        SESSION_MEMORY[key] = {
            "user_name": "JK",
            "home_city": "Seoul",
            "preferred_units": "C",
        }
    return SESSION_MEMORY[key]


def set_memory(user_id: str, session_id: str, updates: Dict) -> None:
    mem = get_memory(user_id, session_id)
    mem.update(updates)


def send_message_to_agent(target_agent: str, message: str, user_id: str, session_id: str) -> Dict:
    if target_agent not in AGENT_REGISTRY:
        return {"status": "error", "error_message": f"Agent '{target_agent}' not found."}
    mem = get_memory(user_id, session_id)
    prefix = (
        f"(User:{mem['user_name']}, Home:{mem['home_city']}, Units:{mem['preferred_units']}) "
    )
    try:
        response = AGENT_REGISTRY[target_agent].generate_content(prefix + message)
        return {"status": "success", "response": str(response)}
    except Exception as e:
        return {"status": "error", "error_message": str(e)}


def route_query_sync(query: str, user_id: str, session_id: str) -> str:
    q = query.lower()
    mem = get_memory(user_id, session_id)

    if q.startswith("my name is ") or q.startswith("내 이름은 "):
        name = query.split()[-1]
        set_memory(user_id, session_id, {"user_name": name})
        return f"알겠습니다, {name}님."

    if "단위" in q and ("f" in q or "화씨" in q):
        set_memory(user_id, session_id, {"preferred_units": "F"})
        return "단위를 화씨(°F)로 설정했습니다."
    if "단위" in q and ("c" in q or "섭씨" in q):
        set_memory(user_id, session_id, {"preferred_units": "C"})
        return "단위를 섭씨(°C)로 설정했습니다."

    if ("날씨" in q) or ("weather" in q):
        city = None
        for c in ["seoul", "tokyo", "london", "new york"]:
            if c in q:
                city = c.title() if c != "new york" else "New York"
                break
        city = city or mem["home_city"]
        result = send_message_to_agent(
            target_agent="weather_agent",
            message=f"Provide weather for {city} in {mem['preferred_units']}. Use get_weather.",
            user_id=user_id,
            session_id=session_id,
        )
        return result.get("response") or f"Error: {result['error_message']}"

    if ("시간" in q) or ("time" in q):
        city = None
        for c in ["seoul", "tokyo", "london", "new york"]:
            if c in q:
                city = c.title() if c != "new york" else "New York"
                break
        city = city or mem["home_city"]
        result = send_message_to_agent(
            target_agent="time_agent",
            message=f"Provide current time in {city} using get_current_time.",
            user_id=user_id,
            session_id=session_id,
        )
        return result.get("response") or f"Error: {result['error_message']}"

    if ("시간" in q and "날씨" in q) or ("time" in q and "weather" in q):
        city = None
        for c in ["seoul", "tokyo", "london", "new york"]:
            if c in q:
                city = c.title() if c != "new york" else "New York"
                break
        city = city or mem["home_city"]
        result = send_message_to_agent(
            target_agent="broker_agent",
            message=(
                f"Coordinate time + weather for {city}. Ask time_agent and weather_agent, then summarize."
            ),
            user_id=user_id,
            session_id=session_id,
        )
        return result.get("response") or f"Error: {result['error_message']}"

    return "원하시는 정보를 알려주세요 (예: '서울 날씨', '도쿄 시간')."
