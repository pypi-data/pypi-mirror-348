import logging

from stravawizard.clients.api_client.strava_base_api_client import (
    StravaBaseApiClient,
)
from stravawizard.utils import convert_to_timestamp, requires_ready

logger = logging.getLogger(__name__)


class StravaActivityApiClient(StravaBaseApiClient):
    """
    Client for Strava activity-related API endpoints
    """

    def __init__(self, request_handler=None):
        super().__init__()
        self.request_handler = request_handler

    def set_request_handler(self, request_handler):
        """
        Sets the request handler for API calls

        Args:
            request_handler (StravaRequestHandler): Handler for API requests
        """
        self.request_handler = request_handler

    @requires_ready
    def get_athlete_activities(
        self, page="1", per_page="10", start_date=None, end_date=None
    ):
        """
        Gets activities for the authenticated athlete

        Args:
            page (str): Page number for pagination
            per_page (str): Number of items per page
            start_date: Start date for filtering activities
            end_date: End date for filtering activities

        Returns:
            dict: List of activities or error message
        """
        activities_endpoint = f"{self.API_BASE_URL}/athlete/activities"
        params = {"page": page, "per_page": per_page}

        if start_date:
            params["after"] = convert_to_timestamp(start_date)
        if end_date:
            params["before"] = convert_to_timestamp(end_date)

        return self.request_handler.get(activities_endpoint, params)

    @requires_ready
    def get_activity_photos(self, activity_id, size=600):
        """
        Gets all photos for a specific activity

        Args:
            activity_id (int): Strava activity ID
            size (int): Desired photo size (100|600|1200|2000)

        Returns:
            list: List of dictionaries containing photo URLs or None on error
        """
        photos_endpoint = f"{self.API_BASE_URL}/activities/{activity_id}/photos"
        params = {"size": size}

        return self.request_handler.get(photos_endpoint, params)

    def check_if_ready(self):
        """
        Checks if the client is ready for API calls

        Returns:
            bool: True if ready, False otherwise
        """
        if not self.request_handler or not self.request_handler.access_token:
            logger.warning("Request handler not set or access token missing")
            self.is_ready = False
            return False
        self.is_ready = True
        logger.info("StravaActivityApiClient is ready.")
        return True
