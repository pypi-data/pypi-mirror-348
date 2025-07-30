# File: tests/test_planner.py
import os
from dotenv import load_dotenv
import pytest
import openai
from agent.planner import generate_plan

# Load real API key from .env
load_dotenv()

@pytest.fixture(autouse=True)
def stub_openai(monkeypatch):
    # Stub chat.completions.create; preserve real API key
    class DummyChoice:
        def __init__(self, text):
            self.message = type("M", (), {"content": text})
    class DummyResponse:
        def __init__(self):
            self.choices = [DummyChoice("- Subtask A\n- Subtask B")]
    def fake_create(*args, **kwargs):
        return DummyResponse()
    monkeypatch.setattr(openai.chat.completions, "create", fake_create)


def test_generate_plan_returns_list():
    goal = "Test goal for unit testing"
    plan = generate_plan(goal, model="gpt-4")
    assert isinstance(plan, list)
    assert plan == ["Subtask A", "Subtask B"]