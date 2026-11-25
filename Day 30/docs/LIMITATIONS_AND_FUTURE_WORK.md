# Limitations and Future Work

## Current limitations
- Synthetic training data; not actual company or customer records.
- Currency uses generic units (CU), not INR or another real currency.
- Estimated profit is simplified and excludes shipping, tax, overhead, and refunds.
- Structural CSV validation does not enforce every business-specific rule.
- SQL index changes improved six queries and slowed four; further query-plan investigation is needed.
- Power BI visuals, relationships, filters, and refresh behavior require manual desktop inspection.
- Current documentation does not verify Airflow orchestration, production deployment, or scheduled refresh.

## Suggested future work
1. Add explicit referential-integrity and business-rule validation.
2. Inspect query plans and tune the four regressed SQL queries.
3. Evaluate index write overhead and storage impact.
4. Add repeat-customer, cohort, and category/region profitability analysis.
5. Verify and document Power BI page-level interactions and refresh procedure.
6. Add reproducible run logs and a clear operational runbook.
7. If orchestration is required, implement and test it separately rather than describing it as already present.
