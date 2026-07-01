# AI Usage Log

| Tool | Task | What I used it for | What it produced |
|------|------|--------------------|------------------|
| Cursor (Claude) | Task 1 — Scaffold | Project structure, page objects, pytest fixtures, git setup | Selenium + Pytest framework with POM layout |
| Cursor (Claude) | Task 2 — Prompts | Drafting structured prompts for Login, Dashboard, API modules | Raw prompts in `prompts.md` and JSON cases in `test_data/` |
| Cursor (Claude) | Task 2 — Tests | Converting generated cases into executable pytest tests | UI tests in `tests/ui/`, API tests in `tests/api/` |
| Cursor (Claude) | Task 3 — Failure Explainer | LLM hook, context collector, pytest-html attachment | `utils/failure_explainer.py`, `utils/llm_client.py`, sample output |
| Cursor (Claude) | Documentation | README, ai-usage-log, assignment notes | Run instructions and submission docs |

## First commit note

Initial framework structure and test implementation were scaffolded with **Cursor (Claude Agent)** to accelerate boilerplate setup, page object patterns, and pytest wiring.
