import pytest


@pytest.mark.sample_failure
def test_intentional_failure_for_explainer_demo():
    """Run with OPENAI_API_KEY set to produce a sample LLM explanation."""
    assert 1 == 2, "Demo failure for Failure Explainer report attachment"
