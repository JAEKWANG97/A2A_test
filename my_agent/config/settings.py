import os
from typing import List, Optional
from dataclasses import dataclass, field


@dataclass
class Settings:
    """Application settings loaded from environment variables."""
    
    # API Configuration
    google_api_key: str = field(default_factory=lambda: os.getenv("GOOGLE_API_KEY", ""))
    google_genai_use_vertexai: str = field(default_factory=lambda: os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "False"))
    
    # Model Configuration
    model_name: str = "gemini-2.0-flash"
    
    # App Configuration
    app_name: str = "a2a_team_app"
    
    # Supported Cities
    supported_cities: List[str] = field(default_factory=lambda: [
        "Seoul", "New York", "London", "Tokyo"
    ])
    
    # Default User Preferences
    default_user_name: str = "User"
    default_home_city: str = "Seoul"
    default_units: str = "C"
    
    def validate(self) -> None:
        """Validate required settings."""
        if not self.google_api_key:
            raise ValueError(
                "GOOGLE_API_KEY is required. Please set it in .env file or environment variables."
            )
    
    def __post_init__(self):
        """Auto-validate after initialization."""
        self.validate()


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get or create global settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
