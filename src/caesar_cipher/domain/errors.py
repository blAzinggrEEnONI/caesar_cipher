"""
Domain-specific errors with rich context.

All errors capture operation context for better debugging and user feedback.
"""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class DomainError:
    """
    Base class for all domain errors.
    
    Captures both human-readable message and structured context.
    
    Design Decision:
        Using frozen dataclass ensures errors are immutable and hashable.
        Context dict allows flexible error enrichment as errors propagate.
    
    Examples:
        >>> error = DomainError(
        ...     message="Operation failed",
        ...     context={"operation": "encrypt", "input": "test"}
        ... )
        >>> enriched = error.with_context(user="alice")
        >>> enriched.context["user"]
        'alice'
    """
    message: str
    context: dict[str, Any]
    
    def with_context(self, **kwargs: Any) -> 'DomainError':
        """
        Add additional context to error.
        
        Args:
            **kwargs: Additional context key-value pairs
            
        Returns:
            New error instance with merged context
            
        Design Decision:
            Returns new instance to maintain immutability.
            Allows error enrichment as it propagates up the call stack.
        """
        new_context = {**self.context, **kwargs}
        return type(self)(message=self.message, context=new_context)


@dataclass(frozen=True)
class ValidationError(DomainError):
    """
    Error when input validation fails.
    
    Used for:
        - Invalid shift values
        - Empty or malformed input
        - Constraint violations
    
    Examples:
        >>> error = ValidationError(
        ...     message="Shift value out of range",
        ...     context={"value": 100, "valid_range": "[0, 25]"}
        ... )
    """
    pass


@dataclass(frozen=True)
class CipherError(DomainError):
    """
    Error during cipher operations.
    
    Used for:
        - Encryption failures
        - Decryption failures
        - Invalid cipher state
    
    Examples:
        >>> error = CipherError(
        ...     message="Cannot encrypt empty text",
        ...     context={"operation": "encrypt", "text_length": 0}
        ... )
    """
    pass


@dataclass(frozen=True)
class AnalysisError(DomainError):
    """
    Error during frequency analysis.
    
    Used for:
        - Insufficient text for analysis
        - Invalid frequency data
        - Analysis computation failures
    
    Examples:
        >>> error = AnalysisError(
        ...     message="Cannot analyze empty text",
        ...     context={"operation": "crack", "text_length": 0}
        ... )
    """
    pass


@dataclass(frozen=True)
class FileIOError(DomainError):
    """
    Error during I/O operations.

    Used for:
        - File not found
        - Permission denied
        - Read/write failures

    Examples:
        >>> error = FileIOError(
        ...     message="File not found",
        ...     context={"path": "/tmp/missing.txt", "operation": "read"}
        ... )
    """
    pass
