
# Day 15: Data Visualization with Python

## Overview
This project demonstrates data visualization techniques using Matplotlib, Seaborn, and Plotly. It covers basic charts, statistical visualizations, interactive charts, and a multi-chart sales dashboard.

The datasets contain sample training data and do not represent actual business results.

## Learning Objectives
- Create charts using Matplotlib.
- Explore statistical relationships using Seaborn.
- Build interactive charts with Plotly.
- Apply chart selection, labeling, and readability best practices.
- Export charts as image and HTML files.

## Project Structure

```text
Day 15/
├── data/
├── scripts/
│   ├── 02_matplotlib_chart_collection.py
│   ├── 03_seaborn_visualizations.py
│   └── 04_plotly_visualizations.py
├── outputs/
│   ├── matplotlib/
│   ├── seaborn/
│   └── plotly/
├── dashboard/
├── requirements.txt
└── README.md
```

## Libraries
- Matplotlib: static charts and plot customization.
- Seaborn: statistical plots and correlation analysis.
- Plotly: interactive charts and HTML dashboards.
- Pandas: tabular data processing.
- NumPy: numerical operations.

## Chart Guide

| Chart type | Purpose | Recommended use |
|---|---|---|
| Line chart | Show trends over time | Monthly sales |
| Bar chart | Compare categories | Sales by category |
| Scatter plot | Explore relationships | Advertising versus sales |
| Histogram | Show a distribution | Sales values |
| Pie chart | Show part-to-whole proportions | Category sales share |
| Box plot | Summarize spread and outliers | Profit distribution |
| Area chart | Emphasize change over time | Monthly sales |
| Heatmap | Display matrix values | Correlation analysis |
| Violin plot | Compare distributions | Profit by category |
| Pair plot | Explore multiple variable pairs | Sales and profit metrics |
| Regression plot | Show an estimated relationship | Advertising and sales |
| 3D scatter plot | Explore three numerical dimensions | Advertising, sales and profit |
| Animated scatter plot | Explore values across frames | Month-by-month changes |

## Running the Scripts

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Generate Matplotlib charts:

```bash
python scripts/02_matplotlib_chart_collection.py
```

Generate Seaborn charts:

```bash
python scripts/03_seaborn_visualizations.py
```

Generate Plotly charts:

```bash
python scripts/04_plotly_visualizations.py
```

## Output Locations
- Static Matplotlib charts: `outputs/matplotlib/`
- Statistical Seaborn charts: `outputs/seaborn/`
- Interactive Plotly HTML files: `outputs/plotly/`

Open `outputs/plotly/10_sales_dashboard.html` in a browser to explore the interactive dashboard, provided the script has run successfully.

## Visualization Best Practices
1. Choose a chart that fits the question.
2. Use descriptive titles and clear axis labels.
3. Include units where appropriate.
4. Keep colors consistent and distinguishable.
5. Avoid unnecessary 3D effects.
6. Do not distort scales or misrepresent comparisons.
7. Use legends and annotations where they improve understanding.
8. Check missing values and data quality before plotting.
9. Use sufficient contrast and readable text.
10. Clearly identify sample or simulated data.

## Deliverables
- Matplotlib chart collection.
- Seaborn statistical visualizations.
- Interactive Plotly HTML charts.
- Interactive sales dashboard.
- Project documentation and chart guide.

## Conclusion
This project provides hands-on practice in static, statistical, and interactive data visualization with Python. The generated charts demonstrate ways to explore trends, distributions, comparisons, and relationships in data.
