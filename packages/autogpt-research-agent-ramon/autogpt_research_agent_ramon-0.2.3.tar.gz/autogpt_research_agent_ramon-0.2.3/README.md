[![CI](https://github.com/ramonbnuezjr/autogpt-research-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/ramonbnuezjr/autogpt-research-agent/actions/workflows/ci.yml)

# Autonomous Research Agent

A modular AI pipeline that plans, executes, stores memory, and reports research—all orchestrated by `main.py`.

---

## 🚀 Features

- **Planner**: Breaks a research goal into actionable subtasks  
- **Executor**: Uses an LLM to research each subtask  
- **Memory**: Persists session results locally (or vector store)  
- **Reporter**: Generates a Markdown report of findings  
- **Fully Tested**: Unit and integration tests with pytest  

---

## 📦 Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/ramonbnuezjr/autogpt-research-agent.git
   cd autogpt-research-agent
   ```

2. Copy and configure your environment:
   ```bash
   cp .env.example .env
   # Edit `.env` to set your OpenAI API key and backend
   ```

3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🧠 Usage

Run the agent from the CLI:

```bash
python main.py --goal "How is AI being used in smart cities?"
```

*Note: If not using CLI flags yet, just run `python main.py` and input the goal interactively.*

---

## 📝 Sample Report

We’ve saved the latest research report in the `reports/` folder.

Example:
- [`How_are_AI_agents_similar_to_new_species_20250512_184941.md`](reports/How_are_AI_agents_similar_to_new_species_20250512_184941.md)

Browse the full folder:
- [📁 `reports/`](reports/)

---

## ✅ Testing

We use **pytest** for all tests.

1. Install test dependencies:
   ```bash
   pip install pytest
   ```

2. Run all tests:
   ```bash
   pytest
   ```

3. (Optional) Enable live API testing:
   ```bash
   export LIVE_API=true
   pytest -m live
   ```

---

## 🔐 API Key Setup

This project requires access to an LLM (e.g., OpenAI). To run it, you must create a `.env` file using the template provided:

```bash
cp .env.example .env
```

Then edit `.env` with your personal API key:

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
LLM_BACKEND=openai
```

**Never commit `.env` to version control.**

---

## 🧪 CI & Linting

See `.github/workflows/ci.yml` and lint config files in the repo root for continuous integration, formatting, and type checking.
