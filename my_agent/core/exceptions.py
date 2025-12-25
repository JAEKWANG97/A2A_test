"""Custom exceptions for A2A system."""


class A2AException(Exception):
    """Base exception for A2A system."""
    pass


class AgentNotFoundError(A2AException):
    """Raised when requested agent is not found in registry."""
    pass


class SessionNotFoundError(A2AException):
    """Raised when session does not exist."""
    pass


class ToolExecutionError(A2AException):
    """Raised when tool execution fails."""
    pass
