from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class Location(BaseModel):
    name: Optional[str] = None
    geoid: Optional[str] = None

class AIFilter(BaseModel):
    enabled: bool = False
    mode: str = "filter"
    prompt: Optional[str] = None
    threshold: int = 75

class UserBotSettings(BaseModel):
    language: str = "en"
    onboarding_status: bool = False
    
class LinkedinFilters(BaseModel):
    work_formats: List[str] = []
    job_types: List[str] = []
    exp_levels: List[str] = []
    companies: List[str] = []
    
class UserSearchSettings(BaseModel):
    enabled: bool = False
    keywords: List[str]
    locations: List[Location]
    linkedin_filters: Optional[LinkedinFilters] = LinkedinFilters()
    ai_filter: Optional[AIFilter] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class User(BaseModel):
    user_id: int
    bot_settings: Optional[UserBotSettings] = None
    search_settings: Optional[UserSearchSettings] = None

class UserCreateDTO(BaseModel):
    user_id: int
    bot_settings: Optional[UserBotSettings] = None 