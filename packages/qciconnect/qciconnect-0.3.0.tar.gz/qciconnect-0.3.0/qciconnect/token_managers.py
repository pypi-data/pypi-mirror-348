import time
from keycloak import KeycloakOpenID

from qciconnect.exceptions import KeycloakTokenManagerException

class KeycloakTokenManager:
    """
    Manages communication with Keycloak server. 
    This comprises getting and refreshing tokens when needed.
    """
    def __init__(self, server_address: str, username: str, password: str):
        self.server_url = server_address.rstrip("/") + "/auth/"
        self.username = username
        self.password = password

        self.token = None
        self.header = None
        self.token_request_timestamp = 0
        self.token_expiration_time = 0
        self.token_refresh_expiration_time = 0

        self.keycloak_openid = KeycloakOpenID(server_url=self.server_url,
                                            client_id="react-client",
                                            realm_name="qciconnect",
                                            verify=True)

    def _update_timestamps(self) -> None:
        """
        Update the timestamp for token request and store information concerning expiration.
        """
        self.token_request_timestamp = time.time()
        self.token_expiration_time = int(self.token['expires_in'])
        self.token_refresh_expiration_time = int(self.token['refresh_expires_in'])

    def _is_token_expired(self) -> bool:
        """
        Check whether the current token has expired.
        """
        if self.token_request_timestamp + self.token_expiration_time < time.time():
            return True
        else:
            return False

    def _is_token_refreshable(self) -> bool:
        """
        Check whether the current token can be refreshed.
        """
        if self._is_token_expired() and \
           self.token_request_timestamp + self.token_refresh_expiration_time < time.time():
            return False
        else:
            return True
    

    def _ensure_token_validity(self) -> None:
        """
        Update the token, if necessary.
        """
        if self.token is None:
            try:
                self.token = self.keycloak_openid.token(username=self.username, password=self.password)
                self._update_timestamps()
            except Exception as e:
                raise KeycloakTokenManagerException(f"Error obtaining token from Keycloak: {e}")

        if self._is_token_expired() and self._is_token_refreshable():
            try:
                self.token = self.keycloak_openid.refresh_token(refresh_token=self.token['refresh_token'])
                self._update_timestamps()
            except Exception as e:
                raise KeycloakTokenManagerException(f"Error refreshing token from Keycloak: {e}")

        if self._is_token_expired() and not self._is_token_refreshable():
            try:
                self.token = self.keycloak_openid.token(username=self.username, password=self.password)
                self._update_timestamps()
            except Exception as e:
                raise KeycloakTokenManagerException(f"Error obtaining token from Keycloak: {e}")

    def get_auth_header(self) -> dict:
        """
        Get a dictionary that comprises the authorization header for the API.

        Returns: A dictionary with an authorization token.
        """
        self._ensure_token_validity()
        return { "Authorization": f"Bearer {self.token['access_token']}" }
    
    def add_auth_header(self, headers: dict) -> dict:
        """
        Add the "Authorization" header to a dictionary of headers. If necessary, a new token is created (or an 
        existing one is refreshed).

        Args:
            headers (dict): A dictionary of headers.
        Returns:
            dict: The updated input dictionary with the "Authorization" header added.
        """
        auth_header = self.get_auth_header()
        headers.update(auth_header)
        return headers

class DummyTokenManager:
    
   def __init__(self):
      pass
   
   def add_auth_header(self, headers: dict) -> dict:
        return headers
