from fastapi.testclient import TestClient

from app.main import create_app


def test_ambiguous_recipient_blocks_launch():
    client = TestClient(create_app())
    response = client.post("/v1/requests", json={"instruction": "Ask the client for missing renewal details. Don't call."})
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "needs_review"
    assert data["activePlan"]["blockingClarifications"]
    assert "approve" not in data["allowedActions"]


def test_finance_instruction_can_be_approved_to_synthetic_result():
    client = TestClient(create_app())
    response = client.post(
        "/v1/requests",
        json={"instruction": "Ask the client's finance contact for the three missing figures. Don't call."},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "awaiting_approval"
    assert data["activePlan"]["respondent"]["email"] == "riya.shah@example.com"

    approval = client.post(
        f"/v1/requests/{data['id']}/approvals",
        json={"planVersion": data["activePlan"]["version"], "planHash": data["activePlan"]["planHash"]},
    )
    assert approval.status_code == 200
    approved = approval.json()
    assert approved["status"] == "ready_for_review"
    assert approved["result"]["status"] == "partial"
    assert approved["result"]["unresolvedItems"]


def test_stale_hash_rejected():
    client = TestClient(create_app())
    response = client.post(
        "/v1/requests",
        json={"instruction": "Ask finance for initial collection information by email."},
    )
    data = response.json()
    approval = client.post(
        f"/v1/requests/{data['id']}/approvals",
        json={"planVersion": data["activePlan"]["version"], "planHash": "not-the-real-hash"},
    )
    assert approval.status_code == 409
