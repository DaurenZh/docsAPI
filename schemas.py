from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FileResponse(BaseModel):
    id: int
    original_name: str
    version: int
    uploaded_at: datetime
    file_size: int
    
    class Config:
        from_attributes = True

class AnalysisResponse(BaseModel):
    id: int
    file_id: int
    result: str
    analyzed_at: datetime
    
    class Config:
        from_attributes = True
