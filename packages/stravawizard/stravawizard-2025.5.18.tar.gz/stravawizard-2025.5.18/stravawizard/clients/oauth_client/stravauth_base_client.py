from abc import ABC, abstractmethod


class StravauthBaseClient(ABC):
    """
    Base class that handles configuration and readiness state
    """

    STRAVA_OAUTH_BASE_ENDPOINT = "https://www.strava.com/oauth/"
    STRAVA_OAUTH_TOKEN_ENDPOINT = f"{STRAVA_OAUTH_BASE_ENDPOINT}token"

    def __init__(self):
        self.is_ready = False
        self._app_credentials = {}
        self.scope = "read_all,activity:read_all"

    @abstractmethod
    def check_if_ready(self):
        """
        Abstract method to be implemented to check if the client is ready
        """
        pass
