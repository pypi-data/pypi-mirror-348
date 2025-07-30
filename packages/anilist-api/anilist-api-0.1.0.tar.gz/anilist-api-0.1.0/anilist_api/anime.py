from .graphql import graphql_request

def search_anime(search: str, per_page: int = 5):
    query = """
    query ($search: String, $perPage: Int) {
      Page(perPage: $perPage) {
        media(search: $search, type: ANIME) {
          id
          title {
            romaji
            english
            native
          }
          episodes
          status
          averageScore
          genres
          description(asHtml: false)
          startDate {
            year
            month
            day
          }
          endDate {
            year
            month
            day
          }
          siteUrl
        }
      }
    }
    """
    variables = {
        "search": search,
        "perPage": per_page
    }
    data = graphql_request(query, variables)
    return data.get("Page", {}).get("media", [])
