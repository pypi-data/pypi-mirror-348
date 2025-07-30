# File: tests/test_reporter.py
import os
import re
import pytest
from agent.reporter import sanitize_filename, generate_report


def test_sanitize_filename_removes_bad_chars():
    name = sanitize_filename("Invalid:/Name?*")
    assert re.match(r'^[A-Za-z0-9_\-]+$', name)


def test_generate_report_creates_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    goal = "Sample Goal"
    results = {"Task": "Result"}
    report_path = generate_report(goal, results)
    assert os.path.exists(report_path)
    with open(report_path) as f:
        content = f.read()
        assert "# 🧠 Research Report" in content
