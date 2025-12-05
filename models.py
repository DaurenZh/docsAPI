from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class File(Base):
    __tablename__ = "files"
    
    id = Column(Integer, primary_key=True, index=True)
    original_name = Column(String, nullable=False)
    version = Column(Integer, default=1)
    path = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    uploaded_by = Column(Integer, default=1)
    
    analyses = relationship("Analysis", back_populates="file")

class Analysis(Base):
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("files.id"), nullable=False)
    result = Column(Text, nullable=False)
    analyzed_at = Column(DateTime, default=datetime.utcnow)
    
    file = relationship("File", back_populates="analyses")
