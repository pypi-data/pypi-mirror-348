import logging

from stravawizard.clients.oauth_client.stravauth_base_client import (
    StravauthBaseClient,
)
from stravawizard.utils import requires_ready

logger = logging.getLogger(__name__)


class StravauthCredentialsManager(StravauthBaseClient):
    """
    Manages application credentials and configuration settings
    """

    REQUIRED_APP_CREDENTIALS = ["client_id", "client_secret", "redirect_uri"]

    def __init__(self):
        super().__init__()

    @requires_ready
    def get_app_credentials(self):
        """
        Returns the application credentials
        """
        return self._app_credentials

    def set_app_credentials(self, client_id, client_secret, redirect_uri):
        """
        Sets the required application credentials for Strava OAuth.

        Args:
            client_id (str): The Strava client ID.
            client_secret (str): The Strava client secret.
            redirect_uri (str): The redirect URI for OAuth.
        """
        self._app_credentials.update(
            {
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_uri,
            }
        )

    def check_app_credentials(self):
        """
        Checks if all required application credentials are present.

        Returns:
            tuple[bool, list]: True and empty list if all are present, otherwise False and the missing credentials.
        """
        missing_credentials = [
            credential
            for credential in self.REQUIRED_APP_CREDENTIALS
            if not self._app_credentials.get(credential)
        ]
        return not missing_credentials, missing_credentials

    def check_if_ready(self):
        """
        Validates that all required app credentials are set.

        If valid, sets the instance as ready for usage.

        Returns:
            bool: True if the client is ready.

        Raises:
            Exception: If any required app credential is missing.
        """
        credentials_ok, missing_credentials = self.check_app_credentials()
        if not credentials_ok:
            self.is_ready = False  # in case it had been set to True before
            error_msg = f"{', '.join(missing_credentials)} are required credentials and are missing in the credentials dict"
            logger.error(error_msg)
            raise Exception(error_msg)
        self.is_ready = True
        logger.info("StravaCredentialsManager is ready.")
        return True
