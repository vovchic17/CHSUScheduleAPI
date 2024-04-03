class CHSUApiBaseError(Exception):
    """Base CHSU api error"""


class CHSUApiResponseError(CHSUApiBaseError):
    """Api response is invalid"""


class CHSUApiUnauthorizedError(CHSUApiBaseError):
    """Unauthorized"""


class CHSUApiLookupError(CHSUApiBaseError):
    """Group or lecturer id lookup error"""
