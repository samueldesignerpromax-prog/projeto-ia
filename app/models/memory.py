from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.sql import func
from app.database.connection import Base

class Memory(Base):
    __tablename__ = "memories"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), index=True, nullable=False)
    user_message = Column(Text, nullable=False)
    assistant_response = Column(Text, nullable=False)
    context = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    relevance_score = Column(Float, default=1.0)
    tags = Column(String(255), nullable=True)
    
    def __repr__(self):
        return f"<Memory(id={self.id}, user_id={self.user_id})>"
