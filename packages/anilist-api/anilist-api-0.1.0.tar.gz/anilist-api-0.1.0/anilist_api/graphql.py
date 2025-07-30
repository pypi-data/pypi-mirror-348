import requests
from .config import API_URL, HEADERS
from .exceptions import AniListAPIError

def graphql_request(query: str, variables: dict = None) -> dict:
    payload = {
        "query": query,
        "variables": variables or {}
    }
    response = requests.post(API_URL, json=payload, headers=HEADERS)
    if response.status_code != 200:
        raise AniListAPIError(f"HTTP error {response.status_code}: {response.text}")
    data = response.json()
    if "errors" in data:
        error_message = data["errors"][0].get("message", "Unknown error")
        raise AniListAPIError(f"API error: {error_message}")
    return data.get("data", {})
