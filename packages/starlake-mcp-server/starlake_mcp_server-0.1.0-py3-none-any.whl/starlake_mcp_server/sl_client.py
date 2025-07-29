import requests

from starlake_mcp_server.logging_setup import setup_logging
from starlake_mcp_server.settings import DEBUG


logger = setup_logging(debug=DEBUG)


class APIClient:
    session_cookie = None  # Initialize session_cookie as an instance variable

    def __init__(self, base_url, api_key):
        """
        Initialize the API client.

        :param base_url: The base URL of the API.
        :param api_key: The API key for authentication.
        """
        self.base_url = base_url
        self.api_key = api_key

    def request(self, method, endpoint, headers, data, json, session_cookie=None):
        """
        Post to the API and retrieve the '_sessiondata' cookie.

        :param endpoint: The API endpoint to post to.
        :param payload: The JSON payload to send in the request body.
        :param session_cookie: Optional '_sessiondata' cookie to include in the request.
        :return: The value of the '_sessiondata' cookie, or None if not found.
        """
        url = f"{self.base_url}/{endpoint}"
        # Include the '_sessiondata' cookie if provided
        cookies = {}
        if session_cookie:
            cookies['_sessiondata'] = session_cookie

        response = requests.request(method, url, data=data, json=json, headers=headers, cookies=cookies)

        # Raise an exception for HTTP errors
        response.raise_for_status()

        # Retrieve the '_sessiondata' cookie
        new_session_cookie = response.cookies.get('_sessiondata')
        if new_session_cookie:
            logger.debug(f"Session cookie retrieved: {new_session_cookie}")
            self.session_cookie = new_session_cookie
        return response

    def select_project(self, project_id):
        """
        Select a project using the provided project ID.

        :param project_id: The ID of the project to select.
        :param session_cookie: The '_sessiondata' cookie for authentication.
        :return: The response from the project selection API.
        """
        endpoint = f"api/v1/projects/{project_id}"
        headers = {
            "Content-Type": "application/json"
        }
        cookies = {
            "_sessiondata": self.session_cookie
        }

        response = self.request('GET', endpoint, headers=headers, data=None, json=None, session_cookie=self.session_cookie)

        return response.json()

    def auth(self):
        """
        Authenticate using the API key and optional existing cookie.
        """
        endpoint = "api/v1/auth/basic/api-key-signin"
        headers = {
            "Content-Type": "application/json",
            "apiKey": self.api_key
        }
        self.request('POST', endpoint, headers, data=None, json=None, session_cookie=self.session_cookie)


# Example usage
if __name__ == "__main__":
    base_url = "http://localhost:9000"
    api_key = "25a3c0a890e008d2532c9aabbf88772b45a895dd096488ec4b4deae858b410b1"
    existing_cookie = None  # Replace with an existing '_sessiondata' cookie if available

    # Authenticate and retrieve session cookie
    client = APIClient(base_url, api_key)
    client.auth()
    # Select a project
    project_id = 101
    project_response = client.select_project(project_id)
    print(f"Project selected: {project_response}")

