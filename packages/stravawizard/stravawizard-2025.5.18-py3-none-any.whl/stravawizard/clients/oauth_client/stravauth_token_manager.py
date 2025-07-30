import json
import logging
import time
from datetime import datetime

import requests

from stravawizard.clients.oauth_client.stravauth_base_client import (
    StravauthBaseClient,
)
from stravawizard.utils import requires_ready

logger = logging.getLogger(__name__)


class StravauthTokenManager(StravauthBaseClient):
    """
    Manages OAuth tokens, including refreshing and validating access tokens
    """

    def __init__(self, credentials_manager=None):
        super().__init__()
        self.credentials_manager = credentials_manager
        self.user_oauth_credentials = {
            "access_token": None,
            "refresh_token": None,
            "expires_at": None,
        }

    def set_credentials_manager(self, credentials_manager):
        """
        Sets the credentials manager to use for token operations

        Args:
            credentials_manager (StravaCredentialsManager): The credentials manager instance
        """
        self.credentials_manager = credentials_manager

    @requires_ready
    def get_user_oauth_credentials(self):
        """
        Returns the current user OAuth credentials

        Returns:
            dict: User OAuth credentials
        """
        return self.user_oauth_credentials

    @requires_ready
    def set_user_oauth_credentials_from_user(self, user):
        """
        Sets user OAuth credentials from a user object.

        The user object must have:
            - strava_access_token
            - strava_refresh_token
            - strava_expires_at

        Args:
            user: Object with required Strava token attributes.
        """
        self.user_oauth_credentials.update(
            {
                "access_token": user.strava_access_token,
                "refresh_token": user.strava_refresh_token,
                "expires_at": user.strava_expires_at,
            }
        )

    @requires_ready
    def is_access_token_valid(self):
        """
        Checks whether the access token is still valid based on its expiration time.

        Returns:
            bool: True if the token is valid, False otherwise.
        """
        expires_at = self.user_oauth_credentials["expires_at"]
        if isinstance(expires_at, datetime):
            expires_at = expires_at.timestamp()
        if not expires_at or time.time() > expires_at:
            logger.warning(
                "Access Token has expired, it has to be renewed with the last known refresh token."
            )
            return False
        else:
            logger.info("Access Token is still valid and can be used.")
            return True

    def _post_to_token_endpoint(self, data):
        """
        Helper method to post data to the Strava OAuth token endpoint

        Args:
            data (dict): Data to post to the token endpoint

        Returns:
            tuple: Response object and JSON response if available
        """
        response = requests.post(self.STRAVA_OAUTH_TOKEN_ENDPOINT, data=data)
        try:
            return response, response.json()
        except json.decoder.JSONDecodeError:
            logger.error("Invalid JSON in response")
            return response, None

    @requires_ready
    def refresh_access_token(self):
        """
        Uses the refresh token to obtain a new access token from Strava.

        Updates user credentials upon success.

        Returns:
            None

        Raises:
            Exception: If the token refresh fails.
        """
        app_credentials = self.credentials_manager.get_app_credentials()
        data = {
            "client_id": app_credentials["client_id"],
            "client_secret": app_credentials["client_secret"],
            "refresh_token": self.user_oauth_credentials["refresh_token"],
            "grant_type": "refresh_token",
        }
        response, json_response = self._post_to_token_endpoint(data)

        if response.status_code == 200:
            self.user_oauth_credentials.update(
                {
                    "access_token": json_response["access_token"],
                    "refresh_token": json_response["refresh_token"],
                    "expires_at": json_response["expires_at"],
                }
            )
            logger.info("Success: access token has been refreshed")
        else:
            logger.error("Access token could not be refreshed")
            if json_response:
                logger.error(f"Response content: {json_response}")
            raise Exception(
                f"Access token could not be refreshed: {response.status_code}"
            )

    @requires_ready
    def exchange_authorization_code(self, authorization_code):
        """
        Exchanges an authorization code for access and refresh tokens.

        Updates internal user credentials on success.

        Args:
            authorization_code (str): Code received from Strava after user authorization.

        Returns:
            dict: JSON response from Strava on success.

        Raises:
            Exception: If the exchange fails.
        """
        app_credentials = self.credentials_manager.get_app_credentials()
        data = {
            "client_id": app_credentials["client_id"],
            "client_secret": app_credentials["client_secret"],
            "code": authorization_code,
            "grant_type": "authorization_code",
        }
        response, json_response = self._post_to_token_endpoint(data)

        if response.status_code == 200:
            self.user_oauth_credentials.update(
                {
                    "access_token": json_response["access_token"],
                    "refresh_token": json_response["refresh_token"],
                    "expires_at": json_response["expires_at"],
                }
            )
            logger.info("Authorization code exchanged successfully.")
            return json_response
        else:
            logger.error(
                f"Failed to exchange authorization code: {response.status_code}"
            )
            if json_response:
                logger.error(f"Response content: {json_response}")
            raise Exception(
                f"Authorization code could not be exchanged: {response.status_code}"
            )

    def check_if_ready(self):
        """
        Validates that the credentials manager is set and ready.

        Returns:
            bool: True if the token manager is ready.

        Raises:
            Exception: If the credentials manager is not ready.
        """
        if not self.credentials_manager or not self.credentials_manager.is_ready:
            self.is_ready = False
            error_msg = "Credentials manager is not set or not ready"
            logger.error(error_msg)
            raise Exception(error_msg)

        self.is_ready = True
        logger.info("StravaTokenManager is ready.")
        return True
