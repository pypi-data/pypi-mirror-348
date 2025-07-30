import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class StravaBaseApiClient(ABC):
    """
    Base class for Strava API clients with common functionality
    """

    API_BASE_URL = "https://www.strava.com/api/v3"

    def __init__(self):
        self.is_ready = False

    @abstractmethod
    def check_if_ready(self):
        """
        Abstract method to be implemented to check if the client is ready
        """
        pass
