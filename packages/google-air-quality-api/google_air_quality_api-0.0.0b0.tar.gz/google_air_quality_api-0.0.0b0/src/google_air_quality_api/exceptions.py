"""Exceptions for Google Air Quality API calls."""


class GoogleAirQuailityApiError(Exception):
    """Error talking to the Google Air Quality API."""


class ApiError(GoogleAirQuailityApiError):
    """Raised during problems talking to the API."""


class AuthError(GoogleAirQuailityApiError):
    """Raised due to auth problems talking to API."""


class ApiForbiddenError(GoogleAirQuailityApiError):
    """Raised due to permission errors talking to API."""


class NoDataForLocationError(GoogleAirQuailityApiError):
    """Raised due to permission errors talking to API."""
