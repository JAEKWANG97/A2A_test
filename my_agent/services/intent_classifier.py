from enum import Enum
from typing import Optional, Tuple
from ..config import get_settings


class Intent(Enum):
    """User intent types."""
    WEATHER = "weather"
    TIME = "time"
    COMBINED = "combined"  # time + weather
    SET_NAME = "set_name"
    SET_UNITS = "set_units"
    UNKNOWN = "unknown"


class IntentClassifier:
    """Classifies user intent from query."""
    
    def __init__(self):
        self.settings = get_settings()
    
    def classify(self, query: str) -> Tuple[Intent, Optional[str]]:
        """Classify query and extract entity (e.g., city).
        
        Returns:
            (intent, entity) tuple
        """
        q = query.lower()
        
        # Preference settings
        if q.startswith("my name is ") or q.startswith("내 이름은 "):
            name = query.split()[-1]
            return (Intent.SET_NAME, name)
        
        if "단위" in q:
            if "f" in q or "화씨" in q:
                return (Intent.SET_UNITS, "F")
            elif "c" in q or "섭씨" in q:
                return (Intent.SET_UNITS, "C")
        
        # Extract city
        city = self._extract_city(q)
        
        # Check for combined query
        has_time = ("시간" in q) or ("time" in q)
        has_weather = ("날씨" in q) or ("weather" in q)
        
        if has_time and has_weather:
            return (Intent.COMBINED, city)
        elif has_weather:
            return (Intent.WEATHER, city)
        elif has_time:
            return (Intent.TIME, city)
        
        return (Intent.UNKNOWN, None)
    
    def _extract_city(self, query: str) -> Optional[str]:
        """Extract city name from query."""
        query_lower = query.lower()
        
        # Map Korean city names to English
        city_map = {
            "서울": "Seoul",
            "도쿄": "Tokyo",
            "런던": "London",
            "뉴욕": "New York",
        }
        
        # Check Korean names first
        for kr_name, en_name in city_map.items():
            if kr_name in query:
                return en_name
        
        # Check English names
        for city in self.settings.supported_cities:
            if city.lower() in query_lower:
                return city
        
        return None
