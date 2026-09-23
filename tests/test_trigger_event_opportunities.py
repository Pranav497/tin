import asyncio
import importlib.util
from pathlib import Path


WORKFLOW_PATH = (
    Path(__file__).resolve().parents[1]
    / "workflow_packages"
    / "growth.trigger_event_opportunities"
    / "main.py"
)


def load_workflow():
    spec = importlib.util.spec_from_file_location(
        "trigger_event_workflow", WORKFLOW_PATH
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FakeModels:
    async def generate(self, **kwargs):
        assert kwargs["route"] == "prioritize"
        assert kwargs["step"] == "prioritize_trigger_events"
        assert kwargs["output_schema"]["required"] == ["opportunities"]

        return {
            "parsed": {
                "opportunities": [
                    {
                        "company": "Example SaaS",
                        "trigger": "Recent expansion into a new market",
                        "evidence": "Company announcement supplied as evidence",
                        "fit_reason": "Matches the supplied ICP",
                        "priority": "high",
                        "next_action": "Review the announcement and prepare a targeted outreach brief",
                    }
                ]
            }
        }


class FakeContext:
    models = FakeModels()


def test_trigger_event_workflow_returns_actionable_artifact():
    module = load_workflow()

    result = asyncio.run(
        module.run(
            FakeContext(),
            {
                "project_id": "123e4567-e89b-12d3-a456-426614174000",
                "company_description": "AI customer support platform",
                "ideal_customer_profile": "SaaS companies with 20-200 employees",
                "target_market": "United States",
                "candidate_companies": (
                    "Company: Example SaaS\n"
                    "Trigger: Recent expansion\n"
                    "Evidence: Company announcement"
                ),
                "opportunity_count": 5,
            },
        )
    )

    assert result["path"] == "reports/TRIGGER_EVENT_OPPORTUNITIES.md"
    assert "Example SaaS" in result["content"]
    assert "HIGH" in result["content"]
    assert "Next action" in result["content"]


def test_model_output_is_used_as_the_decision_artifact():
    module = load_workflow()

    result = asyncio.run(
        module.run(
            FakeContext(),
            {
                "project_id": "123e4567-e89b-12d3-a456-426614174000",
                "company_description": "B2B analytics platform",
                "ideal_customer_profile": "Growing SaaS companies",
                "target_market": "United States",
                "candidate_companies": (
                    "Company: Test Company\n"
                    "Trigger: Raised funding\n"
                    "Evidence: Funding announcement"
                ),
                "opportunity_count": 1,
            },
        )
    )

    assert "Test Company" not in result["content"]
    assert "Example SaaS" in result["content"]
