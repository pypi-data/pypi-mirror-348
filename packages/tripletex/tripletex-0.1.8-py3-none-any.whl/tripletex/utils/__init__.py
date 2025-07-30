"""Utility functions for the Tripletex API client."""

from datetime import datetime, timedelta
from typing import Any, Dict, Optional


def ensure_date_params(
    params: Optional[Dict[str, Any]] = None,
    date_from_key: str = "dateFrom",
    date_to_key: str = "dateTo",
) -> Dict[str, Any]:
    """
    Ensure that date parameters are present in the params dictionary.

    Many Tripletex API endpoints require date range parameters. This utility
    function ensures that these parameters are present, defaulting to yesterday
    and today if not provided.

    Args:
        params: Optional dictionary of parameters. If None, a new dict is created.
        date_from_key: The key to use for the 'from' date parameter (default: "dateFrom").
        date_to_key: The key to use for the 'to' date parameter (default: "dateTo").

    Returns:
        Dict with date parameters added if they were not already present.
    """
    if params is None:
        params = {}
    else:
        # Create a copy to avoid modifying the original
        params = params.copy()

    # Only generate date strings if needed
    if date_from_key not in params or date_to_key not in params:
        today = datetime.now().strftime("%Y-%m-%d")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        # Use setdefault to only set if not already present
        params.setdefault(date_from_key, yesterday)
        params.setdefault(date_to_key, today)

    return params
