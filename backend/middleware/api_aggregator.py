"""
Public API Aggregator for Hobbyist App
Provides unified access to external event/activity APIs
"""

import requests
from typing import Dict, List, Optional, Any
from datetime import datetime
import os


class APIDataAggregator:
    """
    Aggregates data from multiple hobby/activity APIs
    """
    
    def __init__(self, api_keys: Optional[Dict[str, str]] = None):
        """
        Initialize API aggregator
        
        Args:
            api_keys: Dictionary of API keys
        """
        self.api_keys = api_keys or {}
        self.api_endpoints = {
            "meetup": self._fetch_meetup_events,
            "eventbrite": self._fetch_eventbrite_events,
            "google_places": self._fetch_google_places,
            "reddit_subreddits": self._fetch_reddit_hobbies
        }
        self.default_cache = {
            "meetup": self._create_sample_meetup_events,
            "eventbrite": self._create_sample_eventbrite_events,
            "google_places": self._create_sample_google_places,
            "reddit_subreddits": self._create_sample_subreddits
        }
    
    async def fetch_events_by_category(
        self,
        category: str,
        location: str = None,
        date_range: tuple = None
    ) -> List[Dict[str, Any]]:
        """
        Fetch events from available APIs
        
        Args:
            category: Hobby category (e.g., "art", "fitness", "tech")
            location: City/location filter
            date_range: (start_date, end_date) tuple
            
        Returns:
            List of event/activity data
        """
        # Try relevant APIs in order
        event_types = self._map_category_to_apis(category)
        
        events = []
        for api_name in event_types:
            if api_name in self.api_endpoints:
                try:
                    events.extend(await self.api_endpoints[api_name](
                        category, location, date_range
                    ))
                except Exception as e:
                    print(f"Error fetching from {api_name}: {e}")
                    # Fall back to defaults if real API fails in demo
                    if api_name in self.default_cache:
                        events.extend(self.default_cache[api_name]())
        
        return events
    
    def _fetch_meetup_events(
        self,
        category: str,
        location: str,
        date_range: tuple
    ) -> List[Dict[str, Any]]:
        """Fetch events from Meetup API"""
        # Mock implementation - in production would call real Meetup API
        category_keywords = category.lower()
        
        sample_events = [
            {
                "source": "meetup",
                "name": f"{category.title()} Meetup Group",
                "description": f"Join our community of {category_keywords} enthusiasts",
                "category": category,
                "location": location or "Remote",
                "indoor": True,
                "difficulty": "beginner",
                "social": True
            }
        ]
        
        return sample_events
    
    def _fetch_eventbrite_events(
        self,
        category: str,
        location: str,
        date_range: tuple
    ) -> List[Dict[str, Any]]:
        """Fetch events from Eventbrite API"""
        # Mock implementation
        category_keywords = category.lower()
        
        sample_events = [
            {
                "source": "eventbrite",
                "name": f"Learn {category} Basics",
                "description": f"A beginner-friendly workshop on {category_keywords}",
                "category": category,
                "location": location or "Online",
                "indoor": True,
                "difficulty": "beginner",
                "social": True,
                "cost": "free"
            }
        ]
        
        return sample_events
    
    def _fetch_google_places(
        self,
        category: str,
        location: str,
        date_range: tuple
    ) -> List[Dict[str, Any]]:
        """Fetch places from Google Places API"""
        # Mock implementation
        category_keywords = category.lower()
        
        return [
            {
                "source": "google_places",
                "name": f"{category.title()} Studio/Space",
                "description": f"A dedicated space for {category_keywords} activities",
                "category": category,
                "location": location or "Various locations",
                "indoor": True,
                "difficulty": "any",
                "social": True
            }
        ]
    
    async def _fetch_reddit_hobbies(
        self,
        category: str,
        location: str,
        date_range: tuple
    ) -> List[Dict[str, Any]]:
        """Fetch hobby communities from Reddit"""
        # Mock implementation
        return [
            {
                "source": "reddit",
                "name": f"r/{category.lower()} Community",
                "description": f"Discussion and resources for {category_keywords}",
                "category": category,
                "location": "Online",
                "indoor": True,
                "difficulty": "any",
                "social": True
            }
        ]
    
    def _map_category_to_apis(self, category: str) -> List[str]:
        """Map hobby category to appropriate APIs"""
        category_lower = category.lower()
        
        mappings = {
            "art": ["meetup", "eventbrite", "google_places"],
            "fitness": ["meetup", "eventbrite", "google_places"],
            "tech": ["reddit_subreddits", "meetup"],
            "music": ["meetup", "eventbrite"],
            "cooking": ["meetup", "eventbrite", "google_places"],
            "sports": ["meetup", "google_places"],
            "reading": ["reddit_subreddits", "meetup"],
            "gardening": ["eventbrite", "meetup"],
            "default": ["meetup", "eventbrite", "google_places", "reddit_subreddits"]
        }
        
        return mappings.get(category_lower, mappings["default"])
    
    async def search_hobbies(self, query: str, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Search for hobbies matching user interests
        
        Args:
            query: User's interest keywords
            filters: Optional filters (indoor, cost, etc.)
            
        Returns:
            List of hobby suggestions
        """
        keywords = [k.strip().lower() for k in query.split()]
        
        hobbies = [
            {
                "source": "discovery",
                "name": f"{keywords[0].title()} Interest Group",
                "description": f"Connect with others interested in {keywords[0]} and related topics",
                "category": keywords[0].capitalize(),
                "location": "Flexible",
                "indoor": True,
                "difficulty": "any",
                "social": True
            }
        ]
        
        return hobbies
    
    async def get_trending_hobbies(self, location: str) -> List[Dict[str, Any]]:
        """Get currently popular hobbies in area"""
        return [
            {
                "source": "trending",
                "name": "AI and Technology Hobbies",
                "description": "Explore emerging tech hobbies and skills",
                "category": "technology",
                "trending_score": 95
            },
            {
                "source": "trending",
                "name": "Urban Gardening",
                "description": "Grow your own food in limited spaces",
                "category": "gardening",
                "trending_score": 88
            },
            {
                "source": "trending",
                "name": "Photography Walks",
                "description": "Learn photography while exploring your area",
                "category": "photography",
                "trending_score": 82
            }
        ]
    
    def _create_sample_meetup_events(self) -> List[Dict[str, Any]]:
        """Create sample meetup events for demo"""
        return [
            {
                "source": "meetup",
                "name": "Art Supplies & Techniques",
                "description": "Learn about art supplies and painting techniques",
                "category": "art",
                "location": "Community Art Studio",
                "indoor": True,
                "difficulty": "beginner",
                "social": True
            },
            {
                "source": "meetup",
                "name": "Running Group",
                "description": "Weekly running sessions for all levels",
                "category": "fitness",
                "location": "Community Parks",
                "indoor": False,
                "difficulty": "beginner",
                "social": True
            }
        ]
    
    def _create_sample_eventbrite_events(self) -> List[Dict[str, Any]]:
        """Create sample eventbrite events for demo"""
        return [
            {
                "source": "eventbrite",
                "name": "Cooking Workshop: Italian Cuisine",
                "description": "Learn authentic Italian recipes and techniques",
                "category": "cooking",
                "location": "Community Kitchen",
                "indoor": True,
                "difficulty": "intermediate",
                "social": True,
                "cost": "medium"
            }
        ]
    
    def _create_sample_google_places(self) -> List[Dict[str, Any]]:
        """Create sample google places for demo"""
        return [
            {
                "source": "google_places",
                "name": "Local Library",
                "description": "Access to books, workshops, and community events",
                "category": "reading",
                "location": "Main Street Library",
                "indoor": True,
                "difficulty": "any",
                "social": True
            }
        ]
    
    def _create_sample_subreddits(self) -> List[Dict[str, Any]]:
        """Create sample subreddit suggestions"""
        return [
            {
                "source": "reddit",
                "name": "r/LearnProgramming",
                "description": "Beginner-friendly programming resources",
                "category": "programming",
                "location": "Online",
                "indoor": True,
                "difficulty": "beginner",
                "social": True
            }
        ]