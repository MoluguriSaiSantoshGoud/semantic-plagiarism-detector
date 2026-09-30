from pydantic import BaseModel
from datetime import datetime


class ReportResponse(BaseModel):
    id: int
    comparison_id: int
    report_path: str
    created_at: datetime
    
    class Config:
        from_attributes = True
