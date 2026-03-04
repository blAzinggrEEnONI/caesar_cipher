"""
Result type for explicit error handling without exceptions.

This module provides a type-safe way to handle operations that can fail,
making error handling explicit in function signatures.
"""

from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

T = TypeVar('T')
E = TypeVar('E')
U = TypeVar('U')


@dataclass(frozen=True)
class Ok(Generic[T]):
    """
    Successful result containing a value.
    
    Examples:
        >>> result = Ok(42)
        >>> result.is_ok()
        True
        >>> result.unwrap()
        42
    """
    value: T
    
    def is_ok(self) -> bool:
        """Check if this is a successful result."""
        return True
    
    def is_err(self) -> bool:
        """Check if this is an error result."""
        return False
    
    def map(self, func: Callable[[T], U]) -> 'Ok[U] | Err[E]':
        """
        Transform the success value.
        
        Args:
            func: Function to apply to the value
            
        Returns:
            Ok with transformed value
            
        Examples:
            >>> Ok(5).map(lambda x: x * 2)
            Ok(value=10)
        """
        return Ok(func(self.value))
    
    def bind(self, func: Callable[[T], 'Ok[U] | Err[E]']) -> 'Ok[U] | Err[E]':
        """
        Chain operations that return Results (flatMap/monadic bind).
        
        Args:
            func: Function that takes value and returns a Result
            
        Returns:
            Result from applying func to the value
            
        Examples:
            >>> def safe_divide(x: int) -> Ok[int] | Err[str]:
            ...     return Ok(10 // x) if x != 0 else Err("division by zero")
            >>> Ok(2).bind(safe_divide)
            Ok(value=5)
        """
        return func(self.value)
    
    def unwrap(self) -> T:
        """
        Extract the value (safe for Ok).
        
        Returns:
            The contained value
        """
        return self.value
    
    def unwrap_or(self, default: T) -> T:
        """
        Extract value or return default.
        
        Args:
            default: Value to return if this is Err
            
        Returns:
            The contained value (ignores default)
        """
        return self.value


@dataclass(frozen=True)
class Err(Generic[E]):
    """
    Failed result containing an error.
    
    Examples:
        >>> result = Err("something went wrong")
        >>> result.is_err()
        True
        >>> result.unwrap_or(0)
        0
    """
    error: E
    
    def is_ok(self) -> bool:
        """Check if this is a successful result."""
        return False
    
    def is_err(self) -> bool:
        """Check if this is an error result."""
        return True
    
    def map(self, func: Callable[[T], U]) -> 'Err[E]':
        """
        No-op for errors (preserves the error).
        
        Args:
            func: Function to apply (ignored for Err)
            
        Returns:
            Self unchanged
        """
        return self
    
    def bind(self, func: Callable[[T], 'Ok[U] | Err[E]']) -> 'Err[E]':
        """
        No-op for errors (preserves the error).
        
        Args:
            func: Function to apply (ignored for Err)
            
        Returns:
            Self unchanged
        """
        return self
    
    def unwrap(self) -> T:
        """
        Raises error (use only when certain it's Ok).
        
        Raises:
            ValueError: Always, with the error message
        """
        raise ValueError(f"Called unwrap on Err: {self.error}")
    
    def unwrap_or(self, default: T) -> T:
        """
        Return default for errors.
        
        Args:
            default: Value to return since this is Err
            
        Returns:
            The default value
        """
        return default


# Type alias for Result - can be either Ok or Err
Result = Ok[T] | Err[E]
