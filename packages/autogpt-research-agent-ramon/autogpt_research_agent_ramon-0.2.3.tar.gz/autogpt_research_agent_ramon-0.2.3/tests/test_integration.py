# tests/test_integration.py

import os
from pathlib import Path
import pytest
from dotenv import load_dotenv

from agent.planner import generate_plan
from agent.executor import execute_tasks
from agent.memory import save_results, load_memory
from agent.reporter import generate_report

# Load your real API key
load_dotenv()

# ─── Stub out OpenAI so no real HTTP calls ────────────────────────────────
@pytest.fixture(autouse=True)
def stub_openai(monkeypatch):
    import openai
    class DummyChoice:
        def __init__(self, content):
            self.message = type("M", (), {"content": content})
    class DummyResponse:
        def __init__(self, content):
            self.choices = [DummyChoice(content)]
    def fake_create(*args, **kwargs):
        # Echo back the last user prompt
        last = kwargs["messages"][-1]["content"]
        return DummyResponse(f"Echo: {last}")
    monkeypatch.setenv("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
    monkeypatch.setattr(openai.chat.completions, "create", fake_create)
# ─────────────────────────────────────────────────────────────────────────

def test_full_agent_pipeline(tmp_path, monkeypatch):
    # Redirect memory and reports to a temp directory
    monkeypatch.setenv("MEMORY_PATH", str(tmp_path / "memory.json"))
    monkeypatch.chdir(tmp_path)

    goal = "Test integration goal"

    # 1. Plan
    plan = generate_plan(goal)
    assert isinstance(plan, list) and plan, "Planner must return a non-empty list"

    # 2. Execute
    results = execute_tasks(plan)
    assert all(isinstance(r, str) for r in results.values()), "Executor must return strings"

    # 3. Memory
    save_results(goal, results)
    mem = load_memory()
    assert mem[-1]["goal"] == goal

    # 4. Report
    report_path = generate_report(goal, results)
    assert report_path.endswith(".md") and os.path.exists(report_path)

    # 5. Read and verify content
    with open(report_path, "r") as f:
        content = f.read()
    assert "# 🧠 Research Report" in content
