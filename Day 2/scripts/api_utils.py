
import time
import requests


def get_json(url, params=None, headers=None, timeout=15, max_retries=3):
    """Fetch JSON from an API with basic retry and error handling."""

    for attempt in range(max_retries):
        try:
            response = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=timeout,
            )

            # Retry rate-limit and temporary server errors.
            if response.status_code == 429 or response.status_code >= 500:
                if attempt < max_retries - 1:
                    retry_after = response.headers.get("Retry-After")

                    try:
                        delay = float(retry_after) if retry_after else 2 ** attempt
                    except ValueError:
                        delay = 2 ** attempt

                    delay = min(delay, 30)
                    print(
                        f"Temporary HTTP {response.status_code}. "
                        f"Retrying in {delay} seconds..."
                    )
                    time.sleep(delay)
                    continue

            response.raise_for_status()

            # This raises ValueError if the response isn't valid JSON.
            return response.json()

        except (requests.Timeout, requests.ConnectionError) as error:
            if attempt == max_retries - 1:
                raise

            delay = 2 ** attempt
            print(f"Network error: {error}. Retrying in {delay} seconds...")
            time.sleep(delay)

    raise RuntimeError("API request failed after all retry attempts.")
