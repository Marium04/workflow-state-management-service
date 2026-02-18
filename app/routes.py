from typing import Optional
from fastapi import Depends, HTTPException, Response, Header, Query, APIRouter
from sqlalchemy.orm import Session
from uuid import UUID

from .db import get_db
from .models import WorkflowStatus
from .schemas import (
    WorkflowItemCreate,
    WorkflowItemListResponse,
    WorkflowItemRead,
    WorkflowItemUpdate,
)
from . import services
from .services import NotFoundError, VersionConflictError, InvalidTransitionError


router = APIRouter(
    prefix="/workflow_items",
    responses={404: {"description": "Not found"}},
)


# Create a workflow item
@router.post("/", response_model=WorkflowItemRead)
def create_workflow_item(
    item: WorkflowItemCreate, response: Response, db: Session = Depends(get_db)
):
    db_item = services.create_workflow_item(db, item)
    response.headers["ETag"] = f'"{db_item.version}"'
    return db_item


# Get all workflow items
@router.get("/", response_model=WorkflowItemListResponse)
def get_all_workflow_items(
    status: Optional[WorkflowStatus] = Query(None),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    return services.get_all_workflow_items(db, status, limit, offset)


# Get a workflow item by id
@router.get("/{item_id}", response_model=WorkflowItemRead)
def get_workflow_item(item_id: UUID, response: Response, db: Session = Depends(get_db)):
    try:
        item = services.get_workflow_item(db, item_id)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Workflow item not found")
    response.headers["ETag"] = f'"{item.version}"'
    return item


# Update
@router.put("/{item_id}", response_model=WorkflowItemRead)
def update_workflow_item(
    item_id: UUID,
    item_update: WorkflowItemUpdate,
    response: Response,
    if_match: str = Header(None),
    db: Session = Depends(get_db),
):

    if if_match is None:
        raise HTTPException(status_code=427, detail="Missing If-Match header")
    try:
        client_version = int(if_match.strip('"'))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid If-Match header")
    try:
        item = services.update_workflow_item(db, item_id, item_update, client_version)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Workflow item not found")
    except VersionConflictError:
        raise HTTPException(
            status_code=412, detail="Precondition failed. Resource was modified."
        )
    except InvalidTransitionError:
        raise HTTPException(status_code=400, detail=f"Invalid status transition")
    response.headers["ETag"] = f'"{item.version}"'
    return item


# Delete
@router.delete("/{item_id}", response_model=dict)
def delete_workflow_item(item_id: UUID, db: Session = Depends(get_db)):
    try:
        services.delete_workflow_item(db, item_id)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Workflow item not found")
    return {"detail": "Workflow item deleted successfully"}
