class TeamXError(Exception):
    """Base exception for TeamXBot errors."""
    pass

class TokenInvalidError(TeamXError):
    """Raised when the bot token is invalid or empty."""
    pass

class APIError(TeamXError):
    """Raised when Telegram API returns an error."""
    pass

class HandlerError(TeamXError):
    """Raised when a handler fails."""
    pass

class BotRunningError(TeamXError):
    """Raised when trying to start a bot that is already running."""
    pass

class FileNotFoundError(TeamXError):
    """Raised when a file is not found."""
    pass