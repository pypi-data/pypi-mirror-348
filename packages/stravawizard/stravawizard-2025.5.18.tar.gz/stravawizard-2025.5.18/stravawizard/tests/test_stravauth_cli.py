import unittest
from datetime import datetime, timedelta
from unittest.mock import patch
from stravawizard.clients.oauth_client.stravauth_client import (
    StravauthClient,
)


class TestStravAuthClient(unittest.TestCase):

    def setUp(self):
        # Initialisation pour chaque test
        self.client = StravauthClient()
        self.client.credentials_manager.set_app_credentials(
            "your_client_id", "your_client_secret", "your_redirect_uri"
        )
        self.client.check_if_ready()

    def test_check_app_credentials(self):
        # Teste si la méthode détecte correctement les informations d'identification manquantes
        credentials_ok, _ = self.client.credentials_manager.check_app_credentials()
        self.assertTrue(credentials_ok)

        # Simule l'absence d'une information d'identification
        for (
            required_credential
        ) in self.client.credentials_manager.REQUIRED_APP_CREDENTIALS:
            old_credential_val = self.client.credentials_manager._app_credentials[
                required_credential
            ]
            self.client.credentials_manager._app_credentials[required_credential] = None
            credentials_ok, _ = self.client.credentials_manager.check_app_credentials()
            self.assertFalse(credentials_ok)
            self.client.credentials_manager._app_credentials[required_credential] = (
                old_credential_val
            )

    def test_exchange_authorization_code(self):
        # Teste si la méthode échange correctement le code d'autorisation
        with patch("requests.post") as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "access_token": "new_access_token",
                "refresh_token": "new_refresh_token",
                "expires_at": int((datetime.now() + timedelta(hours=1)).timestamp()),
                "athlete": "athlete_summary",
            }

            authorization_code = "authorization_code"
            response = self.client.exchange_authorization_code(authorization_code)

            self.assertEqual(response["access_token"], "new_access_token")
            self.assertEqual(response["refresh_token"], "new_refresh_token")

            # Vérifie si les attributs des managers ont été mis à jour correctement
            self.assertEqual(
                self.client.token_manager.user_oauth_credentials["access_token"],
                "new_access_token",
            )
            self.assertEqual(
                self.client.token_manager.user_oauth_credentials["refresh_token"],
                "new_refresh_token",
            )
            self.assertEqual(
                self.client.token_manager.user_oauth_credentials["expires_at"],
                int((datetime.now() + timedelta(hours=1)).timestamp()),
            )
            # Vérifie que le résumé de l'athlète a été mis à jour
            self.assertEqual(self.client.athlete_summary, "athlete_summary")


if __name__ == "__main__":
    unittest.main()
