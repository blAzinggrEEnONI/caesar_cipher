"""
Domain services encapsulating business logic.

Services coordinate between value objects and use injected dependencies
for operations that don't belong to a single entity.
"""

from typing import Sequence

from caesar_cipher.core.result import Err, Ok, Result
from caesar_cipher.domain.errors import AnalysisError
from caesar_cipher.domain.values import (
    CipherText,
    CrackResult,
    PlainText,
    Shift,
)
from caesar_cipher.ports.interfaces import (
    CipherEnginePort,
    FrequencyAnalyzerPort,
)


class CipherService:
    """
    Domain service for cipher operations.
    
    This is the functional core - pure business logic with no I/O.
    All dependencies are injected via constructor.
    
    Design Philosophy:
        - Dependency injection for testability
        - Returns Result types for operations that can fail
        - Coordinates between domain objects and ports
        - No direct I/O or infrastructure dependencies
        
    Examples:
        >>> from caesar_cipher.core.cipher_engine import PureCipherEngine
        >>> engine = PureCipherEngine()
        >>> service = CipherService(engine)
        >>> plaintext = PlainText("HELLO")
        >>> shift = Shift(3)
        >>> ciphertext = service.encrypt_text(plaintext, shift)
        >>> ciphertext
        CipherText('KHOOR')
    """
    
    def __init__(self, engine: CipherEnginePort):
        """
        Initialize service with cipher engine.
        
        Args:
            engine: Implementation of cipher algorithm
            
        Design Decision:
            Takes Protocol (interface) not concrete class.
            Allows swapping implementations without changing service.
        """
        self._engine = engine
    
    def encrypt_text(
        self, 
        plaintext: PlainText, 
        shift: Shift
    ) -> CipherText:
        """
        Encrypt plaintext using Caesar cipher.
        
        This is a pure function - same inputs always produce same output.
        
        Args:
            plaintext: Text to encrypt
            shift: Number of positions to shift
            
        Returns:
            Encrypted ciphertext
            
        Examples:
            >>> service = CipherService(engine)
            >>> service.encrypt_text(PlainText("HELLO"), Shift(3))
            CipherText("KHOOR")
            
        Design Decision:
            Does not return Result because encryption cannot fail
            with valid inputs. Type system ensures validity.
        """
        return self._engine.encrypt(plaintext, shift)
    
    def decrypt_text(
        self, 
        ciphertext: CipherText, 
        shift: Shift
    ) -> PlainText:
        """
        Decrypt ciphertext using Caesar cipher.
        
        Args:
            ciphertext: Text to decrypt
            shift: Number of positions to shift back
            
        Returns:
            Decrypted plaintext
            
        Examples:
            >>> service = CipherService(engine)
            >>> service.decrypt_text(CipherText("KHOOR"), Shift(3))
            PlainText("HELLO")
        """
        return self._engine.decrypt(ciphertext, shift)
    
    def crack_cipher(
        self,
        ciphertext: CipherText,
        analyzer: FrequencyAnalyzerPort,
        top_n: int = 5
    ) -> Result[Sequence[CrackResult], AnalysisError]:
        """
        Attempt to crack cipher by trying all possible shifts.
        
        Uses frequency analysis to rank candidates by likelihood.
        
        Args:
            ciphertext: Encrypted text to crack
            analyzer: Frequency analyzer for scoring
            top_n: Number of top candidates to return
            
        Returns:
            Result containing ranked crack attempts or error
            
        Examples:
            >>> service = CipherService(engine)
            >>> result = service.crack_cipher(
            ...     CipherText("KHOOR"),
            ...     analyzer,
            ...     top_n=3
            ... )
            >>> result.is_ok()
            True
            >>> results = result.unwrap()
            >>> results[0].plaintext
            PlainText("HELLO")
            
        Design Decision:
            We try all 26 shifts rather than using optimization because:
            1. 26 iterations is trivial computationally
            2. Simpler code is more maintainable
            3. We want to show all candidates to user anyway
            
        Edge Cases:
            - Empty ciphertext returns Err(AnalysisError)
            - top_n larger than 26 returns all 26 results
            - top_n <= 0 returns empty list
        """
        if not ciphertext:
            return Err(AnalysisError(
                message="Cannot crack empty ciphertext",
                context={"ciphertext": ciphertext, "operation": "crack"}
            ))
        
        if top_n <= 0:
            return Ok([])
        
        results: list[CrackResult] = []
        
        # Try all 26 possible shifts
        for shift_value in range(26):
            shift = Shift(value=shift_value)
            plaintext = self.decrypt_text(ciphertext, shift)
            score = analyzer.analyze(plaintext)
            
            results.append(CrackResult(
                shift=shift,
                plaintext=plaintext,
                score=score
            ))
        
        # Sort by score (lower is better)
        ranked = sorted(results, key=lambda r: r.score.value)
        
        # Return top N results
        return Ok(ranked[:min(top_n, len(ranked))])
