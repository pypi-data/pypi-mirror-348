# agent/planner.py

import os
import re
import openai

def generate_plan(goal: str, model: str = "gpt-4") -> list[str]:
    """
    Decompose the user goal into 3–7 clear, independent subtasks using the OpenAI v1 API.
    Leading numbers or bullets in GPT’s response are removed for clean task names.
    """
    # Load API key
    openai.api_key = os.getenv("OPENAI_API_KEY")

    prompt = (
        "You are a research planner AI. Break down the following research goal "
        "into 3 to 7 clear and independent subtasks. Each subtask should be actionable "
        "and **do not** include numbering or bullets in your final list:\n\n"
        f"Research Goal: {goal}\n\n"
        "Subtasks:"
    )

    response = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system",  "content": "You are a helpful AI assistant."},
            {"role": "user",    "content": prompt}
        ],
        temperature=0.4
    )

    raw_content = response.choices[0].message.content
    # Split into lines and strip common list markers
    lines = [line.strip() for line in raw_content.splitlines() if line.strip()]
    # Remove any leading bullets or numbers (e.g., "1. ", "2) ", "- ")
    tasks = [re.sub(r"^[\-\d\.\)]+\s*", "", line) for line in lines]

    return tasks
