class CHSUApiBaseError(Exception):
    """Base CHSU api error"""


class CHSUApiResponseError(CHSUApiBaseError):
    """Api response is invalid"""


class CHSUApiUnauthorizedError(CHSUApiBaseError):
    """Unauthorized"""
