# File: tests/test_executor.py
import os
from dotenv import load_dotenv
import pytest
import openai
from agent.executor import execute_tasks

# Load real API key from .env
load_dotenv()

@pytest.fixture(autouse=True)
def stub_openai(monkeypatch):
    class DummyChoice:
        def __init__(self, text):
            self.message = type("M", (), {"content": text})
    class DummyResponse:
        def __init__(self):
            self.choices = [DummyChoice("Result")]
    def fake_create(*args, **kwargs):
        return DummyResponse()
    monkeypatch.setattr(openai.chat.completions, "create", fake_create)

@pytest.fixture
def sample_tasks():
    return ["Task 1", "Task 2"]


def test_execute_tasks_returns_dict(sample_tasks):
    results = execute_tasks(sample_tasks, model="gpt-4")
    assert isinstance(results, dict)
    assert results == {"Task 1": "Result", "Task 2": "Result"}