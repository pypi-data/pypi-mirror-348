import logging

from stravawizard.clients.oauth_client.stravauth_credentials_manager import (
    StravauthCredentialsManager,
)
from stravawizard.clients.oauth_client.stravauth_token_manager import (
    StravauthTokenManager,
)

logger = logging.getLogger(__name__)


class StravauthClient:
    """
    A client class responsible for managing Strava OAuth authentication.

    Integrates credential management, token handling, and athlete data access.
    """

    def __init__(self):
        """
        Initializes the StravAuthClient with all required managers.
        """
        self.credentials_manager = StravauthCredentialsManager()
        self.token_manager = StravauthTokenManager()
        self.athlete_summary = None

        # Setup dependencies
        self.token_manager.set_credentials_manager(self.credentials_manager)

        self.is_ready = False

    def get_authorization_url(self):
        """
        Generates authorization URL to redirect user requesting access
        """
        app_credentials = self.credentials_manager.get_app_credentials()
        scope = self.credentials_manager.scope
        base_endpoint = self.credentials_manager.STRAVA_OAUTH_BASE_ENDPOINT

        return (
            f"{base_endpoint}authorize?"
            f"client_id={app_credentials['client_id']}&"
            f"redirect_uri={app_credentials['redirect_uri']}&"
            f"response_type=code&scope={scope}"
        )

    def exchange_authorization_code(self, authorization_code):
        """
        Exchanges an authorization code for access and refresh tokens.
        Updates athlete summary from the response data.
        """
        response = self.token_manager.exchange_authorization_code(authorization_code)
        if response and "athlete" in response:
            self.athlete_summary = response["athlete"]
        return response

    def get_athlete_summary(self):
        """
        Returns the athlete profile summary.
        """
        return self.athlete_summary

    def check_if_ready(self):
        """
        Validates that all components are ready for usage.
        """
        try:
            self.credentials_manager.check_if_ready()
            self.token_manager.check_if_ready()
            self.is_ready = True
            logger.info("StravauthClient is ready.")
            return True
        except Exception as e:
            self.is_ready = False
            logger.error(f"StravAuthClient is not ready: {str(e)}")
            raise
