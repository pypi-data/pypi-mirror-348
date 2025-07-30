# AniList-API Python Wrapper

![AniList Logo](https://docs.anilist.co/anilist.png)

[![PyPI Version](https://img.shields.io/pypi/v/anilist-api)](https://pypi.org/project/anilist-api/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)  
[![Build Status](https://img.shields.io/github/actions/workflow/status/anbuinfosec/anilist-api/python-package.yml?branch=main)](https://github.com/anbuinfosec/anilist-api/actions)

---

> A powerful, modular Python client for the AniList GraphQL API that enables you to fetch anime, manga, user profiles, characters, and more with minimal setup.

---

## Features

- Comprehensive search for Anime and Manga with detailed metadata  
- Fetch AniList user profiles and statistics  
- Retrieve character information including descriptions and images  
- Minimal external dependencies (`requests` only)  
- Graceful error handling and clear exceptions  
- Modular design for easy integration and extension

---

## Installation

Install the latest stable release from PyPI:

```bash
pip install anilist-api
````

Or install the latest development version directly from GitHub:

```bash
pip install git+https://github.com/anbuinfosec/anilist-api.git
```

---

## Getting Started

### Importing functions

Import only the features you need:

```python
from anilist_api import search_anime, search_manga, get_user, search_character
```

---

### Basic Usage Examples

#### Search Anime by Title

```python
try:
    anime_results = search_anime("Fullmetal Alchemist", per_page=3)
    for anime in anime_results:
        title = anime['title']['english'] or anime['title']['romaji']
        print(f"{title} | Status: {anime['status']} | Score: {anime.get('averageScore', 'N/A')}")
except Exception as e:
    print(f"Failed to fetch anime: {e}")
```

---

#### Search Manga by Title

```python
try:
    manga_results = search_manga("Death Note", per_page=3)
    for manga in manga_results:
        title = manga['title']['english'] or manga['title']['romaji']
        print(f"{title} | Volumes: {manga.get('volumes', 'N/A')} | Status: {manga['status']}")
except Exception as e:
    print(f"Failed to fetch manga: {e}")
```

---

#### Get User Profile and Stats

```python
try:
    user = get_user("example_username")
    if user:
        print(f"User: {user['name']}")
        print(f"Anime watched: {user['statistics']['anime']['count']}")
        print(f"Manga read: {user['statistics']['manga']['count']}")
    else:
        print("User not found.")
except Exception as e:
    print(f"Failed to fetch user info: {e}")
```

---

#### Search Characters by Name

```python
try:
    characters = search_character("Mikasa Ackerman", per_page=2)
    for character in characters:
        print(f"{character['name']['full']} — {character['description'][:120]}...")
except Exception as e:
    print(f"Failed to fetch characters: {e}")
```

---

## Advanced Usage

### Handling Pagination and Large Data Sets

The `per_page` argument controls the number of results per request (max 50). For larger data sets, you can modify queries to handle pages:

```python
def fetch_all_anime(search_term):
    page = 1
    all_results = []
    while True:
        results = search_anime(search_term, per_page=50, page=page)
        if not results:
            break
        all_results.extend(results)
        page += 1
    return all_results
```

---

### Custom GraphQL Queries

If you want to extend functionality beyond the wrapper, you can directly use the internal `graphql_request` function:

```python
from anilist_api.graphql import graphql_request

query = """
query ($id: Int) {
  Media(id: $id) {
    id
    title {
      romaji
      english
    }
    description(asHtml: false)
  }
}
"""

variables = {"id": 15125}  # Example Media ID for "Naruto"

try:
    data = graphql_request(query, variables)
    media = data.get("Media", {})
    print(media.get("title", {}).get("english"))
    print(media.get("description"))
except Exception as e:
    print(f"GraphQL request failed: {e}")
```

---

## Error Handling

The library raises `AniListAPIError` (a subclass of `Exception`) for any API-related issues such as HTTP errors, malformed requests, or returned API errors.

Example:

```python
from anilist_api.exceptions import AniListAPIError

try:
    results = search_anime("NonExistentAnimeTitle")
except AniListAPIError as api_err:
    print(f"AniList API error: {api_err}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

## Development & Contribution

Feel free to contribute! Fork the repo and submit pull requests with improvements or fixes.

* Follow [PEP8](https://pep8.org/) style guidelines
* Write clear commit messages
* Add tests for new features
* Open issues for bugs or feature requests

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## Useful Links

* AniList API Documentation: [https://docs.anilist.co](https://docs.anilist.co)
* GitHub Repository: [https://github.com/anbuinfosec/anilist-api](https://github.com/anbuinfosec/anilist-api)
* Issue Tracker: [https://github.com/anbuinfosec/anilist-api/issues](https://github.com/anbuinfosec/anilist-api/issues)

---

*Made with ❤️ by Mohammad Alamin*

