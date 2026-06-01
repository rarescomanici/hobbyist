"""
FastAPI Application Entry Point
Routes and middleware for Hobbyist AI
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn

from models.user_models import User, HobbyProfile
from agents.strands_orchestrator import StrandsHobbyAgent
from middleware.api_aggregator import APIDataAggregator

# Initialize FastAPI app
app = FastAPI(
    title="Hobbyist AI",
    description="AI-powered hobby recommendation app using Strands Agents",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agents and services
strands_agent = StrandsHobbyAgent()
api_aggregator = APIDataAggregator()

# Mock database (use real database later)
users_db: dict[str, User] = {}
user_profiles_db: dict[str, HobbyProfile] = {}


# ============== USER MANAGEMENT ROUTES ==============

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Hobbyist AI"}


@app.post("/api/users/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: User):
    """Register a new user"""
    users_db[user.email] = user
    return {"message": "User registered successfully", "user": user.model_dump()}


@app.get("/api/users/{email}")
async def get_user(email: str):
    """Get user profile"""
    if email not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[email]


@app.post("/api/users/{email}/profile")
async def update_user_profile(
    email: str,
    profile: User,
    existing_user: Optional[User] = Depends(lambda email: users_db.get(email))
):
    """Update user profile"""
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    users_db[email] = profile
    return {"message": "Profile updated successfully"}


# ============== RECOMMENDATION ROUTES ==============

@app.get("/api/recommendations/{email}")
async def get_recommendations(email: str):
    """
    Get hobby recommendations for user
    
    This endpoint uses Strands Agents to orchestrate multiple AI agents
    that analyze user interests, MBTI type, and preferences.
    """
    if email not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Prepare profile from user
    user = users_db[email]
    profile = HobbyProfile(
        user_email=email,
        hobby_categories=user.interests,
        activity_preferences=user.preferences,
        mbti_personality_type=user.mbti_type
    )
    
    # Generate recommendations using Strands Agents
    recommendations = await strands_agent.orchestrate_recommendations(
        email,
        profile,
        days_ahead=7
    )
    
    return {
        "email": email,
        "recommendations": recommendations,
        "agent_orchestration": "Strands Agents Framework"
    }


@app.post("/api/recommendations/weekly-plan/{email}")
async def generate_weekly_plan(email: str):
    """Generate a weekly hobby plan for the user"""
    if email not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = users_db[email]
    profile = HobbyProfile(
        user_email=email,
        hobby_categories=user.interests,
        activity_preferences=user.preferences,
        mbti_personality_type=user.mbti_type
    )
    
    weekly_plan = await strands_agent.generate_weekly_plan(profile)
    
    return weekly_plan


@app.get("/api/recommendations/{email}/progress/{week}")
async def get_progress(email: str, week: Optional[str] = None):
    """Get user's hobby progress"""
    if email not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = users_db[email]
    progress = await strands_agent.analyze_user_progress(email)
    
    return progress


@app.post("/api/recommendations/complete/{email}/{activity_id}")
async def mark_activity_completed(email: str, activity_id: str):
    """Mark a recommended activity as completed"""
    if email not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    # In production, this would update the database
    activity = {
        "id": activity_id,
        "completed": True,
        "completed_at": "2024-01-01T00:00:00Z"
    }
    
    return {"message": f"Activity {activity_id} marked as completed"}


# ============== SEARCH & BROWSE ROUTES ==============

@app.get("/api/search/hobbies")
async def search_hobbies(query: str, filters: Optional[dict] = None):
    """Search for hobbies by keyword"""
    hobbies = await api_aggregator.search_hobbies(query)
    return {"hobbies": hobbies}


@app.get("/api/trending")
async def get_trending_hobbies():
    """Get currently trending hobbies"""
    trending = await api_aggregator.get_trending_hobbies(location="global")
    return {"trending_hobbies": trending}


@app.get("/api/categories")
async def get_categories():
    """Get available hobby categories"""
    return {
        "categories": [
            {"id": "art", "name": "Artistic", "description": "Painting, drawing, sculpting"},
            {"id": "fitness", "name": "Fitness", "description": "Sports, exercise, wellness"},
            {"id": "music", "name": "Music", "description": "Playing instruments, singing"},
            {"id": "cooking", "name": "Cooking", "description": "Recipes, culinary arts"},
            {"id": "tech", "name": "Technology", "description": "Programming, AI, robotics"},
            {"id": "reading", "name": "Reading", "description": "Books, literature groups"},
            {"id": "outdoor", "name": "Outdoor", "description": "Hiking, camping, gardening"},
            {"id": "crafts", "name": "Crafts", "description": "DIY, knitting, woodworking"},
            {"id": "gaming", "name": "Gaming", "description": "Strategy, board, video games"},
            {"id": "wellness", "name": "Wellness", "description": "Meditation, yoga, mindfulness"}
        ]
    }


# ============== UI ENDPOINTS ==============

GET_STARTED_API_KEY = "GET_STARTED_KEY"
    
@app.get("/ui/get-started")
async def get_get_started_api_key():
    """Get API key for UI"""
    return GET_STARTED_API_KEY


@app.get("/ui/interest-form-response")
async def get_interest_form_response_api_key():
    """Get API key for interest form responses"""
    return "INTEREST_FORM_RESPONSE_KEY"


@app.get("/ui/hobby-dashboard")
async def get_hobby_dashboard_api_key():
    """Get API key for hobby dashboard"""
    return "HOBBY_DASHBOARD_KEY"


# Main runner
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)