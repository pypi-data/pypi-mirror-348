import requests
import time

API_URL = "http://localhost:8500"

def search_web(query: str, engine: str = "google", num_results: int = 5):
    payload = {
        "query": query,
        "engine": engine,
        "num_results": num_results
    }

    try:
        # Step 1: Submit the search request
        response = requests.post(f"{API_URL}/search", json=payload)
        response.raise_for_status()
        data = response.json()
        task_id = data.get("task_id")
        if not task_id:
            print("No task ID returned from the server.")
            return

        print(f"Search started. Task ID: {task_id}")
        print("Waiting for result...")

        # Step 2: Poll for result
        for _ in range(30):  # try for up to ~30 seconds
            time.sleep(2)
            poll_response = requests.get(f"{API_URL}/search/{task_id}")
            if poll_response.status_code == 404:
                print("Result not ready or expired.")
                continue

            result_data = poll_response.json()
            status = result_data.get("status")

            if status == "completed":
                print("\nSearch Results:\n")
                results = result_data.get("results", [])
                for idx, result in enumerate(results, start=1):
                    print(f"{idx}. {result}")
                return

            elif status == "failed":
                print(f"Search failed: {result_data.get('error')}")
                return

            else:
                print(".", end="", flush=True)

        print("\nTimed out waiting for search results.")

    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
    except ValueError:
        print("Invalid response received from the server.")


if __name__ == "__main__":
    search_web("latest AI research in 2025")
