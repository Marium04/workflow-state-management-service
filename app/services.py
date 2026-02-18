from sqlalchemy.orm import Session
from datetime import datetime, timezone
from .models import WorkflowItem, WorkflowStatus


class NotFoundError(Exception):
    pass


class VersionConflictError(Exception):
    pass


class InvalidTransitionError(Exception):
    pass


ALLOWED_TRANSITIONS = {
    WorkflowStatus.CREATED: {WorkflowStatus.IN_PROGRESS, WorkflowStatus.CANCELLED},
    WorkflowStatus.IN_PROGRESS: {WorkflowStatus.COMPLETED, WorkflowStatus.CANCELLED},
    WorkflowStatus.COMPLETED: set(),
    WorkflowStatus.CANCELLED: set(),
}


def create_workflow_item(db: Session, payload):
    db_item = WorkflowItem(**payload.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_workflow_item(db: Session, item_id):
    item = db.query(WorkflowItem).filter(WorkflowItem.id == item_id).first()
    if not item:
        raise NotFoundError()
    return item


def get_all_workflow_items(db: Session, status, limit, offset):
    query = db.query(WorkflowItem)

    if status is not None:
        query = query.filter(WorkflowItem.status == status)

    total = query.count()
    items = query.offset(offset).limit(limit).all()

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": items,
    }


def delete_workflow_item(db: Session, item_id):
    item = get_workflow_item(db, item_id)
    db.delete(item)
    db.commit()


def update_workflow_item(db: Session, item_id, payload, client_version: int):
    item = get_workflow_item(db, item_id)

    if item.version != client_version:
        raise VersionConflictError()

    if payload.title is not None:
        item.title = payload.title

    if payload.description is not None:
        item.description = payload.description

    if payload.status is not None and item.status != payload.status:
        allowed = ALLOWED_TRANSITIONS[item.status]
        if payload.status not in allowed:
            raise InvalidTransitionError()

        item.status = payload.status
        item.status_updated_at = datetime.now(timezone.utc)

    item.version += 1

    db.commit()
    db.refresh(item)

    return item
