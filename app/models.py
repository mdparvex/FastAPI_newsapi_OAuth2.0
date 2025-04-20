from app.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text, DateTime


class LatestNewsModel(Base):
    __tablename__ = "latestnews"

    news_id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    description = Column(String,nullable=True)
    url = Column(String,nullable=False, unique=True)
    publishedAt = Column(DateTime,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
