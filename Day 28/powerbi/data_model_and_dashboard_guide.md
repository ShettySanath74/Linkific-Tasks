# Power BI Data Model and Dashboard Guide

## Import data
In Power BI Desktop: Home → Get data → Text/CSV. Import `customers.csv`, `products.csv`, `orders.csv`, and `order_items.csv` from the `data` folder. Confirm date and numeric data types.

## Relationships (Model view)
- Customers[customer_id] (1) → Orders[customer_id] (*)
- Orders[order_id] (1) → Order_Items[order_id] (*)
- Products[product_id] (1) → Order_Items[product_id] (*)
Use single-direction filtering from dimension to fact tables. Avoid many-to-many relationships.

## Measures
Create the measures in `dax_measures.dax`. Set `Profit Margin %` to Percentage format. Format revenue, cost, profit, and AOV as currency or decimal with a clear note that the dataset uses generic currency units (CU).

## Recommended report pages
### Page 1 – Executive Overview
- KPI cards: Total Revenue, Estimated Profit, Profit Margin %, Completed Orders, Unique Customers, Average Order Value
- Line chart: order date by month vs Total Revenue
- Bar chart: Category vs Total Revenue
- Bar/column chart: Region vs Total Revenue

### Page 2 – Product Performance
- Bar chart: Product name vs Total Revenue (Top N = 10)
- Matrix: Category, Product, Units Sold, Total Revenue, Estimated Profit
- Slicers: Category, Product

### Page 3 – Customer & Regional Analysis
- Bar chart: Region vs Total Revenue
- Table: Customer name, region, completed orders, revenue (create additional customer-level measures if desired)
- Slicers: Region, City

### Page 4 – Order & Discount Analysis
- Donut chart: Orders by order_status (use count of order_id)
- Column chart: discount_pct vs revenue
- Cards: Returned Orders, Cancelled Orders

## Interactions and navigation
- Add slicers for Order Date, Region, Category, and Order Status.
- Use Format → Edit interactions to confirm slicers filter relevant visuals.
- Enable drill-through on Product name to a Product Detail page.
- Add bookmarks for key views only after arranging visuals.
- Insert page-navigation buttons via Insert → Buttons → Navigator → Page navigator.

## Validation
Compare Power BI Total Revenue and Completed Orders cards with the SQL executive KPI query. Confirm cancelled and returned orders are excluded from revenue/profit measures. Save as `powerbi/analytics_dashboard.pbix`.

## Note
A `.pbix` is a native Power BI Desktop file. This package supplies the prepared source data, model design, DAX, and report specification; create and save the PBIX in Power BI Desktop.
