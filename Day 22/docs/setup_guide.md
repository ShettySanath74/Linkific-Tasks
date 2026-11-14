# Local Setup Guide

## 1. Python environment
From the project root in PowerShell:
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, use:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 2. PostgreSQL
Install PostgreSQL locally or use an approved Docker setup. Create a database named `ecommerce_warehouse`. Run:
```powershell
psql -U postgres -d ecommerce_warehouse -f warehouse\sql\001_create_warehouse.sql
```
If `psql` is not on PATH, use the SQL editor in pgAdmin to execute the SQL file.

## 3. Environment variables
Copy `.env.example` to `.env` and enter local connection details. Do not commit `.env`.

## 4. Airflow
Airflow is designed for Linux-based environments. For Windows development, use WSL2 or Docker and follow the official Apache Airflow installation instructions for the selected environment. The included DAG is a template and needs its Python modules and database connection configured before execution.

## 5. Git
```powershell
git init
git add .
git commit -m "Add e-commerce analytics platform project foundation"
```
Connect the repository to the intended GitHub remote only after confirming the correct remote URL.
