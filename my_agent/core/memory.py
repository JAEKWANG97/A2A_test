from dataclasses import dataclass, asdict
from typing import Dict


@dataclass
class UserMemory:
    """User preferences and personalization data."""
    
    user_name: str = "User"
    home_city: str = "Seoul"
    preferred_units: str = "C"  # "C" or "F"
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> "UserMemory":
        """Create from dictionary."""
        return cls(**data)
    
    def update(self, **kwargs) -> None:
        """Update memory fields."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def get_context_prefix(self) -> str:
        """Generate context prefix for agent messages."""
        return f"(User:{self.user_name}, Home:{self.home_city}, Units:{self.preferred_units}) "
