# agent/memory.py

import os
import json

# Allow override via environment for testing
MEMORY_PATH = os.getenv("MEMORY_PATH", "data/memory.json")

def save_results(goal: str, results: dict):
    os.makedirs(os.path.dirname(MEMORY_PATH), exist_ok=True)

    entry = {"goal": goal, "results": results}

    if os.path.exists(MEMORY_PATH):
        with open(MEMORY_PATH, "r") as f:
            memory = json.load(f)
    else:
        memory = []

    memory.append(entry)

    with open(MEMORY_PATH, "w") as f:
        json.dump(memory, f, indent=2)

def load_memory() -> list:
    if os.path.exists(MEMORY_PATH):
        with open(MEMORY_PATH, "r") as f:
            return json.load(f)
    return []
