# Day 28 – Business Intelligence & Analytics
## Sales Performance Analytics Dashboard

### Objective
Analyze retail sales performance, customer purchasing behavior, product/category contribution, regional performance, and monthly trends.

### Dataset
This project uses a **synthetic retail dataset** generated for practice. It is not real company/customer data. Currency is represented as generic currency units (CU), not INR or any other real currency.

### Tools
- SQL (SQLite-compatible analytical queries)
- Python (pandas, matplotlib, seaborn; optional Jupyter)
- Power BI Desktop (manual dashboard assembly)

### Folder structure
- `data/` – customers, products, orders, and order_items CSV files
- `sql/analytical_queries.sql` – reusable business queries
- `python/exploratory_analysis.ipynb` – analysis notebook
- `powerbi/` – model guide, DAX measures, and report build instructions
- `docs/business_insights.md` – interpretation guide and findings template
- `outputs/` – generated chart and result folders

### Data model
`customers (1) -> orders (many) -> order_items (many) <- products (1)`

Join keys:
- customers.customer_id = orders.customer_id
- orders.order_id = order_items.order_id
- products.product_id = order_items.product_id

### Quick start
1. Install Python 3.10+ and run `pip install -r requirements.txt`.
2. Open `python/exploratory_analysis.ipynb` in Jupyter and run all cells.
3. Run SQL statements in `sql/analytical_queries.sql` using SQLite. The notebook also creates `data/sales_analytics.db`.
4. In Power BI Desktop, import the four CSV files, create the relationships described in `powerbi/data_model_and_dashboard_guide.md`, add measures from `powerbi/dax_measures.dax`, and build the report pages.

### Important metric definition
Revenue and profit calculations include only `Completed` orders. Returned and Cancelled orders are excluded. Revenue is calculated from `order_items.line_revenue`; estimated profit is line revenue minus quantity multiplied by product unit cost. This is a simplified training model and does not include shipping, tax, overhead, or refunds.

### Deliverables checklist
- [x] Synthetic source dataset
- [x] Analytical SQL query pack
- [x] Python exploratory analysis notebook
- [x] Power BI model and DAX measure definitions
- [x] Dashboard construction guide
- [x] Business insights documentation template
- [ ] Build and save the `.pbix` file in Power BI Desktop
- [ ] Review actual notebook outputs and complete evidence-based insights
