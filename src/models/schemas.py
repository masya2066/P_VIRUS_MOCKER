from fastapi import Form
from pydantic import BaseModel
from datetime import datetime


class KataFileCreate(BaseModel):
    scan_id: str = Form("scanId")
    state: str = "processing"
    content: str = Form("content")


class KataFileResponse(BaseModel):
    id: int
    scan_id: str
    state: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Updated for Pydantic v2
