from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class Notification(BaseModel):
    user_id: int
    job_id: str
    message: str
    relevance_score: Optional[int] = None
    relevance_score_success: Optional[bool] = None
    parse_mode: str = "HTML"
    disable_web_page_preview: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None 