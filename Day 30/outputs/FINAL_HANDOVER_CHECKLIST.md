# Final Handover Checklist

## Repository structure
- [ ] `Day 28/` source data, SQL, notebook, outputs, and Power BI assets are present.
- [ ] `Day 29/` validation scripts, tests, reports, documentation, and presentation materials are present.
- [ ] Extract this package as `Day 30/` in the repository root.

## Local execution
- [ ] Run `python ".\Day 30\scripts\project_audit.py" --root "."`.
- [ ] Run `python -m unittest discover -s ".\Day 30\tests" -v`.
- [ ] Re-run `python -m unittest discover -s ".\Day 29\tests" -v`.
- [ ] Re-run the Day 29 data-quality validation script if source files have changed.
- [ ] Inspect SQL query plans and repeat benchmarks if indexes are changed.

## Manual review
- [ ] Open the PBIX in Power BI Desktop.
- [ ] Verify relationships, measures, visuals, slicers, and refresh behavior.
- [ ] Review presentation slides in PowerPoint.
- [ ] Confirm that all metric labels use generic currency units (CU).
- [ ] Confirm that no unverified Airflow or production claims remain.

## Submission
- [ ] Update tracker row with actual status.
- [ ] Review `git status` and stage only `Day 30/`.
- [ ] Inspect staged changes before committing.
- [ ] Commit and push only after local review.
