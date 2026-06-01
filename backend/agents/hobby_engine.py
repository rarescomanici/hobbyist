"""
Hobby recommendation engine with Strands Agents integration
"""

import sys
from pathlib import Path

# Add backend directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from typing import Dict, Any, Optional
from datetime import datetime, timedelta

# Import models
from models.user_models import User, HobbyProfile

class HobbyRecommendationEngine:
    """
    AI-powered hobby recommendation engine using Strands Agents framework
    
    This engine orchestrates multiple agents to:
    1. Analyze user interests, MBTI, and personality traits
    2. Fetch data from public event/activity APIs
    3. Generate personalized hobby recommendations
    4. Create structured weekly/monthly activity plans
    """
    
    def __init__(self, api_keys: Optional[Dict[str, str]] = None):
        """
        Initialize the recommendation engine
        
        Args:
            api_keys: Dictionary of API keys for external services
        """
        self.api_keys = api_keys or {}
        self.recommendations_history: Dict[str, list] = {}
        
    async def generate_hobby_plan(
        self,
        user_email: str,
        user_profile: User,
        days_ahead: int = 7
    ) -> list[Dict[str, Any]]:
        """
        Generate a personalized hobby plan using AI agents
        
        Args:
            user_email: User's email address
            user_profile: User profile with interests and preferences
            days_ahead: Number of days to plan ahead (default: 7)
            
        Returns:
            List of recommended activities with dates and details
        """
        # Initialize recommendations storage
        if user_email not in self.recommendations_history:
            self.recommendations_history[user_email] = []
        
        # Step 1: Analyze user personality and traits
        personality_analysis = await self._analyze_user(user_profile)
        
        # Step 2: Fetch available activities/events from APIs
        available_activities = await self._fetch_activities()
        
        # Step 3: Generate recommendations based on analysis
        recommendations = await self._generate_recommendations(
            user_profile=user_profile,
            personality_analysis=personality_analysis,
            available_activities=available_activities,
            days_ahead=days_ahead
        )
        
        # Store recommendations
        self.recommendations_history[user_email] = recommendations
        
        return recommendations
    
    async def _analyze_user(self, user_profile: User) -> Dict[str, Any]:
        """
        Analyze user's personality traits, interests, and MBTI type
        
        Args:
            user_profile: User profile data
            
        Returns:
            Dictionary with analysis results
        """
        # Extract personality indicators
        interests = user_profile.interests
        
        # Calculate trait scores based on interests
        trait_scores = {
            "creative": sum(1 for i in interests if any(
                keyword in i.lower() 
                for keyword in ["art", "music", "writing", "painting", "poetry"]
            )),
            "intellectual": sum(1 for i in interests if any(
                keyword in i.lower()
                for keyword in ["reading", "learning", "philosophy", "science"]
            )),
            "physical": sum(1 for i in interests if any(
                keyword in i.lower()
                for keyword in ["sports", "fitness", "dancing", "hiking", "cycling"]
            )),
            "social": sum(1 for i in interests if any(
                keyword in i.lower()
                for keyword in ["community", "group", "networking", "meeting"]
            )),
            "solitary": sum(1 for i in interests if any(
                keyword in i.lower()
                for keyword in ["meditation", "writing", "reading", "journaling"]
            ))
        }
        
        # Normalize scores to 0-1 range
        total = sum(trait_scores.values()) or 1
        trait_scores = {k: v / total for k, v in trait_scores.items()}
        
        # Analyze MBTI type if provided
        mbti_analysis = None
        mbti_type = user_profile.mbti_type
        
        if mbti_type:
            mbti_analysis = await self._analyze_mbti_type(mbti_type)
        
        return {
            "traits": trait_scores,
            "mbti_analysis": mbti_analysis,
            "primary_strengths": [
                k for k, v in sorted(trait_scores.items(), key=lambda x: x[1], reverse=True)[:2]
            ]
        }
    
    async def _analyze_mbti_type(self, mbti_type: str) -> Dict[str, Any]:
        """
        Analyze MBTI personality type
        
        Args:
            mbti_type: MBTI 4-letter code (e.g., "INTJ", "ENFP")
            
        Returns:
            Dictionary with MBTI analysis
        """
        analysis = {
            "introvert/extrovert": "introvert" if mbti_type[0] == "I" else "extravert",
            "sensing/intuition": "sensing" if mbti_type[1] == "S" else "intuition",
            "thinking/feeling": "thinking" if mbti_type[2] == "T" else "feeling",
            "judging/perceiving": "judging" if mbti_type[3] == "J" else "perceiving",
            "strengths": self._get_mbti_strengths(mbti_type)
        }
        
        return analysis
    
    def _get_mbti_strengths(self, mbti_type: str) -> list[str]:
        """
        Get strengths based on MBTI type
        
        Args:
            mbti_type: MBTI 4-letter code
            
        Returns:
            List of personality strengths
        """
        strengths_map = {
            "ISTJ": ["organized", "practical", "dependable", "analytical"],
            "ISFJ": ["caring", "protective", "conscientious", "loyal"],
            "INFJ": ["insightful", "empathetic", "creative", "visionary"],
            "INTJ": ["innovative", "strategic", "analytical", "independent"],
            "ISTP": ["practical", "resourceful", "analytical", "hands-on"],
            "ISFP": ["artist", "compassionate", "adventurous", "flexible"],
            "INFP": ["empathetic", "creative", "idealistic", "introspective"],
            "INTP": ["analytical", "curious", "innovative", "logical"],
            "ESTP": ["hands-on", "energetic", "practical", "adventurous"],
            "ESFP": ["enthusiastic", "social", "creative", "spontaneous"],
            "ENFP": ["enthusiastic", "creative", "social", "imaginative"],
            "ENFJ": ["charismatic", "insightful", "compassionate", "inspirational"],
            "ENTJ": ["leadership", "strategic", "decisive", "visionary"],
            "ESTJ": ["organized", "decisive", "practical", "efficient"],
            "ESFJ": ["caring", "sociable", "attention-to-detail", "friendly"],
            "ENTP": ["innovative", "curious", "intellectual", "charismatic"]
        }
        
        return strengths_map.get(mbti_type, ["curious", "creative", "adventurous"])
    
    async def _fetch_activities(self) -> list[Dict[str, Any]]:
        """
        Fetch activities/events from public APIs
        
        Args:
            None
            
        Returns:
            List of available activities
        """
        # Placeholder implementation - in production this would call real APIs
        sample_activities = [
            {
                "id": "001",
                "name": "Community Painting Class",
                "category": "artistic",
                "location": "Local Art Studio",
                "description": "Learn painting techniques in a group setting",
                "suitable_for": ["social", "creative"],
                "indoor": True,
                "skill_level": "beginner",
                "cost_tier": "low"
            },
            {
                "id": "002",
                "name": "Philosophy Book Club",
                "category": "intellectual",
                "location": "Library Community Center",
                "description": "Discuss philosophical texts and ideas",
                "suitable_for": ["intellectual", "social"],
                "indoor": True,
                "skill_level": "any",
                "cost_tier": "low"
            },
            {
                "id": "003",
                "name": "Hiking Group Meetup",
                "category": "physical",
                "location": "City Nature Trails",
                "description": "Guided hiking tours at various difficulty levels",
                "suitable_for": ["physical", "outdoor", "social"],
                "indoor": False,
                "skill_level": "beginner",
                "cost_tier": "low"
            },
            {
                "id": "004",
                "name": "Meditation Workshop",
                "category": "wellness",
                "location": "Wellness Center",
                "description": "Learn mindfulness and meditation techniques",
                "suitable_for": ["solitary", "introvert", "mindful"],
                "indoor": True,
                "skill_level": "any",
                "cost_tier": "medium"
            },
            {
                "id": "005",
                "name": "Cooking Basics Workshop",
                "category": "creative",
                "location": "Community Kitchen",
                "description": "Learn fundamental cooking skills and recipes",
                "suitable_for": ["creative", "intellectual", "social"],
                "indoor": True,
                "skill_level": "beginner",
                "cost_tier": "medium"
            }
        ]
        
        return sample_activities
    
    async def _generate_recommendations(
        self,
        user_profile: User,
        personality_analysis: Dict[str, Any],
        available_activities: list[Dict[str, Any]],
        days_ahead: int
    ) -> list[Dict[str, Any]]:
        """
        Generate personalized recommendations
        
        Args:
            user_profile: User profile
            personality_analysis: Personality analysis results
            available_activities: Available activities
            days_ahead: Number of days to plan
            
        Returns:
            List of activity recommendations
        """
        recommendations = []
        days_ahead = min(days_ahead, 365)  # Cap at 365 days
        
        for i in range(days_ahead):
            date = datetime.now() + timedelta(days=i)
            day_name = date.strftime("%A")
            
            # Score activities based on user fit
            scores = []
            for activity in available_activities:
                # Calculate compatibility score
                score = 0
                
                # Match interests/categories
                if any(keyword in activity["category"].lower() for keyword in 
                      [k.lower() for k in user_profile.interests]):
                    score += 3
                
                # Match personality traits
                if personality_analysis["traits"].get("creative", 0) > 0.5:
                    if "artistic" in activity["category"] or "creative" in activity["category"]:
                        score += 2
                
                # Match MBTI preferences
                if personality_analysis["mbti_analysis"]:
                    # Introvert preference - prefer solitary or small group
                    if activity.get("suitable_for", []):
                        if "social" not in activity["suitable_for"] and personality_analysis["traits"]["solitary"] > 0.5:
                            score += 1
                    
                    # Thinker preference - prefer intellectual activities
                    if "thinking" in personality_analysis["mbti_analysis"] and \
                       "intellectual" in activity["category"]:
                        score += 2
                
                # Indoor/outdoor preference
                if user_profile.preferences.get("indoor", True) and not activity.get("indoor", True):
                    score -= 1
                
                scores.append((activity, score))
            
            # Sort by score and pick top recommendations
            scores.sort(key=lambda x: x[1], reverse=True)
            
            # Add top matching activities to recommendations
            for activity, score in scores[:2]:  # Top 2 activities
                if score > 0:  # Only add if positively matched
                    recommendations.append({
                        "activity": activity,
                        "date": date.strftime("%Y-%m-%d"),
                        "day_name": day_name,
                        "priority": 1 if score == max(s[1] for s in scores) else 2
                    })
        
        return recommendations

# Export engine
__all__ = ["HobbyRecommendationEngine"]