"""
User models and schemas for the Hobbyist AI application
"""

from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

# User models
class User(BaseModel):
    email: str
    name: str
    interests: list[str]
    mbti_type: Optional[str] = None
    preferences: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "name": "Jane Doe",
                "interests": ["cooking", "gardening", "reading"],
                "mbti_type": "INFJ",
                "preferences": {
                    "budget": "medium",
                    "time_commitment": "flexible",
                    "group_preference": "solo"
                }
            }
        }

class HobbyProfile(BaseModel):
    user_email: str
    personality_traits: Dict[str, Any] = Field(default_factory=dict)
    hobby_categories: List[str]
    activity_preferences: Dict[str, Any]
    mbti_personality_type: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_email": "user@example.com",
                "personality_traits": {
                    "exploratory": 0.8,
                    "creative": 0.9,
                    "outdoor": 0.6
                },
                "hobby_categories": ["artistic", "intellectual", "physical"],
                "activity_preferences": {
                    "indoor": True,
                    "outdoor": False,
                    "social": True
                },
                "mbti_personality_type": "INTJ"
            }
        }
    
    @classmethod
    def from_user(cls, user: User) -> "HobbyProfile":
        """Create a hobby profile from a user"""
        return cls(
            user_email=user.email,
            hobby_categories=user.interests.upper(),
            activity_preferences=user.preferences,
            mbti_personality_type=user.mbti_type
        )


class RecommendationRequest(BaseModel):
    user_email: str
    hobby_profile: Optional[HobbyProfile] = None
    request_timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_email": "user@example.com",
                "hobby_profile": {
                    "user_email": "user@example.com",
                    "personality_traits": {
                        "exploratory": 0.8,
                        "creative": 0.9,
                        "outdoor": 0.6
                    },
                    "hobby_categories": ["artistic", "intellectual", "physical"],
                    "activity_preferences": {
                        "indoor": True,
                        "outdoor": False,
                        "social": True
                    },
                    "mbti_personality_type": "INTJ"
                },
                "request_timestamp": "2024-01-01T00:00:00Z"
            }
        }