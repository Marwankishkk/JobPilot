from pydantic import BaseModel , Field
from typing import Optional
import datetime
import enum
class JobStatus(str, enum.Enum):
    applied = "applied"
    interviewing = "interviewing"
    offered = "offered"
    rejected = "rejected"

class JobBase(BaseModel):
    title: str
    description: str | None = None
    company: str
    location: str
    status: JobStatus = JobStatus.applied
    applied_date: datetime.date | None = None

class JobCreate(JobBase):
    title: str = Field(..., min_length=1)
    description: str | None = Field(None, max_length=1000)
    company: str = Field(..., min_length=1)
    location: str = Field(..., min_length=1)
    status: JobStatus = Field(JobStatus.applied)
    applied_date: datetime.date | None = None

class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    status: Optional[JobStatus] = None
    applied_date: Optional[datetime.date] = None
