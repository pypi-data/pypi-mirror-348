import logging

from stravawizard.clients.api_client.strava_activity_api_client import (
    StravaActivityApiClient,
)
from stravawizard.clients.api_client.strava_athlete_api_client import (
    StravaAthleteApiClient,
)
from stravawizard.clients.api_client.strava_request_handler import (
    StravaRequestHandler,
)
from stravawizard.utils import requires_ready

logger = logging.getLogger(__name__)


class StravaApiClient:
    """
    Main client for Strava API that integrates all specialized clients
    """

    def __init__(self, strava_access_token=None):
        """
        Initializes the Strava API client with all required components

        Args:
            strava_access_token (str, optional): Strava OAuth access token
        """
        # Create request handler and specialized clients
        self.request_handler = StravaRequestHandler(strava_access_token)

        # Public API clients as namespaces
        self.athlete = StravaAthleteApiClient(self.request_handler)
        self.activity = StravaActivityApiClient(self.request_handler)

        # State
        self.is_ready = False

    def set_strava_access_token(self, strava_access_token):
        """
        Sets the access token for all API clients

        Args:
            strava_access_token (str): Strava OAuth access token
        """
        self.request_handler.set_access_token(strava_access_token)

    def check_if_ready(self):
        """
        Checks if all components are ready for API calls

        Returns:
            bool: True if ready, False otherwise
        """
        if not self.request_handler.access_token:
            logger.warning("strava_access_token has not been defined in strava_api_cli")
            self.is_ready = False
            return False

        # Check if all components are ready
        try:
            self.athlete.check_if_ready()
            self.activity.check_if_ready()
            self.is_ready = True
            logger.info("StravaApiClient is ready.")
            return True
        except Exception as e:
            self.is_ready = False
            logger.error(f"StravaApiClient is not ready: {str(e)}")
            return False
