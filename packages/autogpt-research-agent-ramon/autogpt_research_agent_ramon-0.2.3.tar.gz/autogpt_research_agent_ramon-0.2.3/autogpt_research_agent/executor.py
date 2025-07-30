# agent/executor.py

import os
import openai

def execute_tasks(tasks: list, model="gpt-4") -> dict:
    """
    For each subtask, ask GPT to research and return a concise result.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")
    results = {}

    for task in tasks:
        print(f"\n🔍 Executing task: {task}")

        prompt = (
            f"You are a research assistant. Provide a detailed but concise explanation "
            f"for the following subtask:\n\n{task}\n\n"
            "Keep your answer focused and well-structured."
        )

        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system",  "content": "You are a helpful and concise research assistant."},
                {"role": "user",    "content": prompt}
            ],
            temperature=0.5
        )

        results[task] = response.choices[0].message.content.strip()

    return results
