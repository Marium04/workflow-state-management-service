from enum import Enum
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class Status(str, Enum):
    CREATED = "CREATED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class WorkflowItemRead(BaseModel):
    id: UUID
    title: str
    description: Optional[str] = None
    status: Status
    version: int
    created_at: datetime
    updated_at: datetime
    status_updated_at: datetime

    model_config = ConfigDict(from_attributes = True)


class WorkflowItemCreate(BaseModel):
    title: str
    description: Optional[str] = None


class WorkflowItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Status] = None

class WorkflowItemListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: List[WorkflowItemRead]
