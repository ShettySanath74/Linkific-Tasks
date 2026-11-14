# Task Breakdown, Roles, and Timeline

## Suggested roles (individual project can combine all roles)
| Role | Responsibility |
|---|---|
| Data Engineer | Source ingestion, ETL, orchestration |
| Data Warehouse Developer | PostgreSQL schema, dimensional modelling |
| Data Quality Analyst | Validation rules and reconciliation |
| BI Developer | Power BI model, measures, dashboards |
| Project Coordinator | Scope, documentation, milestones |

## Milestones
| Milestone | Tasks | Completion evidence |
|---|---|---|
| M1 — Planning | Domain, requirements, personas, scope | Proposal |
| M2 — Architecture | Components, technology choices, architecture diagram | Architecture document |
| M3 — Data modelling | Grain, dimensions, facts, dictionary | ERD and dictionary |
| M4 — Pipeline design | Extract, transform, quality, load, error handling | ETL flow |
| M5 — Infrastructure | Python, PostgreSQL, Airflow, Git | Setup verification |
| M6 — Ingestion | Connect APIs/files and preserve raw data | Source files and scripts |
| M7 — Warehouse | Create and populate dimensional tables | SQL and loaded tables |
| M8 — Orchestration | Build and schedule DAG | Successful DAG run |
| M9 — BI | Build and validate dashboard | Dashboard report |

## Suggested implementation sequence
1. Finalize sample source schemas and create synthetic data.
2. Set up PostgreSQL and create warehouse tables.
3. Implement ingestion and staging.
4. Implement transformations and data quality checks.
5. Load dimensions and fact tables.
6. Orchestrate with Airflow.
7. Build Power BI dashboard and reconcile metrics.
8. Document tests, limitations, and results.

## Day 22 completion checklist
- [x] Select project domain
- [x] Define functional and non-functional requirements
- [x] Identify sources, volume, frequency, analytics, and users
- [x] Design architecture
- [x] Design star schema and data dictionary
- [x] Document ETL flow
- [x] Prepare dashboard mockup
- [x] Define roles, milestones, and task sequence
- [x] Prepare repository README and starter structure
- [x] Prepare starter SQL, quality-check module, and Airflow DAG template
- [ ] Install and verify PostgreSQL locally
- [ ] Install and verify Airflow in WSL2/Docker
- [ ] Implement and run the complete end-to-end pipeline
