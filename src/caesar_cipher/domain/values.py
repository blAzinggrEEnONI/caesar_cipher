"""
Domain value objects representing core business concepts.

Value objects are immutable and validate their invariants on creation.
"""

from dataclasses import dataclass
from typing import NewType

from caesar_cipher.core.result import Err, Ok, Result

# Type aliases for domain primitives
# These prevent mixing PlainText and CipherText accidentally
PlainText = NewType('PlainText', str)
CipherText = NewType('CipherText', str)


@dataclass(frozen=True)
class Shift:
    """
    Represents a Caesar cipher shift value.
    
    Invariants:
        - Value must be in range [0, 25]
        - Normalized to positive values
        - shift + inverse ≡ 0 (mod 26)
    
    Examples:
        >>> shift = Shift.create(3).unwrap()
        >>> shift.value
        3
        >>> shift.inverse().value
        23
        >>> Shift.create(27).unwrap().value
        1
        >>> Shift.create(-5).unwrap().value
        21
    """
    value: int
    
    @staticmethod
    def create(value: int) -> Result['Shift', str]:
        """
        Create a validated Shift value.
        
        Args:
            value: Integer shift amount (will be normalized to [0, 25])
            
        Returns:
            Ok(Shift) with normalized value
            
        Design Decision:
            We always return Ok because any integer can be normalized.
            This makes the API simpler while maintaining type safety.
        """
        normalized = value % 26
        return Ok(Shift(value=normalized))
    
    def inverse(self) -> 'Shift':
        """
        Return the inverse shift for decryption.
        
        Returns:
            Shift that reverses this shift
            
        Mathematical Property:
            For any shift s, s + s.inverse() ≡ 0 (mod 26)
            
        Examples:
            >>> Shift(3).inverse()
            Shift(value=23)
            >>> Shift(0).inverse()
            Shift(value=0)
        """
        return Shift(value=(26 - self.value) % 26)


@dataclass(frozen=True)
class FrequencyScore:
    """
    Chi-squared score for frequency analysis.
    
    Lower scores indicate better match to English letter distribution.
    
    Properties:
        - Always non-negative
        - 0 means perfect match
        - infinity means no letters to analyze
    
    Examples:
        >>> score1 = FrequencyScore(value=10.5)
        >>> score2 = FrequencyScore(value=20.3)
        >>> score1.is_better_than(score2)
        True
    """
    value: float
    
    def is_better_than(self, other: 'FrequencyScore') -> bool:
        """
        Compare scores (lower is better).
        
        Args:
            other: Score to compare against
            
        Returns:
            True if this score is better (lower) than other
        """
        return self.value < other.value


@dataclass(frozen=True)
class CrackResult:
    """
    Result of attempting to crack a cipher with a specific shift.
    
    Aggregates the shift used, resulting plaintext, and quality score.
    
    Examples:
        >>> result = CrackResult(
        ...     shift=Shift(3),
        ...     plaintext=PlainText("HELLO"),
        ...     score=FrequencyScore(15.2)
        ... )
        >>> result.is_likely_correct()
        True
    """
    shift: Shift
    plaintext: PlainText
    score: FrequencyScore
    
    def is_likely_correct(self, threshold: float = 100.0) -> bool:
        """
        Check if score suggests correct decryption.
        
        Args:
            threshold: Maximum score to consider likely correct
            
        Returns:
            True if score is below threshold
            
        Design Decision:
            Default threshold of 100.0 is empirically determined.
            English text typically scores below 50, random text above 200.
        """
        return self.score.value < threshold
