from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from simple_salesforce.exceptions import SalesforceAuthenticationFailed

from casehandlersf import api
from casehandlersf.api import app

client = TestClient(app)

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
