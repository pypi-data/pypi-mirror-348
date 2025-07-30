"""
File-based rate limiter for cross-process synchronization.

This module provides a robust rate limiting mechanism that works across
independent processes, such as pytest-xdist workers, by using file-based
locking and state storage.
"""

import json
import logging
import os
import sys
import time
from typing import Any, Dict, Optional, Union

# Platform-specific imports for file locking
if sys.platform == "win32":
    import msvcrt
else:
    import fcntl

logger = logging.getLogger(__name__)


class FileBasedRateLimiter:
    """
    A rate limiter that uses file-based locking for cross-process synchronization.

    This implementation uses OS-level file locking to ensure atomic operations
    on the rate limit state across independent processes, making it suitable
    for use with pytest-xdist.

    On Unix-like systems (Linux, macOS), it uses fcntl.flock.
    On Windows, it uses msvcrt.locking.

    The rate limit state (remaining calls and reset timestamp) is stored in a JSON
    file, and a separate lock file is used to ensure atomic read/write operations.
    """

    def __init__(
        self,
        lock_file_path: str,
        state_file_path: str,
        default_remaining: int = -1,
        default_reset_ts: float = 0.0,
    ):
        """
        Initialize the file-based rate limiter.

        Args:
            lock_file_path: Path to the lock file used for synchronization.
            state_file_path: Path to the JSON file storing rate limit state.
            default_remaining: Default value for remaining calls (-1 for unknown).
            default_reset_ts: Default value for reset timestamp (0.0 for unknown).
        """
        self.lock_file_path = lock_file_path
        self.state_file_path = state_file_path
        self.default_remaining = default_remaining
        self.default_reset_ts = default_reset_ts
        self._lock_file_fd: Optional[Any] = None  # File descriptor for the lock file

        # Ensure lock file exists for flock
        os.makedirs(os.path.dirname(self.lock_file_path), exist_ok=True)
        if not os.path.exists(self.lock_file_path):
            with open(self.lock_file_path, "w") as _:
                pass  # Create empty lock file

        logger.info(f"FileBasedRateLimiter initialized with lock_file={lock_file_path}, " f"state_file={state_file_path}")

    def _acquire_lock(self) -> None:
        """Acquire an exclusive lock on the lock file."""
        if self._lock_file_fd is not None:
            logger.warning("Attempting to acquire lock when already held")
            return

        # Open the lock file - different modes for different platforms
        if sys.platform == "win32":
            # Windows requires a file opened in binary mode for locking
            self._lock_file_fd = open(self.lock_file_path, "r+b")  # type: ignore
            # Get file size for locking the entire file
            file_size = os.path.getsize(self.lock_file_path)
            if file_size == 0:
                # Write a byte to ensure the file has content to lock
                self._lock_file_fd.write(b"\0")
                self._lock_file_fd.flush()
                file_size = 1
            # Lock the entire file exclusively
            msvcrt.locking(self._lock_file_fd.fileno(), msvcrt.LK_LOCK, file_size)
        else:
            # Unix systems
            self._lock_file_fd = open(self.lock_file_path, "r")  # type: ignore
            fcntl.flock(self._lock_file_fd.fileno(), fcntl.LOCK_EX)  # type: ignore

        logger.debug(f"Acquired lock: {self.lock_file_path}")

    def _release_lock(self) -> None:
        """Release the lock on the lock file."""
        if self._lock_file_fd is None:
            logger.warning("Attempting to release lock when not held")
            return

        if sys.platform == "win32":
            # Windows unlock
            file_size = os.path.getsize(self.lock_file_path)
            try:
                # Unlock the file
                msvcrt.locking(self._lock_file_fd.fileno(), msvcrt.LK_UNLCK, file_size)
            except OSError:
                # Sometimes Windows throws an error when unlocking, but it still works
                logger.debug("Ignoring Windows unlock error (expected behavior)")
        else:
            # Unix unlock
            fcntl.flock(self._lock_file_fd.fileno(), fcntl.LOCK_UN)

        self._lock_file_fd.close()
        self._lock_file_fd = None
        logger.debug(f"Released lock: {self.lock_file_path}")

    def _read_state(self) -> Dict[str, Union[int, float]]:
        """
        Read the current rate limit state from the state file.

        Returns:
            A dictionary with 'remaining_calls' (int) and 'reset_timestamp' (float).
        """
        try:
            if os.path.exists(self.state_file_path):
                with open(self.state_file_path, "r") as f:
                    state = json.load(f)
                    if not isinstance(state.get("remaining_calls"), int) or not isinstance(state.get("reset_timestamp"), (float, int)):
                        raise ValueError("Invalid state format")
                    return state
        except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
            logger.warning(f"State file '{self.state_file_path}' not found or invalid: {e}. " f"Initializing with defaults.")

        # Return default state if file doesn't exist or is invalid
        return {"remaining_calls": self.default_remaining, "reset_timestamp": self.default_reset_ts}

    def _write_state(self, remaining_calls: int, reset_timestamp: Union[int, float]) -> None:
        """
        Write the rate limit state to the state file.

        Args:
            remaining_calls: Number of API calls remaining in the current window.
            reset_timestamp: Timestamp when the rate limit window resets.
        """
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.state_file_path), exist_ok=True)

        with open(self.state_file_path, "w") as f:
            json.dump({"remaining_calls": remaining_calls, "reset_timestamp": reset_timestamp}, f)
        logger.debug(f"Updated state file: remaining={remaining_calls}, " f"reset_ts={reset_timestamp:.2f}")

    def check_and_wait(self, dynamic_threshold: int, calls_to_make: int = 1) -> None:
        """
        Check if we need to wait for rate limit reset and wait if necessary.

        This method implements the core rate limiting logic:
        1. If the remaining calls are unknown, proceed optimistically.
        2. If the remaining calls are known and below the threshold, wait until reset.
        3. If allowed to proceed, decrement the remaining calls counter.

        Args:
            dynamic_threshold: The threshold below which to start waiting.
                This is typically calculated as num_workers + buffer_size.
            calls_to_make: Number of API calls that will be made (default: 1).
        """
        try:
            self._acquire_lock()

            while True:  # Loop until allowed to proceed
                now = time.monotonic()

                # Read current state
                state = self._read_state()
                remaining = state["remaining_calls"]
                reset_ts = state["reset_timestamp"]
                is_unknown = remaining == self.default_remaining

                # Reset remaining count if reset time has passed
                if now >= reset_ts and not is_unknown:
                    logger.debug("Rate limit reset time passed. Resetting count to unknown.")
                    remaining = self.default_remaining
                    is_unknown = True

                # Check if we need to wait
                if not is_unknown and remaining <= dynamic_threshold:
                    wait_time = reset_ts - now
                    if wait_time <= 0:
                        # Reset time passed while checking, reset state and restart loop
                        logger.debug("Rate limit reset time passed during check. Re-evaluating.")
                        self._write_state(self.default_remaining, 0.0)
                        continue  # Restart the while loop

                    wait_time += 1  # Add buffer
                    reset_time_str = time.strftime("%H:%M:%S", time.localtime(time.time() + wait_time))
                    logger.warning(
                        f"RATE LIMIT WAIT: Remaining={remaining}, Threshold={dynamic_threshold}, "
                        f"Reset={reset_ts:.2f} (in {wait_time:.2f}s at {reset_time_str}). "
                        f"Waiting for rate limit reset..."
                    )

                    # Release lock during sleep
                    self._release_lock()
                    try:
                        time.sleep(wait_time)
                    finally:
                        # Re-acquire lock after sleep
                        self._acquire_lock()

                    # After waiting, restart the loop to re-check the condition
                    continue

                # If allowed to proceed
                elif not is_unknown:
                    # Decrement before releasing the lock
                    new_remaining = int(remaining - calls_to_make)  # Ensure it's an int
                    self._write_state(new_remaining, reset_ts)
                    logger.info(
                        f"Proceeding with request. Decremented rate limit remaining " f"count to {new_remaining} (threshold={dynamic_threshold})"
                    )
                    break  # Exit the while loop, permission granted

                # Proceed if limit is unknown
                else:  # is_unknown is True
                    logger.info(f"Rate limit remaining is unknown. Proceeding optimistically " f"with threshold={dynamic_threshold}.")
                    break  # Exit the while loop, permission granted

        finally:
            # Ensure lock is released even if an exception occurs
            if self._lock_file_fd is not None:
                self._release_lock()

    def update_from_headers(self, headers: Dict[str, Any]) -> None:
        """
        Update the rate limit state based on API response headers.

        Args:
            headers: Dictionary of response headers, which should include
                'X-Rate-Limit-Remaining' and 'X-Rate-Limit-Reset'.
        """
        try:
            remaining_str = headers.get("X-Rate-Limit-Remaining")
            reset_str = headers.get("X-Rate-Limit-Reset")  # Seconds until reset

            if remaining_str is None or reset_str is None:
                logger.debug("Rate limit headers not found in response")
                return

            try:
                remaining = int(remaining_str)
                reset_seconds = int(reset_str)
                now = time.monotonic()
                new_reset_timestamp = now + reset_seconds

                self._acquire_lock()

                # Read current state
                state = self._read_state()
                current_remaining = state["remaining_calls"]
                current_reset_ts = state["reset_timestamp"]

                # Use a large number if remaining is unknown
                current_remaining_comp = float("inf") if current_remaining == self.default_remaining else current_remaining

                # Update only if the new info is relevant
                # (more recent reset or same reset time with lower count)
                if new_reset_timestamp > current_reset_ts or (new_reset_timestamp == current_reset_ts and remaining < current_remaining_comp):
                    self._write_state(remaining, new_reset_timestamp)
                    logger.info(
                        f"Updated rate limit state from headers: "
                        f"Remaining={remaining}, ResetIn={reset_seconds}s "
                        f"(Timestamp={new_reset_timestamp:.2f})"
                    )

            except (ValueError, TypeError) as parse_err:
                logger.warning(f"Could not parse rate limit headers: {parse_err}")

        except Exception as e:
            logger.warning(f"Error processing rate limit headers: {e}")

        finally:
            # Ensure lock is released even if an exception occurs
            if self._lock_file_fd is not None:
                self._release_lock()
