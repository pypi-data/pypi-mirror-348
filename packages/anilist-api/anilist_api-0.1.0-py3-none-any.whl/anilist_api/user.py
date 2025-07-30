from .graphql import graphql_request

def get_user(username: str):
    query = """
    query ($name: String) {
      User(name: $name) {
        id
        name
        avatar {
          large
        }
        about(asHtml: false)
        statistics {
          anime {
            count
            meanScore
          }
          manga {
            count
            meanScore
          }
        }
        siteUrl
      }
    }
    """
    variables = {"name": username}
    data = graphql_request(query, variables)
    return data.get("User", None)
