from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ScanIn(BaseModel):
    disease_name: str
    confidence: float
    recommendations: Optional[str] = None

class ScanOut(BaseModel):
    id: str
    user_id: str
    image_path: str
    disease_name: str
    confidence: float
    recommendations: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ScanHistoryOut(BaseModel):
    scans: list[ScanOut]
    total: int

class UserStatsOut(BaseModel):
    total_scans: int
    healthy_crops: int
    diseases: int
    reports: int

