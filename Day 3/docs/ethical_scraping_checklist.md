# Ethical Web Scraping Checklist

## Before Scraping

- [ ] Check the website's Terms of Service.
- [ ] Review `robots.txt` and applicable crawling guidance.
- [ ] Check whether an official API is available.
- [ ] Confirm that the data is appropriate to collect and use.
- [ ] Avoid collecting unnecessary personal or sensitive information.

## During Scraping

- [ ] Use a descriptive User-Agent where appropriate.
- [ ] Set request timeouts.
- [ ] Limit the number of pages requested.
- [ ] Add reasonable delays between requests.
- [ ] Follow pagination links carefully.
- [ ] Respect documented rate limits and access restrictions.
- [ ] Stop or slow down when receiving HTTP 429 responses.
- [ ] Do not bypass login systems, paywalls, CAPTCHAs, or other access controls.

## Data Handling

- [ ] Validate extracted records.
- [ ] Remove duplicate records where appropriate.
- [ ] Store data in structured CSV or JSON formats.
- [ ] Avoid collecting or publishing confidential information.
- [ ] Keep credentials and API keys out of source code and GitHub.
- [ ] Document data sources and collection limitations.

## Before Publishing or Reusing Data

- [ ] Review applicable site terms and legal requirements.
- [ ] Respect privacy and copyright obligations.
- [ ] Confirm that the intended use is permitted.
- [ ] Avoid presenting scraped data as verified when it has not been verified.

## Practice Sources

- Books to Scrape: https://books.toscrape.com/
- Quotes to Scrape: https://quotes.toscrape.com/
- WebScraper.io demo: https://webscraper.io/test-sites/e-commerce/static

**Purpose:** This checklist supports responsible educational web scraping. It is not legal advice.