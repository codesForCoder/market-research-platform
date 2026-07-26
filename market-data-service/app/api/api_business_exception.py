class AppBusinessException(Exception):
    """Base exception for all internal domain/business logic failures."""
    def __init__(self, error_code: str, message: str, status_code: int):
        self.error_code = error_code
        self.message = message
        self.status_code = status_code
        super().__init__(message)
