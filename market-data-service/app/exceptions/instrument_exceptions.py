class InstrumentDownloadException(Exception):
    """Raised when downloading instrument master fails."""


class SeedInstrumentNotFoundException(Exception):
    """Raised when bundled seed instrument master is missing."""
