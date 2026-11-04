import asyncio
from pathlib import Path
from types import SimpleNamespace

import jsonschema
import pytest
from mcp.server.mcpserver.exceptions import ToolError
from simple_salesforce.exceptions import SalesforceRefusedRequest

from casehandlersf import mcp_server
from casehandlersf import salesforce as salesforce_module
from casehandlersf.knowledge import BM25, Chunk, tokenize
from casehandlersf.mcp_server import mcp

CASE = {
    "Id": "500g800002HiYr3AAF",
    "CaseNumber": "00001001",
    "Subject": "Edits from teammates arrive late",
    "Description": "Changes show up about 30 seconds after they are made.",
    "Priority": "High",
    "Status": "New",
    "CreatedDate": "2026-07-01T09:15:00.000+0000",
    "ClosedDate": None,
}
CHUNKS = [
    Chunk(
        1,
        "KA-0029",
        "Real-time changes appear with a delay",
        "Cause: proxy blocks WebSockets.",
    ),
    Chunk(2, "KA-0012", "Network requirements", "Allow wss://live.lumora.io."),
]


class FakeSearcher:
    def __init__(self) -> None:
        self.queries: list[tuple[str, int]] = []

    def search(self, question: str, k: int = 5) -> list[Chunk]:
        self.queries.append((question, k))
        return CHUNKS[:k]


class FakeClaude:
    def __init__(self, text: str = "", stop_reason: str = "end_turn") -> None:
        self.calls: list[dict] = []
        self.response = SimpleNamespace(
            stop_reason=stop_reason,
            content=[SimpleNamespace(type="text", text=text)],
        )
        self.beta = SimpleNamespace(messages=SimpleNamespace(create=self._create))

    def _create(self, **kwargs):
        self.calls.append(kwargs)
        return self.response


def call(tool: str, args: dict):
    """Call a tool and check its result against its published output schema, like
    MCP clients such as the Inspector do."""
    result = asyncio.run(mcp.call_tool(tool, args))
    schema = next(
        t for t in asyncio.run(mcp.list_tools()) if t.name == tool
    ).output_schema
    jsonschema.validate(result.structured_content, schema)
    return result


@pytest.fixture
def searcher(monkeypatch: pytest.MonkeyPatch) -> FakeSearcher:
    fake = FakeSearcher()
    monkeypatch.setattr(mcp_server.knowledge, "searcher", lambda: fake)
    return fake


@pytest.fixture
def salesforce(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        mcp_server, "find_case", lambda key: CASE if key == "00001001" else None
    )


def claude(monkeypatch: pytest.MonkeyPatch, **kwargs) -> FakeClaude:
    fake = FakeClaude(**kwargs)
    monkeypatch.setattr(mcp_server, "_claude", lambda: fake)
    return fake


def test_lists_the_tools() -> None:
    tools = {t.name: t for t in asyncio.run(mcp.list_tools())}
    assert tools.keys() == {
        "get_case",
        "search_knowledge",
        "draft_reply",
        "update_case",
    }
    # Only update_case tells clients it changes data.
    assert [n for n, t in tools.items() if not t.annotations.read_only_hint] == [
        "update_case"
    ]


def test_get_case(salesforce: None) -> None:
    result = call("get_case", {"case_key": "00001001"})
    assert result.structured_content["case_number"] == "00001001"
    assert result.structured_content["subject"] == CASE["Subject"]


def test_get_case_not_found(salesforce: None) -> None:
    with pytest.raises(ToolError, match="case 00009999 not found"):
        call("get_case", {"case_key": "00009999"})


def test_get_case_salesforce_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail(key: str) -> None:
        raise SalesforceRefusedRequest("url", 403, "Case", [{"errorCode": "X"}])

    monkeypatch.setattr(mcp_server, "find_case", fail)
    with pytest.raises(ToolError, match="SalesforceRefusedRequest"):
        call("get_case", {"case_key": "00001001"})


def test_search_knowledge(searcher: FakeSearcher) -> None:
    result = call("search_knowledge", {"query": "edits arrive late", "top_k": 1})
    assert searcher.queries == [("edits arrive late", 1)]
    assert result.structured_content["result"] == [
        {
            "article_number": "KA-0029",
            "title": CHUNKS[0].title,
            "content": CHUNKS[0].content,
        }
    ]


def test_search_knowledge_rejects_bad_top_k(searcher: FakeSearcher) -> None:
    with pytest.raises(ToolError):
        call("search_knowledge", {"query": "x", "top_k": 0})


def test_draft_reply(
    monkeypatch: pytest.MonkeyPatch, salesforce: None, searcher: FakeSearcher
) -> None:
    fake = claude(
        monkeypatch,
        text="Hi,\nYour proxy blocks WebSockets [KA-0029]. See [KA-9999].\nThe Support team",
    )
    result = call("draft_reply", {"case_key": "00001001", "guidance": "Be brief"})

    # Retrieval uses the Case's subject and description.
    assert searcher.queries == [(f"{CASE['Subject']}\n{CASE['Description']}", 5)]
    prompt = fake.calls[0]["messages"][0]["content"]
    assert '<article id="KA-0029">' in prompt
    assert f"Subject: {CASE['Subject']}" in prompt
    assert "<agent_guidance>\nBe brief\n</agent_guidance>" in prompt

    draft = result.structured_content
    assert draft["case_number"] == "00001001"
    assert draft["reply"].startswith("Hi,")
    assert draft["sources"] == [{"article_number": "KA-0029", "title": CHUNKS[0].title}]
    assert draft["unknown_citations"] == ["KA-9999"]


def test_draft_reply_refusal(
    monkeypatch: pytest.MonkeyPatch, salesforce: None, searcher: FakeSearcher
) -> None:
    claude(monkeypatch, stop_reason="refusal")
    with pytest.raises(ToolError, match="declined"):
        call("draft_reply", {"case_key": "00001001"})


def test_draft_reply_case_not_found(salesforce: None, searcher: FakeSearcher) -> None:
    with pytest.raises(ToolError, match="not found"):
        call("draft_reply", {"case_key": "00009999"})
    assert searcher.queries == []


def test_tokenize_keeps_joined_terms_and_parts() -> None:
    assert tokenize("X-Lumora-Signature") == [
        "x-lumora-signature",
        "x",
        "lumora",
        "signature",
    ]


def test_bm25_prefers_matching_chunk() -> None:
    scores = BM25(["websocket proxy blocked", "invoice billing export"]).scores(
        "proxy websocket"
    )
    assert scores[0] > scores[1] == 0


def test_draft_reply_without_claude_credentials(
    monkeypatch: pytest.MonkeyPatch, salesforce: None, searcher: FakeSearcher
) -> None:
    def no_credentials(**kwargs):
        raise TypeError("Could not resolve authentication method. Expected one of ...")

    fake = claude(monkeypatch)
    fake.beta.messages.create = no_credentials
    with pytest.raises(ToolError, match="ANTHROPIC_API_KEY"):
        call("draft_reply", {"case_key": "00001001"})


def test_get_case_without_salesforce_settings(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    for name in ("SF_DOMAIN_URL", "SF_CLIENT_ID", "SF_CLIENT_SECRET"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.chdir(tmp_path)  # No .env here, as when started from the wrong folder.
    salesforce_module._client.cache_clear()
    try:
        with pytest.raises(
            ToolError, match="SF_DOMAIN_URL, SF_CLIENT_ID, SF_CLIENT_SECRET"
        ):
            call("get_case", {"case_key": "00001001"})
    finally:
        salesforce_module._client.cache_clear()


@pytest.fixture
def written(monkeypatch: pytest.MonkeyPatch) -> list[tuple[str, str, bool]]:
    """Records add_case_comment calls instead of writing to Salesforce."""
    calls: list[tuple[str, str, bool]] = []

    def add(case_id: str, body: str, is_published: bool) -> str:
        calls.append((case_id, body, is_published))
        return "00ag800000CommentAAA"

    monkeypatch.setattr(mcp_server, "add_case_comment", add)
    return calls


def test_update_case(salesforce: None, written: list) -> None:
    result = call(
        "update_case", {"case_key": "00001001", "comment": "  Called the customer.  "}
    )
    assert written == [(CASE["Id"], "Called the customer.", False)]
    assert result.structured_content == {
        "comment_id": "00ag800000CommentAAA",
        "case_number": "00001001",
        "is_published": False,
    }


def test_update_case_refuses_citations_for_the_customer(
    salesforce: None, written: list
) -> None:
    args = {
        "case_key": "00001001",
        "comment": "Allowlist it [KA-0004].",
        "is_published": True,
    }
    with pytest.raises(ToolError, match="remove the \\[KA-xxxx\\] citations"):
        call("update_case", args)
    assert written == []
    # Internal comments may keep them.
    call("update_case", {**args, "is_published": False})
    assert len(written) == 1


def test_update_case_not_found(salesforce: None, written: list) -> None:
    with pytest.raises(ToolError, match="not found"):
        call("update_case", {"case_key": "00009999", "comment": "Hi"})
    assert written == []


def test_update_case_salesforce_refuses(
    monkeypatch: pytest.MonkeyPatch, salesforce: None
) -> None:
    def refuse(case_id: str, body: str, is_published: bool) -> str:
        raise SalesforceRefusedRequest(
            "url", 403, "CaseComment", [{"errorCode": "INSUFFICIENT_ACCESS"}]
        )

    monkeypatch.setattr(mcp_server, "add_case_comment", refuse)
    with pytest.raises(ToolError, match="INSUFFICIENT_ACCESS"):
        call("update_case", {"case_key": "00001001", "comment": "Hi"})
