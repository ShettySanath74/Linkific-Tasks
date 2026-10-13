
import requests

BASE_URL = "https://jsonplaceholder.typicode.com/posts"
HEADERS = {"Content-Type": "application/json"}
TIMEOUT = 15


def show_response(method, response):
    print(f"\n{method} status: {response.status_code}")
    print("Response:", response.text[:500])


def main():
    try:
        # GET: retrieve an existing post.
        response = requests.get(f"{BASE_URL}/1", timeout=TIMEOUT)
        response.raise_for_status()
        show_response("GET", response)

        # POST: simulate creating a post.
        new_post = {
            "title": "API learning",
            "body": "Practising HTTP methods with Python",
            "userId": 1,
        }
        response = requests.post(
            BASE_URL,
            json=new_post,
            headers=HEADERS,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        show_response("POST", response)

        # PUT: simulate replacing an existing post.
        updated_post = {
            "id": 1,
            "title": "Updated title",
            "body": "Practising PUT requests",
            "userId": 1,
        }
        response = requests.put(
            f"{BASE_URL}/1",
            json=updated_post,
            headers=HEADERS,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        show_response("PUT", response)

        # DELETE: simulate deleting an existing post.
        response = requests.delete(f"{BASE_URL}/1", timeout=TIMEOUT)
        response.raise_for_status()
        show_response("DELETE", response)

    except requests.Timeout:
        print("Request timed out. Please try again.")

    except requests.HTTPError as error:
        print("HTTP error:", error)

    except requests.RequestException as error:
        print("Network or request error:", error)


if __name__ == "__main__":
    main()
