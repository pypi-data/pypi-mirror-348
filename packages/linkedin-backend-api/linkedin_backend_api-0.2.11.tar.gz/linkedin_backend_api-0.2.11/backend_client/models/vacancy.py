from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class Vacancy(BaseModel):
    job_id: str
    title: Optional[str] = None
    description: Optional[str] = None
    optimized_description: Optional[str] = None
    listed_time: Optional[str] = None
    employment_type: Optional[str] = None
    company: Optional[str] = None
    industries: Optional[str] = None
    job_function: Optional[str] = None
    seniority_level: Optional[str] = None
    workplace_type: Optional[str] = None
    location: Optional[str] = None
    url: str
    source: str = "linkedin"
    created_at: Optional[datetime] = None 