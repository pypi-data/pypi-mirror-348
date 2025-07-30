import base64
import logging
import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import requests
from crudclient import ClientConfig  # type: ignore[attr-defined]

# Set up logging
logger = logging.getLogger(__name__)


class TripletexConfig(ClientConfig):
    """
    Configuration class for the Tripletex API client.

    Handles authentication tokens, session management, and API endpoint details.
    """

    hostname: str = "https://tripletex.no/"
    version: str = "v2"
    consumer_token: str = os.getenv("TRIPLETEX_CONSUMER_TOKEN", "")
    employee_token: str = os.getenv("TRIPLETEX_EMPLOYEE_TOKEN", "")
    company_id: str = "0"

    session_token: Optional[str] = None
    session_expires_at: Optional[datetime] = None

    auth_type = "basic"

    def get_auth_token(self) -> Optional[str]:
        """
        Returns Base64-encoded `company_id:session_token` string.
        Called automatically by `auth()` from base class.
        """
        if self.session_token:
            raw = f"{self.company_id}:{self.session_token}"
            logger.debug("Creating auth token for company_id: %s", self.company_id)
            return base64.b64encode(raw.encode()).decode()
        logger.warning("No session token available for authentication")
        return None

    def is_token_expired(self) -> bool:
        """Checks if the current session token is expired."""
        if not self.session_token:
            logger.debug("No session token exists")
            return True
        if not isinstance(self.session_expires_at, datetime):
            logger.warning("Invalid expiration date format: %r", self.session_expires_at)
            return True

        # Make sure session_expires_at has timezone info
        expires_at = self.session_expires_at
        if expires_at.tzinfo is None:
            # Convert naive datetime to aware datetime by assuming it's in UTC
            expires_at = expires_at.replace(tzinfo=timezone.utc)

        is_expired = datetime.now(timezone.utc) >= expires_at

        if is_expired:
            logger.info("Session token has expired at %s", self.session_expires_at)
        else:
            logger.debug("Session token valid until %s", self.session_expires_at)
        return is_expired

    def create_date(self) -> str:
        """Generates the expiration date string for token creation (tomorrow)."""
        tomorrow_cet = (datetime.now(timezone.utc) + timedelta(days=2)).astimezone().date()
        expiration_str = tomorrow_cet.isoformat()
        logger.debug("Created expiration date: %s", expiration_str)
        return expiration_str

    def refresh_token(self, force: bool = False) -> None:
        """
        Refreshes the Tripletex session token.

        Args:
            force: If True, forces a refresh even if the token is not expired.

        Raises:
            ValueError: If consumer or employee tokens are missing.
            requests.RequestException: If the API request fails.
        """
        if not force and not self.is_token_expired():
            logger.debug("Skipping token refresh, current token is still valid")
            return

        logger.info("Refreshing Tripletex session token%s", " (forced)" if force else "")

        if not self.consumer_token or not self.employee_token:
            logger.error(
                "Missing required tokens for authentication. "
                "Make sure TRIPLETEX_CONSUMER_TOKEN and TRIPLETEX_EMPLOYEE_TOKEN "
                "environment variables are set"
            )
            raise ValueError("Missing required tokens for authentication")

        url = f"{self.base_url}/token/session/:create"
        params = {"consumerToken": self.consumer_token, "employeeToken": self.employee_token, "expirationDate": self.create_date()}

        logger.debug("Requesting new session token from %s with params: %s", url, params)
        try:
            response = requests.put(url, headers={}, params=params, timeout=self.timeout)
            logger.debug("Token refresh response status: %s, content: %s", response.status_code, response.content)
            response.raise_for_status()
            data = response.json()["value"]
            self.session_token = data["token"]
            self.session_expires_at = datetime.fromisoformat(data["expirationDate"])
            if self.session_expires_at.tzinfo is None:
                self.session_expires_at = self.session_expires_at.replace(tzinfo=timezone.utc)
            logger.info("Successfully obtained new session token, valid until %s", self.session_expires_at)
        except requests.RequestException as e:
            logger.error("Failed to refresh session token: %s", str(e), exc_info=True)
            raise

    def auth_with_company(self, company_id: str) -> Dict[str, Any]:
        """
        Returns the Basic auth header using the given company_id.

        Refreshes the token if it's expired.

        Args:
            company_id: The company ID to use for authentication.

        Returns:
            A dictionary containing the Authorization header.
        """
        logger.debug("Creating auth header for company ID: %s", company_id)
        if self.is_token_expired():
            logger.info("Token expired, refreshing before authentication")
            self.refresh_token()

        raw = f"{company_id}:{self.session_token}"
        encoded = base64.b64encode(raw.encode()).decode()
        return {"Authorization": f"Basic {encoded}"}

    def auth(self) -> Dict[str, Any]:
        """
        Returns the Basic auth header using the default company_id.
        """
        logger.debug("Getting authentication headers for default company: %s", self.company_id)
        return self.auth_with_company(self.company_id)

    def should_retry_on_403(self) -> bool:
        """Determines if a retry should occur on a 403 Forbidden response."""
        logger.debug("403 received, allowing retry with token refresh")
        return True

    def handle_403_retry(self, client: Any) -> None:
        """Handles the retry logic for a 403 response, forcing a token refresh."""
        logger.warning("Handling 403 response by forcing token refresh")
        self.refresh_token(force=True)


class TripletexTestConfig(TripletexConfig):
    """
    Configuration class specifically for the Tripletex test environment.
    Uses different hostname and environment variables for test tokens.
    """

    hostname: str = "https://api-test.tripletex.tech/"
    consumer_token: str = os.getenv("TRIPLETEX_TEST_CONSUMER_TOKEN", "")
    employee_token: str = os.getenv("TRIPLETEX_TEST_EMPLOYEE_TOKEN", "")
    log_request_body: bool = True
