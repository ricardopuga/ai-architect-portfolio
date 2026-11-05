from pathlib import Path
from types import SimpleNamespace

import botocore.exceptions
import pytest
from conftest import AUTH
from fastapi.testclient import TestClient
from pydantic import ValidationError
from simple_salesforce.exceptions import (
    SalesforceAuthenticationFailed,
    SalesforceRefusedRequest,
)

from casehandlersf import api, bedrock_knowledge
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


# --- POST /cases/{key}/suggested-reply ---

KB_CHUNKS = [
    bedrock_knowledge.Chunk(
        "KA-0029", "Real-time changes appear with a delay", "Proxy blocks WebSockets."
    ),
    bedrock_knowledge.Chunk("KA-0012", "Network requirements", "Allow wss://rt."),
]


class FakeClaude:
    def __init__(self, text: str = "", stop_reason: str = "end_turn") -> None:
        self.calls: list[dict] = []
        self.response = SimpleNamespace(
            stop_reason=stop_reason, content=[SimpleNamespace(type="text", text=text)]
        )
        self.beta = SimpleNamespace(messages=SimpleNamespace(create=self._create))

    def _create(self, **kwargs):
        self.calls.append(kwargs)
        return self.response


@pytest.fixture
def kb_queries(monkeypatch: pytest.MonkeyPatch) -> list[tuple[str, int]]:
    queries: list[tuple[str, int]] = []

    def fake_search(query: str, k: int = 5) -> list[bedrock_knowledge.Chunk]:
        queries.append((query, k))
        return KB_CHUNKS[:k]

    monkeypatch.setattr(api.bedrock_knowledge, "search", fake_search)
    return queries


def fake_claude(monkeypatch: pytest.MonkeyPatch, **kwargs) -> FakeClaude:
    fake = FakeClaude(**kwargs)
    monkeypatch.setattr(api, "_claude", lambda: fake)
    return fake


def test_suggested_reply(monkeypatch: pytest.MonkeyPatch, kb_queries: list) -> None:
    fake = fake_claude(
        monkeypatch,
        text="Hi,\nYour proxy blocks WebSockets [KA-0029] [KA-9999].\nThe Support team",
    )
    response = client.post(
        "/cases/00001002/suggested-reply", json={"guidance": "Be brief"}
    )

    assert response.status_code == 200
    case = FAKE_RECORDS["00001002"]
    # Search uses the Case's subject and description.
    assert kb_queries == [(f"{case['Subject']}\n{case['Description']}", 5)]
    prompt = fake.calls[0]["messages"][0]["content"]
    assert '<article id="KA-0029">' in prompt
    assert "<agent_guidance>\nBe brief\n</agent_guidance>" in prompt
    assert response.json() == {
        "case_number": "00001002",
        "reply": "Hi,\nYour proxy blocks WebSockets [KA-0029] [KA-9999].\nThe Support team",
        "sources": [{"article_number": "KA-0029", "title": KB_CHUNKS[0].title}],
        "unknown_citations": ["KA-9999"],
    }


def test_suggested_reply_without_body(
    monkeypatch: pytest.MonkeyPatch, kb_queries: list
) -> None:
    fake = fake_claude(monkeypatch, text="Hi")
    assert client.post("/cases/00001002/suggested-reply").status_code == 200
    assert "<agent_guidance>" not in fake.calls[0]["messages"][0]["content"]


def test_suggested_reply_needs_api_key(kb_queries: list) -> None:
    response = TestClient(app).post("/cases/00001002/suggested-reply")
    assert response.status_code == 401
    assert kb_queries == []


def test_suggested_reply_unknown_case(kb_queries: list) -> None:
    assert client.post("/cases/00009999/suggested-reply").status_code == 404
    assert kb_queries == []


def test_suggested_reply_rejects_too_long_guidance(kb_queries: list) -> None:
    response = client.post(
        "/cases/00001002/suggested-reply", json={"guidance": "x" * 2001}
    )
    assert response.status_code == 422


def test_suggested_reply_refusal_returns_502(
    monkeypatch: pytest.MonkeyPatch, kb_queries: list
) -> None:
    fake_claude(monkeypatch, stop_reason="refusal")
    response = client.post("/cases/00001002/suggested-reply")
    assert response.status_code == 502
    assert "declined" in response.json()["detail"]


def test_suggested_reply_search_failure_returns_502(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail(query: str, k: int = 5):
        raise botocore.exceptions.ClientError(
            {"Error": {"Code": "AccessDeniedException", "Message": "no"}}, "Retrieve"
        )

    monkeypatch.setattr(api.bedrock_knowledge, "search", fail)
    response = client.post("/cases/00001002/suggested-reply")
    assert response.status_code == 502
    assert response.json()["detail"] == "Knowledge base search failed: ClientError"


def test_suggested_reply_without_kb_settings_returns_503(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.chdir(tmp_path)  # away from the project's .env
    monkeypatch.delenv("BEDROCK_KB_ID", raising=False)
    bedrock_knowledge._client.cache_clear()
    try:
        response = client.post("/cases/00001002/suggested-reply")
    finally:
        bedrock_knowledge._client.cache_clear()
    assert response.status_code == 503


def test_bedrock_result_to_chunk() -> None:
    result = {
        "content": {
            "text": '---\narticle_number: KA-0029\ntitle: "Real-time collaboration delay"\n---\n## Cause'
        },
        "metadata": {"_document_title": "KA-0029-realtime-collaboration-delay.md"},
    }
    chunk = bedrock_knowledge.to_chunk(result)
    assert (chunk.article_number, chunk.title) == (
        "KA-0029",
        "Real-time collaboration delay",
    )

    # A chunk from the middle of an article has no front matter: the title comes from the file name.
    middle = {
        "content": {"text": "Allow WebSockets to rt.lumora.example."},
        "metadata": {
            "_source_uri": "s3://bucket/articles/KA-0029-realtime-collaboration-delay.md",
            "_document_title": "KA-0029-realtime-collaboration-delay.md",
        },
    }
    chunk = bedrock_knowledge.to_chunk(middle)
    assert (chunk.article_number, chunk.title) == (
        "KA-0029",
        "Realtime collaboration delay",
    )


def test_suggested_reply_keeps_title_of_best_chunk(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    chunks = [
        bedrock_knowledge.Chunk("KA-0029", "Real-time collaboration delay", "Cause."),
        bedrock_knowledge.Chunk("KA-0029", "realtime collaboration delay", "Fix."),
    ]
    monkeypatch.setattr(api.bedrock_knowledge, "search", lambda q, k=5: chunks)
    fake_claude(monkeypatch, text="Fix it [KA-0029].")
    sources = client.post("/cases/00001002/suggested-reply").json()["sources"]
    assert sources == [
        {"article_number": "KA-0029", "title": "Real-time collaboration delay"}
    ]
