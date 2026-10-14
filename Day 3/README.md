# Linkific Internship — Day 3: Web Scraping with Python

## Overview

This project demonstrates web scraping fundamentals using Python, Requests, BeautifulSoup, and Selenium. It includes pagination, structured data extraction, data cleaning, and CSV/JSON storage.

## Learning Objectives

- Understand HTML structure, CSS selectors, and basic XPath concepts.
- Fetch and parse HTML pages with Requests and BeautifulSoup.
- Extract text and attributes from HTML elements.
- Follow pagination and relative links.
- Use Selenium to inspect JavaScript-rendered content.
- Clean, validate, and deduplicate extracted records.
- Store structured data in CSV and JSON formats.
- Apply ethical web scraping practices.

## Technologies

- Python
- Requests
- BeautifulSoup 4
- Selenium
- pandas

## Project Structure

```text
Day 3/
├── scripts/
├── outputs/
├── docs/
│   └── ethical_scraping_checklist.md
├── README.md
├── requirements.txt
└── .gitignore
```

## Practice Sources

1. Books to Scrape — https://books.toscrape.com/
2. Quotes to Scrape — https://quotes.toscrape.com/
3. WebScraper.io e-commerce demo — https://webscraper.io/test-sites/e-commerce/static

## Scripts

| Script | Purpose |
|---|---|
| `02_beautifulsoup_basics.py` | Basic HTML parsing and CSS selectors |
| `03_scrape_books.py` | Extract books from one page |
| `04_scrape_books_pagination.py` | Extract books across multiple pages |
| `05_scrape_quotes_pages.py` | Extract quotes across multiple pages |
| `06_selenium_dynamic.py` | Extract JavaScript-rendered quotes |
| `07_clean_data.py` | Clean records and remove duplicates |
| `08_scrape_third_source.py` | Extract product information |
| `09_combine_datasets.py` | Standardize and combine datasets |

## Setup

Install dependencies from the `Day 3` directory:

```powershell
python -m pip install -r requirements.txt
```

Run an individual script:

```powershell
python .\scripts\02_beautifulsoup_basics.py
python .\scripts\03_scrape_books.py
python .\scripts\04_scrape_books_pagination.py
python .\scripts\05_scrape_quotes_pages.py
python .\scripts\06_selenium_dynamic.py
python .\scripts\07_clean_data.py
python .\scripts\08_scrape_third_source.py
python .\scripts\09_combine_datasets.py
```

The Selenium script requires a supported browser environment, such as Google Chrome. Selenium may manage the browser driver automatically in supported environments.

## Outputs

Depending on which scripts have run successfully, the `outputs/` directory may contain:

- Book datasets in CSV and JSON.
- Paginated book datasets in CSV and JSON.
- Quote datasets in CSV and JSON.
- Dynamic quote data collected using Selenium.
- Product datasets in CSV and JSON.
- Cleaned datasets.
- A combined dataset from available sources.

## Data Quality

The cleaning script trims surrounding whitespace, skips records missing required fields, and removes duplicates based on selected fields. The combined dataset standardizes source records into common columns.

## Ethical Considerations

This project uses practice websites for learning. Requests are limited where configured, and delays are included in pagination scripts. Always review applicable site terms, crawling guidance, privacy obligations, and legal requirements before scraping any website.

## Limitations

- Scraped content and record counts can change.
- Network errors or website changes can affect extraction.
- Selenium requires a supported browser environment.
- The combined dataset contains only sources whose input files are available.
- The project is educational and is not intended to bypass access restrictions.

## Author

Prepared as part of the Linkific Data Engineering Internship — Day 3.