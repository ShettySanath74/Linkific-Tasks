
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Create output directory
output_dir = Path("outputs/plotly")
output_dir.mkdir(parents=True, exist_ok=True)

# Sample dataset
df = pd.DataFrame({
    "Month": [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ],
    "Month_Number": list(range(1, 13)),
    "Sales": [
        12000, 15000, 13500, 18000, 22000, 25000,
        24000, 28000, 26000, 31000, 34000, 38000
    ],
    "Profit": [
        2000, 2800, 2200, 3500, 4600, 5200,
        5000, 6200, 5700, 7200, 8100, 9500
    ],
    "Orders": [
        80, 95, 90, 110, 130, 145,
        140, 160, 155, 180, 195, 220
    ],
    "Advertising": [
        1000, 1200, 1100, 1500, 1800, 2000,
        1900, 2300, 2200, 2600, 2900, 3200
    ],
    "Category": [
        "Electronics", "Clothing", "Furniture"
    ] * 4
})

# 1. Interactive line chart
fig = px.line(
    df, x="Month", y="Sales", markers=True,
    title="1. Monthly Sales Trend"
)
fig.write_html(output_dir / "01_interactive_line.html")

# 2. Interactive bar chart
fig = px.bar(
    df, x="Month", y="Sales", color="Category",
    title="2. Monthly Sales by Category"
)
fig.write_html(output_dir / "02_interactive_bar.html")

# 3. Interactive scatter plot
fig = px.scatter(
    df, x="Advertising", y="Sales",
    color="Category", size="Orders",
    hover_data=["Month", "Profit"],
    title="3. Advertising vs Sales"
)
fig.write_html(output_dir / "03_interactive_scatter.html")

# 4. Interactive histogram
fig = px.histogram(
    df, x="Sales", nbins=6,
    title="4. Sales Distribution"
)
fig.write_html(output_dir / "04_interactive_histogram.html")

# 5. Interactive box plot
fig = px.box(
    df, x="Category", y="Profit",
    color="Category", title="5. Profit Distribution"
)
fig.write_html(output_dir / "05_interactive_box.html")

# 6. Interactive pie chart
category_sales = df.groupby("Category", as_index=False)["Sales"].sum()
fig = px.pie(
    category_sales, names="Category", values="Sales",
    title="6. Sales Share by Category"
)
fig.write_html(output_dir / "06_interactive_pie.html")

# 7. Interactive area chart
fig = px.area(
    df, x="Month", y="Sales",
    title="7. Monthly Sales Area Chart"
)
fig.write_html(output_dir / "07_interactive_area.html")

# 8. Interactive 3D scatter plot
fig = px.scatter_3d(
    df, x="Advertising", y="Sales", z="Profit",
    color="Category", hover_name="Month",
    title="8. 3D Advertising, Sales and Profit"
)
fig.write_html(output_dir / "08_interactive_3d.html")

# 9. Animated chart
fig = px.scatter(
    df, x="Advertising", y="Sales",
    animation_frame="Month_Number",
    color="Category", size="Orders",
    hover_name="Month",
    title="9. Animated Sales Exploration"
)
fig.write_html(output_dir / "09_animated_scatter.html")

# 10. Interactive dashboard with multiple charts
from plotly.subplots import make_subplots

dashboard = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        "Monthly Sales", "Monthly Profit",
        "Orders", "Advertising vs Sales"
    )
)

dashboard.add_trace(
    go.Scatter(
        x=df["Month"], y=df["Sales"],
        mode="lines+markers", name="Sales"
    ),
    row=1, col=1
)

dashboard.add_trace(
    go.Bar(
        x=df["Month"], y=df["Profit"], name="Profit"
    ),
    row=1, col=2
)

dashboard.add_trace(
    go.Scatter(
        x=df["Month"], y=df["Orders"],
        mode="lines+markers", name="Orders"
    ),
    row=2, col=1
)

dashboard.add_trace(
    go.Scatter(
        x=df["Advertising"], y=df["Sales"],
        mode="markers", name="Advertising vs Sales"
    ),
    row=2, col=2
)

dashboard.update_layout(
    title_text="Interactive Sales Dashboard",
    height=750,
    showlegend=True
)
dashboard.write_html(output_dir / "10_sales_dashboard.html")

print("Successfully generated 10 interactive Plotly charts.")
print(f"Output folder: {output_dir.resolve()}")
