# A2A System - 간단한 시작 가이드

이 프로젝트는 Google ADK를 사용한 Agent-to-Agent (A2A) 통신 시스템입니다.

## 🎯 핵심 파일

### 필수 파일
- `a2a_team_cli.py` - 실행 파일 (여기서 시작!)
- `my_agent/agents/` - 에이전트 정의
- `my_agent/tools.py` - 도구 함수
- `my_agent/team.py` - 팀 구성

### 헬퍼 파일
- `my_agent/services/` - A2A 통신, 라우팅
- `my_agent/core/` - 세션, 메모리 관리
- `my_agent/config/` - 설정

## 🚀 3단계로 시작하기

### 1. 설치
```bash
pip install google-adk python-dotenv
```

### 2. API 키 설정
`.env` 파일에:
```
GOOGLE_API_KEY=your_key_here
```

### 3. 실행
```bash
python a2a_team_cli.py
```

## 💡 코드 읽는 순서

초보자라면 이 순서로 읽으세요:

1. `a2a_team_cli.py` - 시작점, 전체 흐름 파악
2. `my_agent/team.py` - 팀이 어떻게 구성되는지
3. `my_agent/agents/weather_agent.py` - 에이전트 예제
4. `my_agent/tools.py` - 도구 함수 예제
5. `my_agent/services/query_router.py` - 라우팅 로직

자세한 내용은 `README.md`를 참고하세요!
