import asyncio
import json
from types import SimpleNamespace

import pytest
from test_mcp_server import CASE, FakeSearcher

from casehandlersf import agent, mcp_server


def text(value: str) -> SimpleNamespace:
    return SimpleNamespace(type="text", text=value)


def tool_use(id: str, name: str, **arguments) -> SimpleNamespace:
    return SimpleNamespace(type="tool_use", id=id, name=name, input=arguments)


class ScriptedClaude:
    """Replies with the next scripted turn on each call. With tools switched off
    (tool_choice none), it answers instead, as the API would."""

    def __init__(self, *turns: tuple[str, list]) -> None:
        self.turns = list(turns)
        self.calls: list[dict] = []
        self.beta = SimpleNamespace(messages=SimpleNamespace(create=self._create))

    async def _create(self, **kwargs):
        self.calls.append({**kwargs, "messages": list(kwargs["messages"])})
        if kwargs["tool_choice"] == {"type": "none"}:
            return response("end_turn", [text("Best I can say.")])
        return response(*self.turns.pop(0))


def response(stop_reason: str, content: list) -> SimpleNamespace:
    return SimpleNamespace(
        stop_reason=stop_reason,
        content=content,
        model=agent.MODEL,
        usage=SimpleNamespace(input_tokens=1200, output_tokens=80),
    )


@pytest.fixture(autouse=True)
def written(monkeypatch: pytest.MonkeyPatch) -> list[tuple[str, str, bool]]:
    """Fake Salesforce and knowledge base. Returns the comments written to Salesforce."""
    searcher = FakeSearcher()
    monkeypatch.setattr(mcp_server.knowledge, "searcher", lambda: searcher)
    monkeypatch.setattr(
        mcp_server, "find_case", lambda key: CASE if key == "00001001" else None
    )
    calls: list[tuple[str, str, bool]] = []

    def add(case_id: str, body: str, is_published: bool) -> str:
        calls.append((case_id, body, is_published))
        return "00ag800000CommentAAA"

    monkeypatch.setattr(mcp_server, "add_case_comment", add)
    return calls


class Person:
    """Answers approval requests from a script, and records what it was shown."""

    def __init__(self, *decisions: agent.Decision) -> None:
        self.decisions = list(decisions)
        self.shown: list[tuple[str, dict]] = []

    def __call__(self, name: str, arguments: dict) -> agent.Decision:
        self.shown.append((name, dict(arguments)))
        return self.decisions.pop(0)


def run(
    claude: ScriptedClaude,
    max_steps: int = agent.MAX_STEPS,
    approve: agent.Approver = agent.reject_all,
) -> agent.AgentResult:
    return asyncio.run(
        agent.run_agent("Help with 00001001", claude, max_steps, approve)
    )


def update(id: str, comment: str) -> SimpleNamespace:
    return tool_use(id, "update_case", case_key="00001001", comment=comment)


def test_picks_tools_until_it_can_answer() -> None:
    claude = ScriptedClaude(
        ("tool_use", [tool_use("t1", "get_case", case_key="00001001")]),
        ("tool_use", [tool_use("t2", "search_knowledge", query="edits late", top_k=2)]),
        ("end_turn", [text("Their proxy blocks WebSockets [KA-0029].")]),
    )
    result = run(claude)

    assert result.answer == "Their proxy blocks WebSockets [KA-0029]."
    assert result.steps == 3
    assert result.stop_reason == "end_turn"
    assert [(c.step, c.name, c.is_error) for c in result.tool_calls] == [
        (1, "get_case", False),
        (2, "search_knowledge", False),
    ]
    # Claude sees all three MCP tools.
    assert {t["name"] for t in claude.calls[0]["tools"]} == {
        "get_case",
        "search_knowledge",
        "draft_reply",
        "update_case",
    }
    # The tool result goes back in a user turn, matched to the tool_use id.
    second_call = claude.calls[1]["messages"]
    assert [m["role"] for m in second_call] == ["user", "assistant", "user"]
    result_block = second_call[2]["content"][0]
    assert result_block["tool_use_id"] == "t1"
    assert "00001001" in result_block["content"]
    assert result_block["is_error"] is False


def test_runs_parallel_tool_calls_and_replies_once() -> None:
    claude = ScriptedClaude(
        (
            "tool_use",
            [
                text("Looking both up."),
                tool_use("a", "get_case", case_key="00001001"),
                tool_use("b", "search_knowledge", query="edits late"),
            ],
        ),
        ("end_turn", [text("Done.")]),
    )
    run(claude)

    results = claude.calls[1]["messages"][2]["content"]
    assert [r["tool_use_id"] for r in results] == ["a", "b"]


def test_tool_errors_go_back_to_claude() -> None:
    claude = ScriptedClaude(
        ("tool_use", [tool_use("t1", "get_case", case_key="00009999")]),
        ("end_turn", [text("That case doesn't exist.")]),
    )
    result = run(claude)

    assert result.tool_calls[0].is_error
    result_block = claude.calls[1]["messages"][2]["content"][0]
    assert result_block["is_error"] is True
    assert "not found" in result_block["content"]


def test_stops_at_max_steps_and_forces_an_answer() -> None:
    always_searching = [
        ("tool_use", [tool_use(f"t{i}", "search_knowledge", query="more")])
        for i in range(10)
    ]
    claude = ScriptedClaude(*always_searching)
    result = run(claude)

    assert len(claude.calls) == agent.MAX_STEPS == 5
    assert [c["tool_choice"]["type"] for c in claude.calls] == ["auto"] * 4 + ["none"]
    assert len(result.tool_calls) == 4
    assert result.answer == "Best I can say."
    assert result.steps == 5


def test_refusal() -> None:
    claude = ScriptedClaude(("refusal", []))
    result = run(claude)
    assert result.stop_reason == "refusal"
    assert result.answer == "[Claude declined to answer]"


def test_write_runs_only_after_approval(written: list) -> None:
    claude = ScriptedClaude(
        ("tool_use", [update("u1", "Called the customer.")]),
        ("end_turn", [text("Comment added.")]),
    )
    person = Person(agent.Decision(True))
    result = run(claude, approve=person)

    # The person saw the exact arguments that were then written.
    assert person.shown == [
        ("update_case", {"case_key": "00001001", "comment": "Called the customer."})
    ]
    assert written == [(CASE["Id"], "Called the customer.", False)]
    assert result.tool_calls[0].approved is True
    assert not result.tool_calls[0].is_error


def test_rejection_feedback_goes_back_and_claude_revises(written: list) -> None:
    claude = ScriptedClaude(
        ("tool_use", [update("u1", "Hi, fixed.")]),
        ("tool_use", [update("u2", "Hi, we allowlisted the domain. Please retry.")]),
        ("end_turn", [text("Comment added after revision.")]),
    )
    person = Person(agent.Decision(False, "Say what we changed"), agent.Decision(True))
    result = run(claude, approve=person)

    rejection = claude.calls[1]["messages"][2]["content"][0]
    assert rejection["is_error"] is True
    assert "nothing was written" in rejection["content"]
    assert "Say what we changed" in rejection["content"]
    # Only the approved revision reached Salesforce.
    assert written == [
        (CASE["Id"], "Hi, we allowlisted the domain. Please retry.", False)
    ]
    assert [c.approved for c in result.tool_calls] == [False, True]


def test_without_an_approver_nothing_is_written(written: list) -> None:
    claude = ScriptedClaude(
        ("tool_use", [update("u1", "Called the customer.")]),
        ("end_turn", [text("I couldn't save it.")]),
    )
    result = run(claude)

    assert written == []
    assert result.tool_calls[0].approved is False


def test_read_only_tools_need_no_approval() -> None:
    claude = ScriptedClaude(
        ("tool_use", [tool_use("t1", "get_case", case_key="00001001")]),
        ("end_turn", [text("Done.")]),
    )
    person = Person()  # Would fail if asked: it has no decisions.
    result = run(claude, approve=person)

    assert person.shown == []
    assert result.tool_calls[0].approved is None


def test_logs_every_model_and_tool_call(tmp_path) -> None:
    log_path = tmp_path / "logs" / "runs.jsonl"
    claude = ScriptedClaude(
        ("tool_use", [tool_use("t1", "get_case", case_key="00001001")]),
        ("tool_use", [update("u1", "Called the customer.")]),
        ("end_turn", [text("Done.")]),
    )
    person = Person(agent.Decision(False, "Too short"))
    result = asyncio.run(
        agent.run_agent("Help with 00001001", claude, approve=person, log_path=log_path)
    )

    records = [json.loads(line) for line in log_path.read_text().splitlines()]
    assert {r["run_id"] for r in records} == {result.run_id}
    assert [r["event"] for r in records] == [
        "run_start",
        "model_call",
        "tool_call",
        "model_call",
        "tool_call",
        "model_call",
        "run_end",
    ]
    get_case, update_case = (r for r in records if r["event"] == "tool_call")
    assert get_case["input"] == {"case_key": "00001001"}
    assert "Edits from teammates arrive late" in get_case["output"]
    assert get_case["approved"] is None
    assert isinstance(get_case["duration_ms"], int)
    assert update_case["approved"] is False
    assert update_case["feedback"] == "Too short"
    assert isinstance(update_case["approval_ms"], int)
    first_call = records[1]
    assert first_call["input_tokens"] == 1200
    assert first_call["tool_uses"] == ["get_case"]
    assert records[-1]["answer"] == "Done."
    assert records[-1]["steps"] == 3


def test_logs_a_failed_run(tmp_path) -> None:
    log_path = tmp_path / "runs.jsonl"
    claude = ScriptedClaude()  # No turns scripted: the first call raises.
    with pytest.raises(IndexError):
        asyncio.run(agent.run_agent("Hi", claude, log_path=log_path))
    last = json.loads(log_path.read_text().splitlines()[-1])
    assert last["event"] == "run_error"
    assert last["error"].startswith("IndexError")
