import uuid

import pytest
from starlette.testclient import TestClient

from src.api.dependencies import get_comparison_service
from src.api.main import app
from src.database.connection import init_db
from src.judge.model_loader import MockJudgeEvaluator
from src.services.comparison_service import ComparisonService


@pytest.fixture
def local_client():
    init_db()

    app.dependency_overrides[get_comparison_service] = lambda: ComparisonService(
        judge=MockJudgeEvaluator()
    )

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_comparison_service, None)


def test_e2e_live_models_catalog(local_client):
    res = local_client.get("/api/models")

    assert res.status_code == 200
    data = res.json()
    assert data["total"] >= 10
    model_ids = [m["id"] for m in data["models"]]
    assert any("openrouter" in m for m in model_ids)


@pytest.mark.skip(reason="Requires external API generation or live provider mock")
def test_e2e_live_mode1_generate_3_models():
    pass


@pytest.mark.skip(reason="Requires external API generation or live provider mock")
def test_e2e_live_mode1_generate_4_models():
    pass


def test_e2e_live_mode2_manual_compare_4_answers(local_client):
    payload = {
        "problem": "Explain ACID properties in database management systems.",
        "answers": [
            {
                "model_name": "GPT-4.1",
                "answer": "Atomicity ensures all-or-nothing transactions. Consistency maintains invariants. Isolation prevents concurrency anomalies. Durability guarantees committed data survives crashes.",
            },
            {
                "model_name": "Claude Sonnet",
                "answer": "ACID stands for Atomicity, Consistency, Isolation, and Durability. Essential for relational transactional databases.",
            },
            {
                "model_name": "Gemini Pro",
                "answer": "Atomicity, Consistency, Isolation, Durability. Implemented using write-ahead logs and MVCC.",
            },
            {
                "model_name": "DeepSeek R1",
                "answer": "ACID properties govern database transactions ensuring correctness under failure and concurrent execution.",
            },
        ],
        "position_swap_check": True,
    }

    res = local_client.post("/api/manual-compare", json=payload)

    assert res.status_code == 200

    report = res.json()

    assert report["mode"] == "MANUAL_COMPARE"
    assert len(report["answers"]) == 4
    assert len(report["pairwise_comparisons"]) == 6
    assert len(report["rankings"]) == 4

    for comparison in report["pairwise_comparisons"]:
        assert comparison["position_swap_check"]["executed"] is True


def test_e2e_live_selective_save_and_history(local_client):
    suffix = uuid.uuid4().hex[:8]

    auth_res = local_client.post(
        "/api/auth/register",
        json={
            "username": f"live_{suffix}",
            "email": f"live_{suffix}@example.test",
            "password": "test-password-123",
        },
    )

    assert auth_res.status_code == 200
    headers = {"Authorization": f"Bearer {auth_res.json()['token']}"}

    compare_payload = {
        "problem": "What is the time complexity of QuickSort average and worst case?",
        "answers": [
            {
                "model_name": "Candidate Alpha",
                "answer": "QuickSort average case is O(n log n). Worst case is O(n^2) when pivot selection is poor.",
            },
            {
                "model_name": "Candidate Beta",
                "answer": "QuickSort is always O(n log n).",
            },
        ],
    }

    comp_res = local_client.post("/api/manual-compare", json=compare_payload)

    assert comp_res.status_code == 200

    report = comp_res.json()
    session_id = report["session_id"]

    save_payload = {
        "save_options": {
            "prompt": True,
            "answers": True,
            "evaluations": True,
            "metrics": True,
            "raw_responses": False,
        },
        "session_data": report,
    }

    save_res = local_client.post(
        f"/api/sessions/{session_id}/save",
        json=save_payload,
        headers=headers,
    )

    assert save_res.status_code == 200
    assert save_res.json()["success"] is True

    get_res = local_client.get(
        f"/api/sessions/{session_id}",
        headers=headers,
    )

    assert get_res.status_code == 200

    saved_data = get_res.json()["data"]

    assert saved_data["session_id"] == session_id
    assert saved_data["input"]["prompt"] == compare_payload["problem"]
    assert len(saved_data["answers"]) == 2
    assert len(saved_data["pairwise_comparisons"]) == 1

    list_res = local_client.get("/api/sessions", headers=headers)

    assert list_res.status_code == 200

    all_sessions = list_res.json()["data"]
    assert any(s["session_id"] == session_id for s in all_sessions)
