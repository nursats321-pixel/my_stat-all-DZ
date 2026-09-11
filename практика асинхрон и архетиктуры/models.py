from sqlalchemy import Column, Integer, String, Boolean

from database import Base

class Task(Base):
    __tablename__ = "task"
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    is_completed = Column(Boolean, default=False)
    
    