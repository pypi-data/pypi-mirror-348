# agent/reporter.py

import os
import re
from datetime import datetime

def sanitize_filename(text):
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', text.strip())[:50]

def generate_report(goal: str, results: dict, output_format="markdown") -> str:
    os.makedirs("reports", exist_ok=True)

    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = sanitize_filename(goal)
    filename = f"reports/{base_name}_{timestamp}.md"

    # Compose Markdown report
    lines = [f"# 🧠 Research Report\n\n", f"## Goal\n{goal}\n\n", "## Findings\n"]
    for i, (task, result) in enumerate(results.items(), 1):
        lines.append(f"### {i}. {task}\n{result}\n")

    report_content = "\n".join(lines)

    # Save file
    with open(filename, "w") as f:
        f.write(report_content)

    print(f"\n📄 Report saved to: {filename}")
    return filename
