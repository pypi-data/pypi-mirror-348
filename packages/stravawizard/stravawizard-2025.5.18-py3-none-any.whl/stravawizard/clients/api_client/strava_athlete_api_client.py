import logging

from stravawizard.clients.api_client.strava_base_api_client import (
    StravaBaseApiClient,
)
from stravawizard.utils import requires_ready

logger = logging.getLogger(__name__)


class StravaAthleteApiClient(StravaBaseApiClient):
    """
    Client for Strava athlete-related API endpoints
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
    def get_athlete_stats(self, athlete_id):
        """
        Gets statistics for a specific athlete

        Args:
            athlete_id (int): ID of the athlete

        Returns:
            dict: Athlete statistics
        """
        athlete_stats_endpoint = f"{self.API_BASE_URL}/athletes/{athlete_id}/stats"
        return self.request_handler.get(athlete_stats_endpoint)

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
        logger.info("StravaAthleteApiClient is ready.")
        return True
