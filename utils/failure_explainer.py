"""
Option A: Failure Explainer

We chose this over the Flaky Test Classifier because immediate, per-test
explanations shorten debug time during regression runs. A flaky classifier
is useful at scale, but for this assignment a real-time explainer attached
to pytest-html reports shows clearer LLM integration value.
"""

import os

from utils.context_collector import collect_failure_context
from utils.llm_client import explain_failure


def build_and_explain(item, report, driver=None, api_response=None):
    context = collect_failure_context(item, report, driver, api_response)
    explanation = explain_failure(context)

    reports_dir = os.path.join(os.getcwd(), "reports", "llm_explanations")
    os.makedirs(reports_dir, exist_ok=True)

    safe_name = item.nodeid.replace("/", "_").replace("::", "__")
    output_path = os.path.join(reports_dir, f"{safe_name}.txt")
    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write("=== Failure Context ===\n")
        handle.write(context)
        handle.write("\n\n=== LLM Explanation ===\n")
        handle.write(explanation)

    return explanation, output_path
