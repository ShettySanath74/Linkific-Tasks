# Day 2 — Python API Data Collection

## Objective

Practise REST APIs, HTTP methods, response parsing, authentication concepts, pagination, error handling, retries, and storing collected data in JSON and CSV formats.

## Technologies

- Python
- Requests
- pandas
- python-dotenv
- REST APIs
- JSON and CSV

## Project Structure

```text
day2_api_collection/
├── data/
├── outputs/
│   ├── posts.json
│   ├── countries.csv
│   ├── countries.json
│   ├── github_repository.json
│   └── github_commits.json
├── scripts/
│   ├── api_utils.py
│   ├── collect_countries.py
│   ├── collect_github.py
│   ├── collect_jsonplaceholder.py
│   ├── http_methods_demo.py
│   └── pagination_demo.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

Run these commands from the project folder:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Running the Scripts

Run these commands from the `scripts` folder:

```powershell
python collect_jsonplaceholder.py
python collect_countries.py
python collect_github.py
python pagination_demo.py
python http_methods_demo.py
```

## API Integrations

### 1. JSONPlaceholder

- Endpoint: `https://jsonplaceholder.typicode.com/posts`
- Retrieves sample posts.
- Saves selected fields to `outputs/posts.json`.

### 2. REST Countries

- Uses the REST Countries API v5 endpoint.
- Extracts country name, country code, capital, region, and population.
- Saves the results to `outputs/countries.csv` and `outputs/countries.json`.
- The current verified run returned one country record; the result may depend on API access and response data.

### 3. GitHub REST API

- Endpoint: `https://api.github.com/repos/python/cpython`
- Collects repository metadata such as name, description, stars, forks, language, and URL.
- Saves the result to `outputs/github_repository.json`.
- Authentication is optional for the public-repository example.

### 4. GitHub Pagination

- Endpoint: `https://api.github.com/repos/python/cpython/commits`
- Requests up to three pages, with ten commits per page.
- Extracts commit SHA, author, date, message, and URL.
- Saves results to `outputs/github_commits.json`.
- The verified run collected 30 commits.

## HTTP Methods

The HTTP methods demonstration uses JSONPlaceholder to practise:

- GET — retrieve a resource.
- POST — simulate creating a resource.
- PUT — simulate replacing a resource.
- DELETE — simulate deleting a resource.

JSONPlaceholder is a testing service; write and delete requests do not permanently change its stored data.

## Error Handling and Retries

The project demonstrates request timeouts, HTTP status checks, network error handling, JSON parsing, and retry/backoff logic.

The `api_utils.py` helper provides a reusable `get_json()` function. The pagination example separately implements retries for temporary errors.

## Authentication and Security

- The GitHub repository example works without a personal access token.
- An optional `GITHUB_TOKEN` environment variable can be loaded from a local `.env` file.
- Never commit real API tokens, passwords, or private credentials.
- Keep `.env` excluded through `.gitignore`.

## Verified Results

- JSONPlaceholder: 20 posts collected.
- REST Countries: one country record collected in the verified run.
- GitHub repository metadata: successfully retrieved.
- GitHub pagination: 30 commits collected over three pages.
- HTTP methods: GET 200, POST 201, PUT 200, DELETE 200.
- Reusable API helper: successfully retrieved three posts in a test.

## Learning Outcomes

This project practises API requests, query parameters, headers, HTTP methods, JSON parsing, pagination, retry logic, environment variables, and CSV/JSON data storage.