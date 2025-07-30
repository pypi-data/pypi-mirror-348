from autogpt_research_agent.planner import generate_plan
from autogpt_research_agent.executor import execute_tasks
from autogpt_research_agent.memory import save_results
from autogpt_research_agent.reporter import generate_report

def main():
    import argparse
    import os

    parser = argparse.ArgumentParser(description="Run autonomous research agent")
    parser.add_argument("--goal", type=str, help="Research goal/question")
    args = parser.parse_args()

    goal = args.goal or input("Enter research goal: ")

    plan = generate_plan(goal)
    results = execute_tasks(plan)
    save_results(goal, results)
    generate_report(goal, results)

if __name__ == "__main__":
    main()
