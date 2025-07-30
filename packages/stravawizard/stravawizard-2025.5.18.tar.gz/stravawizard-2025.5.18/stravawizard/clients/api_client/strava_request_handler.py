import logging

import requests

logger = logging.getLogger(__name__)


class StravaRequestHandler:
    """
    Handles HTTP requests to the Strava API
    """

    def __init__(self, access_token=None):
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {access_token}" if access_token else ""
        }

    def set_access_token(self, access_token):
        """
        Sets the access token for API requests

        Args:
            access_token (str): The Strava OAuth access token
        """
        self.access_token = access_token
        self.headers = {"Authorization": f"Bearer {access_token}"}

    def get(self, url, params=None):
        """
        Makes a GET request to the specified URL

        Args:
            url (str): The endpoint URL
            params (dict, optional): Query parameters

        Returns:
            dict: JSON response or error message

        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            logger.error(f"HTTP error: {err}")
            return {"error": f"HTTP error: {err}"}
        except requests.exceptions.RequestException as err:
            logger.error(f"Request failed: {err}")
            return {"error": f"Request failed: {err}"}
