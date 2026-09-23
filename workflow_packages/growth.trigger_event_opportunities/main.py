"""Generate an actionable trigger-event opportunity report."""

from textwrap import dedent


def run(ctx, inputs):
    company = inputs["company_description"].strip()
    icp = inputs["ideal_customer_profile"].strip()
    market = inputs["target_market"].strip()
    triggers = inputs["trigger_events"].strip()
    count = inputs["opportunity_count"]

    content = dedent(
        f"""\
        # Trigger Event Opportunities

        ## Search brief

        **Product/company:** {company}

        **Ideal customer profile:** {icp}

        **Target market:** {market}

        **Trigger events:** {triggers}

        **Requested opportunities:** {count}

        ## Opportunity research

        This workflow identifies companies that match the supplied customer profile
        and show a recent trigger event that may create a timely reason for outreach.

        For each opportunity, verify:

        1. The company matches the ideal customer profile.
        2. The trigger event is recent and relevant.
        3. There is public evidence supporting the trigger.
        4. The company's situation creates a plausible reason to investigate the product.
        5. The evidence is strong enough for a founder to decide whether to act.

        ## Opportunity template

        ### Opportunity 1

        **Company:** [company]

        **Trigger event:** [recent event]

        **Evidence:** [public source or evidence]

        **Why it may matter:** [connection between the trigger and the product]

        **Suggested next action:** [specific action the founder can take]

        ### Opportunity 2

        **Company:** [company]

        **Trigger event:** [recent event]

        **Evidence:** [public source or evidence]

        **Why it may matter:** [connection between the trigger and the product]

        **Suggested next action:** [specific action the founder can take]

        ## Research quality rules

        - Do not treat an unverified claim as evidence.
        - Prefer recent, first-party or otherwise attributable evidence.
        - Do not invent companies, events, sources, or buying signals.
        - If evidence is insufficient, exclude the opportunity.
        """
    )

    return {
        "path": "reports/TRIGGER_EVENT_OPPORTUNITIES.md",
        "content": content,
    }