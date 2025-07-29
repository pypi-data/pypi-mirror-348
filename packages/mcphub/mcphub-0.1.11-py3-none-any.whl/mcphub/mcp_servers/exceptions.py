class ServerConfigNotFoundError(Exception):
    """Raised when a server configuration is not found."""
    pass

class SetupError(Exception):
    """Raised when there's an error during server setup."""
    pass 