from enum import IntEnum


class ErrorCode(IntEnum):
    """Error codes for Dhan Data API responses.

    Each error code represents a specific error condition returned by the Dhan Data API.

    Attributes:
        INTERNAL_SERVER_ERROR: Internal Server Error (Code: 800)
        INSTRUMENT_LIMIT_EXCEEDED: Requested number of instruments exceeds limit (Code: 804)
        TOO_MANY_REQUESTS: Too many requests or connections. Further requests may result in the user being blocked (Code: 805)
        DATA_API_NOT_SUBSCRIBED: Data APIs not subscribed (Code: 806)
        ACCESS_TOKEN_EXPIRED: Access token is expired (Code: 807)
        AUTHENTICATION_FAILED: Authentication Failed - Client ID or Access Token invalid (Code: 808)
        ACCESS_TOKEN_INVALID: Access token is invalid (Code: 809)
        CLIENT_ID_INVALID: Client ID is invalid (Code: 810)
        INVALID_EXPIRY_DATE: Invalid Expiry Date (Code: 811)
        INVALID_DATE_FORMAT: Invalid Date Format (Code: 812)
        INVALID_SECURITY_ID: Invalid SecurityId (Code: 813)
        INVALID_REQUEST: Invalid Request (Code: 814)
    """

    INTERNAL_SERVER_ERROR = 800

    INSTRUMENT_LIMIT_EXCEEDED = 804
    TOO_MANY_REQUESTS = 805

    DATA_API_NOT_SUBSCRIBED = 806

    ACCESS_TOKEN_EXPIRED = 807
    AUTHENTICATION_FAILED = 808
    ACCESS_TOKEN_INVALID = 809
    CLIENT_ID_INVALID = 810

    INVALID_EXPIRY_DATE = 811
    INVALID_DATE_FORMAT = 812
    INVALID_SECURITY_ID = 813
    INVALID_REQUEST = 814