# E-commerce Analytics Platform — Day 22

## Project overview
This project designs a data platform for collecting e-commerce product, customer, order, and inventory data; validating and transforming it; loading it into a PostgreSQL analytical warehouse; orchestrating workflows with Apache Airflow; and presenting insights through Power BI.

**Day 22 scope:** project proposal, requirements, architecture, dimensional data model, data dictionary, ETL flow, dashboard mockup, task breakdown, repository structure, and starter infrastructure/code.

> This is a project foundation and starter implementation. PostgreSQL/Airflow are not installed or running merely by extracting this ZIP. Follow `docs/setup_guide.md` when ready to configure them.

## Technology stack
- Python and Pandas: ingestion and transformation
- PostgreSQL: analytical warehouse
- Apache Airflow: workflow orchestration
- Power BI: reporting and visualization
- Git/GitHub: version control

## Repository structure
```text
Day 22/
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
├── config/
├── data/raw/
├── data/processed/
├── docs/
├── ingestion/
├── transformations/
├── warehouse/
│   └── sql/
├── airflow/dags/
├── tests/
└── dashboards/
```

## Key analytical questions
1. What are total sales and revenue by day, month, and product category?
2. Which products generate the highest revenue and order volume?
3. What is the average order value?
4. Which products are running low on inventory?
5. How do sales vary by location and customer segment?

## Getting started
1. Read `docs/project_proposal.md`.
2. Review the architecture and data model in `docs/`.
3. Copy `.env.example` to `.env` and configure local credentials (never commit `.env`).
4. Follow `docs/setup_guide.md`.
5. Review `warehouse/sql/001_create_warehouse.sql`.
6. The Airflow starter DAG is in `airflow/dags/ecommerce_etl_dag.py`.

## Day 22 deliverables
- Project proposal and requirements
- Architecture diagram
- Star-schema data model and data dictionary
- ETL flow diagram
- Dashboard wireframe / requirements
- Roles, milestones, and timeline
- Starter SQL, validation code, and Airflow DAG template
- Setup guide and Git-ready structure

## Current implementation status
| Component | Status |
|---|---|
| Project planning and documentation | Prepared |
| Architecture and data model design | Prepared |
| PostgreSQL schema script | Starter SQL prepared |
| Data quality checks | Starter Python module prepared |
| Airflow DAG | Template prepared; requires Airflow environment |
| Power BI dashboard | Mockup/specification only; not built |
| Live ingestion and end-to-end ETL | Future implementation |

## Data handling
Use public/sample or synthetic data for development. Do not place credentials, personal customer information, or production data in this repository.
