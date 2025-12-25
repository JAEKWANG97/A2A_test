# A2A (Agent-to-Agent) Communication System

Google ADK 기반의 다중 에이전트 통신 시스템입니다. 에이전트끼리 협력하여 사용자 질의에 응답합니다.

## 🚀 빠른 시작

### 1. 환경 설정

```bash
# 가상환경 생성 및 활성화
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# 의존성 설치
pip install google-adk python-dotenv
```

### 2. API 키 설정

`.env` 파일 생성:
```bash
cp .env.example .env
```

`.env` 파일에 API 키 입력:
```
GOOGLE_API_KEY=your_actual_api_key_here
GOOGLE_GENAI_USE_VERTEXAI=False
```

### 3. 실행

```bash
python a2a_team_cli.py
```

## 💬 사용 예시

```
You: 서울 날씨
<<< 서울의 날씨는 흐림이며, 기온은 5°C입니다.

You: 내 이름은 JK
<<< 알겠습니다, JK님.

You: 단위를 화씨로 바꿔줘
<<< 단위를 화씨(°F)로 설정했습니다.

You: 도쿄 시간
<<< 도쿄의 현재 시간은 오전 4시 30분입니다.

You: 런던 시간과 날씨
<<< 런던의 현재 시간은 오후 11시 30분이며, 날씨는 비가 내리고 있고 기온은 46°F입니다.
```

## 🏗️ 아키텍처

```
my_agent/
├── agents/          # 에이전트 정의
│   ├── weather_agent.py
│   ├── time_agent.py
│   ├── broker_agent.py
│   └── root_agent.py
├── core/            # 핵심 추상화
│   ├── memory.py         # 사용자 메모리
│   ├── session_manager.py # 세션 관리
│   └── exceptions.py     # 커스텀 예외
├── services/        # 비즈니스 로직
│   ├── runner_pool.py      # Runner 풀
│   ├── a2a_service.py      # A2A 통신
│   ├── intent_classifier.py # 의도 분류
│   └── query_router.py     # 쿼리 라우팅
├── config/          # 설정 관리
│   └── settings.py
├── tools.py         # 도구 함수
└── team.py          # 팀 구성
```

### A2A 흐름

```
사용자 입력: "서울 날씨"
    ↓
[CLI] talk_to_agent()
    ↓
[Root Runner] 대화 기록
    ↓
[QueryRouter] route() - 의도 파악
    ↓
[IntentClassifier] classify() → Intent.WEATHER, "Seoul"
    ↓
[SessionManager] get_memory() → Units: C, Home: Seoul
    ↓
[A2AService] send_to_agent("weather_agent", ...)
    ↓
[RunnerPool] get_runner("weather_agent")
    ↓
[Weather Agent Runner] run_async()
    ↓
[Weather Agent] LLM 추론 → 도구 호출 결정
    ↓
[Tool] get_weather("Seoul", "C")
    ↓
[Weather Agent] 응답 생성
    ↓
[CLI] 최종 출력
```

## 🎯 주요 기능

- ✅ **실제 A2A 통신**: `Runner.run_async()`를 통한 에이전트 간 실제 통신
- ✅ **세션 메모리**: 사용자 이름, 홈 도시, 단위 설정 저장
- ✅ **의도 기반 라우팅**: 자연어 쿼리에서 의도와 엔티티 추출
- ✅ **다중 에이전트 조정**: Root → Weather/Time/Broker 에이전트 위임
- ✅ **도구 사용**: LLM이 적절한 도구를 자동 호출
- ✅ **설정 관리**: 환경변수 기반 설정, 검증 포함

## 📝 지원 명령

- **날씨 조회**: "서울 날씨", "Tokyo weather"
- **시간 조회**: "도쿄 시간", "London time"
- **복합 조회**: "런던 시간과 날씨"
- **이름 설정**: "내 이름은 JK", "My name is JK"
- **단위 설정**: "단위를 섭씨로", "단위를 화씨로"

## 🔧 확장

새 에이전트 추가:
1. `my_agent/agents/your_agent.py` 생성
2. `my_agent/tools.py`에 도구 함수 추가
3. `my_agent/team.py`에서 에이전트 등록
4. `my_agent/services/intent_classifier.py`에 새 Intent 추가
5. `my_agent/services/query_router.py`에 라우팅 로직 추가

## 📄 라이선스

MIT
