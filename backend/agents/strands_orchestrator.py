"""
Hobbyist AI App - Strands Agents Orchestrator
Orchestrates multiple AI agents to generate personalized hobby plans
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from typing import Dict, List, Any
from datetime import datetime, timedelta
import json

from models.user_models import User, HobbyProfile
from agents.hobby_engine import HobbyRecommendationEngine
from middleware.api_aggregator import APIDataAggregator


class StrandsHobbyAgent:
    """
    Strands Agents orchestrator for hobby recommendations
    
    This agent coordinates multiple specialized agents:
    1. User Analysis Agent - analyzes personality and traits
    2. Event Discovery Agent - fetches available activities from APIs
    3. Recommendation Agent - generates personalized plans
    4. Schedule Builder Agent - creates calendar-compatible schedules
    """
    
    def __init__(self):
        self.engine = HobbyRecommendationEngine()
        self.aggregator = APIDataAggregator()
        self.context = {}
    
    async def orchestrate_recommendations(
        self,
        user_email: str,
        user_profile: User,
        days_ahead: int = 7
    ) -> Dict[str, Any]:
        """
        Orchestrate multiple agents to generate hobby plan
        
        Args:
            user_email: User's email for tracking
            user_profile: User profile with interests/preferences
            days_ahead: How many days to plan ahead
            
        Returns:
            Complete recommendation package with activities, schedule, and insights
        """
        print(f"[Strands Agents] Orchestration started for {user_email}")
        
        # Phase 1: User Analysis
        user_results = await self._run_analysis_agent(user_profile)
        print(f"[Strands Agents] Analysis complete: {user_results['traits']}")
        
        # Phase 2: Activity Discovery
        activities = await self._run_discovery_agent()
        print(f"[Strands Agents] Discovered {len(activities)} activities")
        
        # Phase 3: Generate Recommendations
        recommendations = await self._run_recommendation_agent(
            user_profile,
            user_results,
            activities,
            days_ahead
        )
        
        # Phase 4: Build Schedule
        schedule = await self._run_scheduler_agent(
            user_profile.preferences,
            recommendations
        )
        
        # Phase 5: Generate Insights
        insights = await self._run_insight_agent(user_results)
        
        # Phase 6: Generate AI-generated prompt description
        plan_description = await self._generate_agent_prompt_description(
            user_profile, user_results
        )
        
        return {
            "user_email": user_email,
            "activity_date": recommendations.get("date"),
            "week_day": recommendations.get("day"),
            "activity_name": recommendations.get("name"),
            "location": recommendations.get("location"),
            "description": recommendations.get("description"),
            "difficulty": recommendations.get("difficulty"),
            "agent_prompt": plan_description,
            "personality_analysis": user_results,
            "available_activities": activities,
            "schedule": schedule,
            "insights": insights,
            "execution_status": "completed"
        }
    
    async def _run_analysis_agent(self, user_profile: User) -> Dict[str, Any]:
        """User analysis agent - analyze personality and traits"""
        return await self.engine._analyze_user(user_profile)
    
    async def _run_discovery_agent(self) -> List[Dict[str, Any]]:
        """Event discovery agent - fetch activities from APIs"""
        return await self.engine._fetch_activities()
    
    async def _run_recommendation_agent(
        self,
        user_profile: User,
        analysis: Dict,
        activities: List,
        days_ahead: int
    ) -> Dict[str, Any]:
        """Recommendation agent - generate activity suggestions"""
        return await self.engine._generate_recommendations(
            user_profile, analysis, activities, days_ahead
        )
    
    async def _run_scheduler_agent(
        self,
        preferences: Dict[str, Any],
        recommendations: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Schedule builder agent - create organized schedule"""
        schedule = []
        
        # Simple scheduler - distribute activities evenly
        day_count = len(rec) or 1
        for i, rec in enumerate(recommendations if recommendations else []):
            schedule.append({
                "day": i % day_count,
                "activity": rec.get("activity", {}),
                "priority": rec.get("priority", 1)
            })
        
        return schedule
    
    async def _run_insight_agent(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Insight agent - generate personalized insights"""
        insights = []
        
        primary_strengths = analysis.get("primary_strengths", [])
        
        if "creative" in primary_strengths and any(s in primary_strengths for s in ["creative", "intellectual"]):
            insights.append(
                "Based on your interests and personality, you might want to focus on activities that combine creativity with learning. "
                "These activities can help you grow both your artistic skills and your knowledge."
            )
        
        if analysis.get("mbti_analysis") and "introvert" in analysis["mbti_analysis"].get("introvert/extrovert", ""):
            insights.append(
                "You may prefer more introspective activities that allow for deep concentration "
                "and time for reflection on what you're experiencing."
            )
        
        if "intellectual" in primary_strengths:
            insights.append(
                "Your intellectual nature suggests you'll benefit from activities that challenge your mind, "
                "such as strategy games, debates, or learning new skills."
            )
        
        return insights
    
    async def _generate_agent_prompt_description(
        self,
        user_profile: User,
        analysis: Dict[str, Any]
    ) -> str:
        """Generate AI prompt for detailed activity description"""
        # Main prompt template for detailed activity descriptions
        prompt_template = """
        ### AI Activity Description Generator
        You are a friendly hobby enthusiast with expertise in helping people discover new interests through activity planning.
        
        **Task**: Create an engaging, personalized description for the recommended activity.

        **Instructions**:
        1. Write a 2-3 paragraph description that appeals to someone with the following profile:
           - Interests: {{interests}}
           - MBTI Type: {{mbti}} (if provided)
           - Top Traits: {{traits}}
           - Activity: {{activity_name}}
        
        2. Include:
           - Why this activity matches their personality
           - What skills or benefits they'll gain
           - Tips for getting started
           - Any prerequisites or what to expect
        
        3. Keep tone appropriate for {{mbti}} personality type:
           - I* users: Direct, factual, practical
           - E* users: Energetic, social, enthusiastic
           - S* users: Concrete, hands-on, step-by-step
           - N* users: Visionary, conceptual, possibilities-focused
           - T* users: Logical, efficiency-focused, analytical
           - F* users: Empathetic, supportive, meaningful
        
        4. Add 1-2 suggested "next steps" for them to consider
        """
        
        # Replace placeholders with actual data
        interests_str = ", ".join(user_profile.interests)
        
        prompt = prompt_template.replace(
            "{{interests}}",
            interests_str or "various interests"
        ).replace(
            "{{mbti}}",
            user_profile.mbti_type or "general"
        ).replace(
            "{{traits}}",
            ", ".join(analysis.get("primary_strengths", ["curious", "adventurous"]))
        ).replace(
            "{{activity_name}}",
            "Recommended Activity"
        )
        
        return prompt
    
    async def generate_weekly_plan(self, user_profile: User) -> Dict[str, Any]:
        """
        Generate a weekly hobby plan
        
        Args:
            user_profile: User profile
            
        Returns:
            Weekly plan with activities for each day
        """
        # Get recommendations
        user_email = user_profile.user_email or "user"
        recommendations = await self.orchestrate_recommendations(
            user_email,
            user_profile,
            days_ahead=7
        )
        
        # Build weekly schedule
        weekly_plan = {
            "week_of": datetime.now().strftime("%Y-%m-%d"),
            "activities": [],
            "total_activities": 0
        }
        
        for day in recommendations.get("schedule", []):
            if day.get("day") >= 7:
                break
            
            activity = day.get("activity", {})
            weekly_plan["activities"].append({
                "day": day.get("day") + 1,
                "activity_name": activity.get("name", f"Activity {day.get('day') + 1}"),
                "category": activity.get("category"),
                "description": activity.get("description"),
                "indoor": activity.get("indoor", True)
            })
            weekly_plan["total_activities"] += 1
        
        return weekly_plan
    
    async def analyze_user_progress(self, user_email: str) -> Dict[str, Any]:
        """Analyze user's hobby engagement and progress"""
        history = self.recommendations_history.get(user_email, [])
        
        completed = len([a for a in history if a.get("completed", False)])
        total = len(history)
        
        return {
            "user_email": user_email,
            "total_recommendations": total,
            "completed": completed,
            "completion_rate": (completed / total * 100) if total > 0 else 0
        }