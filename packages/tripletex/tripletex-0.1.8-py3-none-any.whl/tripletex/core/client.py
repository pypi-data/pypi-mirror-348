from __future__ import annotations

import logging
import os
from typing import Any, Optional, Protocol

import requests  # Need this for type hints and accessing response
from crudclient.client import Client
from crudclient.exceptions import RateLimitError  # Need this exception

from tripletex.core.config import TripletexConfig, TripletexTestConfig

log = logging.getLogger(__name__)


class RateLimiterProtocol(Protocol):
    """Protocol for rate limiter objects."""

    def check_and_wait(self, dynamic_threshold: int, calls_to_make: int = 1) -> None:
        """Check if we need to wait for rate limit reset and wait if necessary."""

    def update_from_headers(self, headers: Any) -> None:
        """Update the rate limit state based on API response headers."""


class TripletexClient(Client):
    """
    Custom HTTP client for interacting with the Tripletex API.

    Handles configuration loading (production or test) and overrides
    the base request method to potentially skip response handling for DELETE requests.
    Includes rate limiting support via the FileBasedRateLimiter.
    """

    def __init__(
        self,
        config: TripletexConfig | None = None,
        rate_limiter: RateLimiterProtocol | None = None,
        num_workers: int = 1,  # Number of worker processes for dynamic threshold calculation
        buffer_size: int = 10,  # Buffer size for rate limit threshold
    ) -> None:
        """
        Initialize the Tripletex client.

        Args:
            config: An optional configuration object. If None, loads
                   TripletexTestConfig if DEBUG env var is "1", otherwise TripletexConfig.
            rate_limiter: A rate limiter object implementing RateLimiterProtocol.
                          Used for cross-process rate limiting.
            num_workers: Number of worker processes for dynamic threshold calculation.
                         Used to calculate the rate limit threshold.
            buffer_size: Buffer size for rate limit threshold.
                         Added to num_workers to determine when to start waiting.
        """
        if config is None:
            config = TripletexTestConfig() if os.getenv("DEBUG", "") == "1" else TripletexConfig()

        super().__init__(config=config)

        # Store worker count and buffer size for dynamic threshold calculation
        self._num_workers = num_workers
        self._buffer_size = buffer_size

        # Store the rate limiter
        self._rate_limiter = rate_limiter

        if self._rate_limiter is not None:
            log.info(f"TripletexClient initialized with rate limiting. Workers: {num_workers}, Buffer: {buffer_size}")
        else:
            log.warning("TripletexClient initialized WITHOUT rate limiting. API rate limits may be exceeded.")

    def _update_rate_limit_state(self, response: Optional[requests.Response]) -> None:
        """
        Helper to update rate limit state from a response object.

        Extracts rate limit information from response headers and updates
        the rate limiter state if available.
        """
        if response is None or self._rate_limiter is None:
            return

        self._rate_limiter.update_from_headers(response.headers)

    def _wait_for_rate_limit(self) -> None:
        """
        Checks rate limit and waits if necessary using the rate limiter.

        Uses a dynamic threshold based on the number of workers and a configurable buffer.
        The threshold is calculated as num_workers + buffer_size.
        """
        # Calculate dynamic threshold based on worker count and buffer size
        dynamic_threshold = self._num_workers + self._buffer_size

        # Use the rate limiter if available
        if self._rate_limiter is not None:
            self._rate_limiter.check_and_wait(dynamic_threshold=dynamic_threshold)
        else:
            log.warning("No rate limiter available. Proceeding without rate limit check.")

    def _request(self, method: str, endpoint: str | None = None, url: str | None = None, **kwargs: Any) -> Any:
        """
        Sends an HTTP request to the Tripletex API.

        Overrides the base method to conditionally skip response handling,
        specifically for DELETE requests where Tripletex might return an empty body.

        Args:
            method: The HTTP method (e.g., 'GET', 'POST', 'DELETE').
            endpoint: The API endpoint path (appended to base_url).
            url: An absolute URL to use instead of base_url + endpoint.
            **kwargs: Additional arguments passed to the underlying request library.

        Returns:
            The processed response data (usually a dict or list) or raw response object,
            depending on the base client's implementation and the handle_response flag.
        """
        # Original handle_response logic (specific to TripletexClient)
        original_handle_response = method != "DELETE"
        # Get handle_response from kwargs if provided, otherwise use default
        handle_response_arg = kwargs.pop("handle_response", original_handle_response)

        # --- Rate Limiting Wait ---
        self._wait_for_rate_limit()
        # --- End Rate Limiting Wait ---

        raw_response: Optional[requests.Response] = None
        result: Any = None
        try:
            # Always call super()._request with handle_response=False to get the raw response
            # We need the raw response to access headers for rate limiting state update.
            # Ensure the request uses the potentially modified kwargs
            raw_response = super()._request(method, endpoint=endpoint, url=url, handle_response=False, **kwargs)

            # Now, handle the response processing based on the original handle_response_arg
            if handle_response_arg:
                # Manually trigger response handling using the http_client's handler
                # This mimics what crudclient.Client._request -> http_client._request -> _handle_request_response does
                try:
                    # Ensure response is valid before handling
                    if not isinstance(raw_response, requests.Response):
                        raise TypeError(f"Expected requests.Response, got {type(raw_response).__name__}")
                    # Raise HTTP errors (like 4xx, 5xx) to be caught below or handled by caller
                    raw_response.raise_for_status()
                    # Process the successful response using the handler from the http_client
                    result = self.http_client.response_handler.handle_response(raw_response)
                except requests.HTTPError as http_err:
                    # Let crudclient's error handling take over if raise_for_status fails
                    # We still update rate limit state in finally block
                    self.http_client._handle_http_error(http_err)  # This will raise the appropriate CrudClientError
                    # This line technically shouldn't be reached if _handle_http_error raises
                    raise http_err from http_err
            else:
                # If original request didn't want handling, return the raw response
                result = raw_response

        except RateLimitError as rle:
            # If super()._request raises RateLimitError, try to update state from its response
            log.error(f"RATE LIMIT ERROR (429): Request hit rate limit. Response: {getattr(rle, 'response', None)}")
            self._update_rate_limit_state(rle.response)
            raise rle  # Re-raise the exception
        except Exception as e:
            # Catch other exceptions, potentially update state if response is available
            response_for_update = None
            if isinstance(raw_response, requests.Response):
                response_for_update = raw_response
            elif hasattr(e, "response") and isinstance(e.response, requests.Response):
                response_for_update = e.response  # type: ignore

            if response_for_update:
                # Check if this is a 429 Too Many Requests error
                if response_for_update.status_code == 429:
                    log.error(f"RATE LIMIT ERROR (429): Request failed with status 429. Headers: {response_for_update.headers}")
                self._update_rate_limit_state(response_for_update)

            # Re-raise the original exception if one occurred
            if isinstance(e, Exception) and not isinstance(e, RateLimitError):  # RateLimitError already handled
                raise e

        finally:
            # Final attempt to update state if we have a raw response
            # (covers cases where handling failed but we got a response)
            if raw_response is not None and isinstance(raw_response, requests.Response):
                self._update_rate_limit_state(raw_response)

        return result
