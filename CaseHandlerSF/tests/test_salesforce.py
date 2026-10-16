"""Offline tests for the Salesforce layer, with a fake simple-salesforce client."""

from types import SimpleNamespace
from typing import Any

import pytest
from conftest import AUTH
from fastapi.testclient import TestClient
from requests import ConnectionError
from simple_salesforce.exceptions import (
    SalesforceExpiredSession,
    SalesforceMalformedRequest,
)

from casehandlersf import salesforce
from casehandlersf.api import app
from casehandlersf.salesforce import add_case_comment, find_case

CASE_ID = "500g800002HiYr3AAF"

# Shaped like a record from simple-salesforce's query() result.
CASE_RECORD = {
    "attributes": {
        "type": "Case",
        "url": f"/services/data/v65.0/sobjects/Case/{CASE_ID}",
    },
    "Id": CASE_ID,
    "CaseNumber": "00001001",
    "Subject": "Performance inadequate for second consecutive week",
    "Description": None,
    "Priority": "High",
    "Status": "Closed",
    "CreatedDate": "2026-07-01T09:15:00.000+0000",
    "ClosedDate": "2026-07-03T17:00:00.000+0000",
}


class FakeSalesforce:
    """Stands in for simple_salesforce.Salesforce; records queries and creates."""

    def __init__(self, records: list[dict[str, Any]] | None = None) -> None:
        self.records = records or []
        self.queries: list[str] = []
        self.created: list[dict[str, Any]] = []
        self.CaseComment = SimpleNamespace(create=self._create_comment)

    def query(self, soql: str) -> dict[str, Any]:
        self.queries.append(soql)
        return {"totalSize": len(self.records), "done": True, "records": self.records}

    def _create_comment(self, fields: dict[str, Any]) -> dict[str, Any]:
        self.created.append(fields)
        return {"id": "00ag800000CommentAAA", "success": True, "errors": []}


class FakeLogin:
    """Replaces the cached _client(): hands out `clients` in order, one per login."""

    def __init__(self, *clients: FakeSalesforce) -> None:
        self.clients = list(clients)
        self.logins = 0

    def __call__(self) -> FakeSalesforce:
        return self.clients[min(self.logins, len(self.clients) - 1)]

    def cache_clear(self) -> None:
        self.logins += 1


@pytest.fixture
def sf(monkeypatch: pytest.MonkeyPatch) -> FakeSalesforce:
    fake = FakeSalesforce([CASE_RECORD])
    monkeypatch.setattr(salesforce, "_client", FakeLogin(fake))
    return fake


def test_find_case_by_case_number(sf: FakeSalesforce) -> None:
    assert find_case("00001001") == CASE_RECORD
    assert sf.queries == [
        (
            f"SELECT {salesforce.CASE_FIELDS} FROM Case "
            "WHERE CaseNumber = '00001001' LIMIT 1"
        )
    ]


@pytest.mark.parametrize("key", [CASE_ID, CASE_ID[:15]])
def test_find_case_by_record_id(sf: FakeSalesforce, key: str) -> None:
    assert find_case(key) == CASE_RECORD
    assert f"WHERE Id = '{key}' LIMIT 1" in sf.queries[0]


def test_find_case_returns_none_when_no_case_matches(sf: FakeSalesforce) -> None:
    sf.records = []
    assert find_case("99999999") is None


@pytest.mark.parametrize(
    "key",
    [
        "500g800002HiYr",  # 14 characters: too short for an Id
        "500g800002HiYr3AAFX",  # 19 characters: too long for an Id
        "001g800002HiYr3AAF",  # an Account Id, not a Case Id
    ],
)
def test_key_that_is_not_a_case_id_is_looked_up_as_case_number(
    sf: FakeSalesforce, key: str
) -> None:
    find_case(key)
    assert f"WHERE CaseNumber = '{key}' LIMIT 1" in sf.queries[0]


def test_quotes_in_key_are_escaped_in_soql(sf: FakeSalesforce) -> None:
    find_case("x' OR Subject != '")
    assert "WHERE CaseNumber = 'x\\' OR Subject != \\'' LIMIT 1" in sf.queries[0]


def test_add_case_comment_sends_fields_and_returns_id(sf: FakeSalesforce) -> None:
    assert add_case_comment(CASE_ID, "Called back.", True) == "00ag800000CommentAAA"
    assert sf.created == [
        {"ParentId": CASE_ID, "CommentBody": "Called back.", "IsPublished": True}
    ]


def test_expired_session_logs_in_again_and_retries(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    expired = FakeSalesforce()

    def reject(soql: str) -> dict[str, Any]:
        raise SalesforceExpiredSession(
            "https://example.my.salesforce.com/services/data/v65.0/query/",
            401,
            "query",
            b"Session expired or invalid",
        )

    expired.query = reject
    fresh = FakeSalesforce([CASE_RECORD])
    login = FakeLogin(expired, fresh)
    monkeypatch.setattr(salesforce, "_client", login)

    assert find_case("00001001") == CASE_RECORD
    assert login.logins == 1
    assert len(fresh.queries) == 1


def test_other_salesforce_errors_are_not_retried(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    broken = FakeSalesforce()

    def reject(fields: dict[str, Any]) -> dict[str, Any]:
        raise SalesforceMalformedRequest(
            "https://example.my.salesforce.com/services/data/v65.0/sobjects/CaseComment/",
            400,
            "CaseComment",
            [{"message": "bad value", "errorCode": "INVALID_FIELD"}],
        )

    broken.CaseComment = SimpleNamespace(create=reject)
    login = FakeLogin(broken)
    monkeypatch.setattr(salesforce, "_client", login)

    with pytest.raises(SalesforceMalformedRequest):
        add_case_comment(CASE_ID, "Hello", False)
    assert login.logins == 0


# Through the HTTP API, with only the Salesforce client faked.
client = TestClient(app, headers=AUTH)


def test_api_get_case_by_record_id(sf: FakeSalesforce) -> None:
    response = client.get(f"/cases/{CASE_ID}")
    assert response.status_code == 200
    assert response.json()["case_number"] == "00001001"
    assert "WHERE Id = " in sf.queries[0]


def test_api_network_error_returns_502(monkeypatch: pytest.MonkeyPatch) -> None:
    offline = FakeSalesforce()

    def fail(soql: str) -> dict[str, Any]:
        raise ConnectionError("connection refused")

    offline.query = fail
    monkeypatch.setattr(salesforce, "_client", FakeLogin(offline))

    response = client.get("/cases/00001001")
    assert response.status_code == 502
    assert response.json() == {"detail": "Salesforce request failed: ConnectionError"}
