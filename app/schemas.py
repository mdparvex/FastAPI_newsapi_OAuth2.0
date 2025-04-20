from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class LatestNewsSchema(BaseModel):
    news_id: int
    title: str
    description: Optional[str]=None
    url: str
    publishedAt: datetime
    created_at: datetime

    class Config:
        orm_mode = True

class SaveLatestRequest(BaseModel):
    country_code: Optional[str] = None
    source_id: Optional[str] = None


