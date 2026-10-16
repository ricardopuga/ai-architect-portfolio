from pathlib import Path

import pytest
from conftest import AUTH
from fastapi.testclient import TestClient
from pydantic import ValidationError
from simple_salesforce.exceptions import (
    SalesforceAuthenticationFailed,
    SalesforceRefusedRequest,
)

from casehandlersf import api
from casehandlersf.api import app

client = TestClient(app, headers=AUTH)

# Shaped like a record from simple-salesforce's query() result.
FAKE_RECORDS = {
    "00001001": {
        "attributes": {
            "type": "Case",
            "url": "/services/data/v65.0/sobjects/Case/500g800002HiYr3AAF",
        },
        "Id": "500g800002HiYr3AAF",
        "CaseNumber": "00001001",
        "Subject": "Performance inadequate for second consecutive week",
        "Description": None,
        "Priority": "High",
        "Status": "Closed",
        "CreatedDate": "2026-07-01T09:15:00.000+0000",
        "ClosedDate": "2026-07-03T17:00:00.000+0000",
    },
    "00001002": {
        "attributes": {
            "type": "Case",
            "url": "/services/data/v65.0/sobjects/Case/500g800002HiYr5AAF",
        },
        "Id": "500g800002HiYr5AAF",
        "CaseNumber": "00001002",
        "Subject": "Seeking guidance on electrical wiring installation for GC5060",
        "Description": "Customer asks for the wiring diagram.",
        "Priority": "Medium",
        "Status": "Working",
        "CreatedDate": "2026-07-02T10:00:00.000+0000",
        "ClosedDate": None,
    },
}


@pytest.fixture(autouse=True)
def fake_salesforce(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(api, "find_case", FAKE_RECORDS.get)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.parametrize(
    ("method", "path"),
    [("GET", "/cases/00001001"), ("POST", "/cases/00001001/comments")],
)
@pytest.mark.parametrize(
    "headers", [{}, {"X-API-Key": "wrong"}, {"X-API-Key": ""}], ids=str
)
def test_cases_need_api_key(
    created_comments: list, method: str, path: str, headers: dict
) -> None:
    unauthenticated = TestClient(app, headers=headers)
    response = unauthenticated.request(method, path, json={"body": "Hello"})
    assert response.status_code == 401
    assert response.json() == {"detail": "missing or invalid API key"}
    assert created_comments == []


def test_health_needs_no_api_key() -> None:
    assert TestClient(app).get("/health").status_code == 200


@pytest.mark.parametrize("value", [None, "too-short"])
def test_app_refuses_to_start_without_valid_api_key(
    monkeypatch: pytest.MonkeyPatch, value: str | None
) -> None:
    monkeypatch.chdir(Path(__file__).parent)  # away from the project's .env
    if value is None:
        monkeypatch.delenv("API_KEY")
    else:
        monkeypatch.setenv("API_KEY", value)
    api._api_key.cache_clear()
    with pytest.raises(ValidationError, match="api_key"), TestClient(app):
        pass


def test_get_case() -> None:
    response = client.get("/cases/00001001")
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == "500g800002HiYr3AAF"
    assert body["case_number"] == "00001001"
    assert body["priority"] == "High"
    assert body["description"] is None
    assert body["created_date"] == "2026-07-01T09:15:00Z"
    assert body["closed_date"] == "2026-07-03T17:00:00Z"
    assert "attributes" not in body


def test_status_outside_old_mock_values_is_accepted() -> None:
    body = client.get("/cases/00001002").json()
    assert body["status"] == "Working"
    assert body["closed_date"] is None


def test_unknown_case_returns_404() -> None:
    response = client.get("/cases/99999999")
    assert response.status_code == 404
    assert response.json() == {"detail": "case 99999999 not found"}


def test_salesforce_failure_returns_502(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail(_key: str) -> None:
        raise SalesforceAuthenticationFailed("INVALID_CLIENT", "bad secret")

    monkeypatch.setattr(api, "find_case", fail)
    response = client.get("/cases/00001001")
    assert response.status_code == 502
    assert response.json() == {
        "detail": "Salesforce request failed: SalesforceAuthenticationFailed"
    }


@pytest.mark.skipif(
    not Path(".env").exists(), reason="needs Salesforce credentials in .env"
)
def test_live_salesforce_lookup(monkeypatch: pytest.MonkeyPatch) -> None:
    from casehandlersf.salesforce import find_case

    monkeypatch.setattr(api, "find_case", find_case)
    by_number = client.get("/cases/00001001")
    assert by_number.status_code == 200
    record_id = by_number.json()["id"]
    by_id = client.get(f"/cases/{record_id}")
    assert by_id.json()["case_number"] == "00001001"
    assert client.get("/cases/99999999").status_code == 404


@pytest.fixture
def created_comments(monkeypatch: pytest.MonkeyPatch) -> list[tuple[str, str, bool]]:
    """Fake add_case_comment; records each call instead of writing to Salesforce."""
    calls: list[tuple[str, str, bool]] = []

    def fake_add(case_id: str, body: str, is_published: bool) -> str:
        calls.append((case_id, body, is_published))
        return "00ag800000CommentAAA"

    monkeypatch.setattr(api, "add_case_comment", fake_add)
    return calls


def test_create_comment(created_comments: list) -> None:
    response = client.post(
        "/cases/00001001/comments", json={"body": "  Called the customer back.  "}
    )
    assert response.status_code == 201
    assert response.json() == {
        "id": "00ag800000CommentAAA",
        "case_id": "500g800002HiYr3AAF",
        "body": "Called the customer back.",
        "is_published": False,
    }
    assert created_comments == [
        ("500g800002HiYr3AAF", "Called the customer back.", False)
    ]


def test_create_published_comment(created_comments: list) -> None:
    response = client.post(
        "/cases/00001002/comments", json={"body": "Fixed.", "is_published": True}
    )
    assert response.status_code == 201
    assert created_comments == [("500g800002HiYr5AAF", "Fixed.", True)]


@pytest.mark.parametrize(
    ("payload", "field"),
    [
        ({}, "body"),
        ({"body": ""}, "body"),
        ({"body": "   "}, "body"),
        ({"body": "x" * (api.COMMENT_MAX_LENGTH + 1)}, "body"),
        ({"body": 123}, "body"),
        ({"body": "ok", "is_published": "maybe"}, "is_published"),
        ({"body": "ok", "author": "me"}, "author"),
    ],
)
def test_invalid_comment_returns_422(
    created_comments: list, payload: dict, field: str
) -> None:
    response = client.post("/cases/00001001/comments", json=payload)
    assert response.status_code == 422
    assert [err["loc"] for err in response.json()["detail"]] == [["body", field]]
    assert created_comments == []


def test_comment_at_max_length_is_accepted(created_comments: list) -> None:
    body = "x" * api.COMMENT_MAX_LENGTH
    response = client.post("/cases/00001001/comments", json={"body": body})
    assert response.status_code == 201


def test_comment_on_unknown_case_returns_404(created_comments: list) -> None:
    response = client.post("/cases/99999999/comments", json={"body": "Hello"})
    assert response.status_code == 404
    assert response.json() == {"detail": "case 99999999 not found"}
    assert created_comments == []


def test_comment_rejected_by_salesforce_returns_502(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def refuse(case_id: str, body: str, is_published: bool) -> str:
        raise SalesforceRefusedRequest(
            "https://example.my.salesforce.com/services/data/v65.0/sobjects/CaseComment/",
            403,
            "CaseComment",
            [{"message": "insufficient access", "errorCode": "INSUFFICIENT_ACCESS"}],
        )

    monkeypatch.setattr(api, "add_case_comment", refuse)
    response = client.post("/cases/00001001/comments", json={"body": "Hello"})
    assert response.status_code == 502
    assert response.json() == {
        "detail": "Salesforce request failed: SalesforceRefusedRequest (INSUFFICIENT_ACCESS)"
    }
