class MusicGPTAPIError(Exception):
    """General API error for MusicGPT."""
    pass

class MusicGPTAuthError(MusicGPTAPIError):
    """Authentication error for MusicGPT."""
    pass

class MusicGPTNotFoundError(MusicGPTAPIError):
    """Resource not found error for MusicGPT."""
    pass

class MusicGPTRateLimitError(MusicGPTAPIError):
    """Rate limit exceeded error for MusicGPT."""
    pass
