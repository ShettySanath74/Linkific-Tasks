# User Guide – Sales Performance Dashboard

## Purpose
This guide explains how to use the project's Power BI dashboard. Update page names, slicers, and KPI definitions to match the actual PBIX file.

## Opening the dashboard
1. Open Power BI Desktop.
2. Open `Day 28/powerbi/Day28_Business_Intelligence_Dashboard.pbix`.
3. If prompted, verify data-source paths and credentials.
4. Refresh only when the source data and refresh configuration are ready.

## Using the report
1. Review the overview KPIs and confirm the reporting period.
2. Use available slicers to filter the report.
3. Select chart elements to cross-filter other visuals where interactions are configured.
4. Hover over visuals to inspect tooltips.
5. Use reset/clear-filter controls if the report provides them.
6. Export data only where permitted and appropriate.

## Interpreting results
- Check metric definitions and units before comparing values.
- Compare like-for-like periods.
- Distinguish totals from averages and counts.
- Confirm whether cancelled, returned, or incomplete transactions are included.

## Troubleshooting
| Symptom | Suggested action |
|---|---|
| Data source not found | Verify file path and refresh configuration |
| Refresh error | Read the full Power BI error and validate source access |
| Blank visual | Check filters, relationships, and measure logic |
| Unexpected totals | Reconcile with source data and SQL/Python calculation |
| Slow report | Record slow page/visual and inspect model, measures, and visuals |

## Known limitations
Record actual limitations discovered during final testing. Do not claim that all filters, refreshes, or exports work until tested.
