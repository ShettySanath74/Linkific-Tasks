# Analysis Methodology

## Qualitative comparison
1. Review sources and extract claims about objectives, questions, methods, outputs, evaluation, applications, and limitations.
2. Record source-supported points in `comparison_framework.md`.
3. Compare fields dimension by dimension.
4. Identify overlap and complementary roles.
5. Preserve differing definitions and cite claims in the final report.

## Illustrative case
Use the synthetic marketing dataset to show:
- Prediction perspective: rank customers by estimated response probability.
- Decision perspective: consider expected financial value and a fixed budget.

For each customer: expected revenue = response probability × revenue if response.
For a selected group: expected net value = expected revenue − contact cost.

The script uses a simple greedy heuristic, not a guaranteed global optimum.

## Quality checks
Use the same budget for both approaches; check costs stay within budget; label values as estimates; state assumptions and limitations. The synthetic example illustrates different questions and cannot prove one field is superior.
