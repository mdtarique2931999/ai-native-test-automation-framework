# TestMu SDET-1 Assignment

AI-native QA framework for **Login**, **Dashboard**, and **REST API** regression coverage, with an LLM-powered **Failure Explainer** wired into pytest reports.

## Stack

- Python 3.10+
- Selenium + Chrome
- Pytest + pytest-html
- OpenAI API (Failure Explainer)
- UI target: [Sauce Demo](https://www.saucedemo.com/)
- API targets: [JSONPlaceholder](https://jsonplaceholder.typicode.com/) + [httpbin](https://httpbin.org/)

## Project structure

```
pages/              Page Object Model for Sauce Demo
tests/ui/           Generated login + dashboard tests
tests/api/          Generated REST API tests
test_data/          LLM-generated test cases (JSON)
utils/              Failure Explainer + LLM client
reports/            HTML reports and sample LLM output
prompts.md          Raw prompts used for test generation
ai-usage-log.md     AI tool usage log
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and set:

```env
OPENAI_API_KEY=sk-your-key-here
```

## Run tests

```bash
# All tests
pytest

# UI only
pytest tests/ui -m ui

# API only
pytest tests/api -m api

# HTML report
pytest --html=reports/latest.html --self-contained-html

# Sample Failure Explainer output (needs OPENAI_API_KEY)
pytest tests/test_sample_failure.py -m sample_failure --html=reports/sample_failure_report.html --self-contained-html
```

## Failure Explainer (Task 3)

When a test fails, the pytest hook in `conftest.py`:

1. Collects browser/API context
2. Sends it to OpenAI via `utils/llm_client.py`
3. Attaches the explanation to the pytest-html report
4. Saves output under `reports/llm_explanations/`

See committed sample output in `reports/llm_explanations/sample_failure.txt`.

## What I'd build next

- Flaky Test Classifier as a second LLM pipeline
- Playwright migration for faster, more stable UI tests
- Self-healing locators using LLM-assisted selector recovery
- TestMu cloud grid execution for CI parallel runs

## Author

Md Tarique — TestMu AI SDET-1 Assessment
