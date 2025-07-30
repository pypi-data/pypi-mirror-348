from .graphql import graphql_request

def search_character(search: str, per_page: int = 5):
    query = """
    query ($search: String, $perPage: Int) {
      Page(perPage: $perPage) {
        characters(search: $search) {
          id
          name {
            first
            last
            full
            native
          }
          image {
            large
          }
          description(asHtml: false)
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
    return data.get("Page", {}).get("characters", [])
