from datetime import datetime

from pydantic import BaseModel, ConfigDict , Field


from app.db.models import IncidentSeverity, IncidentStatus


class IncidentCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=5000)
    severity: IncidentSeverity = IncidentSeverity.MEDIUM
    source: str = Field(min_length=1, max_length=100)
    service: str = Field(min_length=1, max_length=100)
    detected_at: datetime

class IncidentResponse(BaseModel):
    id: int
    title: str
    description: str | None
    severity: IncidentSeverity
    status: IncidentStatus
    source: str
    service: str
    detected_at: datetime
    resolved_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
