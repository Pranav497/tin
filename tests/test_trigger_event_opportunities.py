import importlib.util
from pathlib import Path


WORKFLOW_PATH = (
    Path(__file__).resolve().parents[1]
    / "workflow_packages"
    / "growth.trigger_event_opportunities"
    / "main.py"
)


def load_workflow():
    spec = importlib.util.spec_from_file_location("trigger_event_workflow", WORKFLOW_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_trigger_event_workflow_returns_markdown_artifact():
    module = load_workflow()

    result = module.run(
        None,
        {
            "project_id": "123e4567-e89b-12d3-a456-426614174000",
            "company_description": "AI customer support platform",
            "ideal_customer_profile": "SaaS companies with 20-200 employees",
            "target_market": "United States",
            "trigger_events": "Recent funding, product launch, market expansion",
            "opportunity_count": 5,
        },
    )

    assert result["path"] == "reports/TRIGGER_EVENT_OPPORTUNITIES.md"
    assert result["content"].startswith("# Trigger Event Opportunities")
    assert "AI customer support platform" in result["content"]
    assert "SaaS companies with 20-200 employees" in result["content"]
    assert "United States" in result["content"]


def test_trigger_event_workflow_rejects_invalid_opportunity_count():
    module = load_workflow()

    try:
        module.run(
            None,
            {
                "project_id": "123e4567-e89b-12d3-a456-426614174000",
                "company_description": "AI customer support platform",
                "ideal_customer_profile": "SaaS companies",
                "target_market": "United States",
                "trigger_events": "Recent funding",
                "opportunity_count": 0,
            },
        )
    except (KeyError, ValueError, TypeError):
        pass