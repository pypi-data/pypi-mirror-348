# File: tests/test_memory.py
import os
import json
import pytest
from agent.memory import save_results, load_memory


def test_save_and_load_memory(tmp_path, monkeypatch):
    monkeypatch.setenv("MEMORY_PATH", str(tmp_path / "memory.json"))
    save_results("G", {"T": "R"})
    data = load_memory()
    assert isinstance(data, list)
    assert data[-1]["goal"] == "G"