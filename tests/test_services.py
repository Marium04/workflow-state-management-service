import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import Base
from app import services
from app.models import WorkflowStatus
from app.schemas import WorkflowItemCreate, WorkflowItemUpdate

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(bind=engine)

    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_update_workflow_success(db_session):
    # Create item
    create_payload = WorkflowItemCreate(
        title="Test",
        description="Test description"
    )

    item = services.create_workflow_item(db_session, create_payload)

    original_version = item.version

    update_payload = WorkflowItemUpdate(
        title="Updated",
        description="Updated desc",
        status=WorkflowStatus.IN_PROGRESS
    )

    updated = services.update_workflow_item(
        db_session,
        item.id,
        update_payload,
        client_version=original_version,
    )

    assert updated.title == "Updated"
    assert updated.status == WorkflowStatus.IN_PROGRESS
    assert updated.version == original_version + 1
    assert updated.status_updated_at is not None

def test_version_conflict_raises(db_session):
    create_payload = WorkflowItemCreate(
        title="Test",
        description="Test description"
    )

    item = services.create_workflow_item(db_session, create_payload)

    update_payload = WorkflowItemUpdate(
        title="Updated",
        description="Updated desc",
        status=WorkflowStatus.IN_PROGRESS
    )

    with pytest.raises(services.VersionConflictError):
        services.update_workflow_item(
            db_session,
            item.id,
            update_payload,
            client_version=999,  # wrong version
        )

def test_invalid_transition_raises(db_session):
    create_payload = WorkflowItemCreate(
        title="Test",
        description="Test description"
    )

    item = services.create_workflow_item(db_session, create_payload)

    update_payload = WorkflowItemUpdate(
        title="Test",
        description="Test",
        status=WorkflowStatus.COMPLETED,
    )

    with pytest.raises(services.InvalidTransitionError):
        services.update_workflow_item(
            db_session,
            item.id,
            update_payload,
            client_version=item.version,
        )
