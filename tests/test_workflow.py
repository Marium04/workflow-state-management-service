import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_workflow_item():
    response = client.post(
        "/workflow_items/",
        json={"title": "Test Item", "description": "Testing"},
    )

    assert response.status_code == 200
    data = response.json()

    assert data["title"] == "Test Item"
    assert data["status"] == "CREATED"
    assert "id" in data


def test_invalid_status_transition():
    # Create item
    response = client.post(
        "/workflow_items/",
        json={"title": "Transition Test", "description": "Testing"},
    )
    item = response.json()
    item_id = item["id"]

    # Move to IN_PROGRESS
    etag = response.headers.get("ETag")

    update_response = client.put(
        f"/workflow_items/{item_id}",
        headers={"If-Match": etag},
        json={"status": "IN_PROGRESS"},
    )

    assert update_response.status_code == 200

    # Try invalid transition: COMPLETED → IN_PROGRESS
    new_etag = update_response.headers.get("ETag")

    complete_response = client.put(
        f"/workflow_items/{item_id}",
        headers={"If-Match": new_etag},
        json={"status": "COMPLETED"},
    )

    assert complete_response.status_code == 200

    invalid_etag = complete_response.headers.get("ETag")

    invalid_response = client.put(
        f"/workflow_items/{item_id}",
        headers={"If-Match": invalid_etag},
        json={"status": "IN_PROGRESS"},
    )

    assert invalid_response.status_code == 400


def test_etag_conflict():
    # Create item
    response = client.post(
        "/workflow_items/",
        json={"title": "ETag Test", "description": "Testing"},
    )

    item = response.json()
    item_id = item["id"]

    # Wrong version
    conflict_response = client.put(
        f"/workflow_items/{item_id}",
        headers={"If-Match": '"999"'},
        json={"status": "IN_PROGRESS"},
    )

    assert conflict_response.status_code == 412
