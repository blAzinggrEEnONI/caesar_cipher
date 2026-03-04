"""
Port interfaces (Protocols) for dependency inversion.

These define contracts that adapters must implement, allowing
the domain core to remain independent of infrastructure details.
"""

from typing import Protocol

from caesar_cipher.core.result import Result
from caesar_cipher.domain.errors import FileIOError
from caesar_cipher.domain.values import (
    CipherText,
    FrequencyScore,
    PlainText,
    Shift,
)


class TextInputPort(Protocol):
    """
    Port for reading text input from various sources.
    
    Implementations might read from:
        - Command line arguments
        - Files
        - Standard input
        - Network sources
        - Databases
        
    Design Decision:
        Returns Result type to make I/O failures explicit.
        Allows callers to handle errors without exceptions.
        
    Examples:
        >>> class FileInput:
        ...     def read_text(self) -> Result[str, FileIOError]:
        ...         try:
        ...             with open("file.txt") as f:
        ...                 return Ok(f.read())
        ...         except FileNotFoundError:
        ...             return Err(FileIOError("File not found", {}))
    """
    def read_text(self) -> Result[str, FileIOError]:
        """
        Read text from the input source.
        
        Returns:
            Ok(str) with text content, or Err(FileIOError) on failure
        """
        ...


class TextOutputPort(Protocol):
    """
    Port for writing text output to various destinations.
    
    Implementations might write to:
        - Console (with formatting)
        - Files
        - Standard output
        - Network destinations
        - Databases
        
    Design Decision:
        Returns Result[None, FileIOError] to signal success/failure.
        None indicates successful write with no return value.
        
    Examples:
        >>> class FileOutput:
        ...     def write_text(self, text: str) -> Result[None, FileIOError]:
        ...         try:
        ...             with open("out.txt", "w") as f:
        ...                 f.write(text)
        ...             return Ok(None)
        ...         except PermissionError:
        ...             return Err(FileIOError("Permission denied", {}))
    """
    def write_text(self, text: str) -> Result[None, FileIOError]:
        """
        Write text to the output destination.
        
        Args:
            text: Text content to write
            
        Returns:
            Ok(None) on success, or Err(FileIOError) on failure
        """
        ...


class CipherEnginePort(Protocol):
    """
    Port for cipher encryption/decryption operations.
    
    Implementations must be pure (no side effects).
    
    Design Decision:
        Does not return Result because cipher operations on valid
        inputs cannot fail. Type system ensures inputs are valid.
        
    Examples:
        >>> class SimpleCipher:
        ...     def encrypt(self, plaintext: PlainText, shift: Shift) -> CipherText:
        ...         # Pure transformation
        ...         return CipherText(plaintext.upper())
        ...     def decrypt(self, ciphertext: CipherText, shift: Shift) -> PlainText:
        ...         return PlainText(ciphertext.lower())
    """
    def encrypt(self, plaintext: PlainText, shift: Shift) -> CipherText:
        """
        Encrypt plaintext with given shift.
        
        Args:
            plaintext: Text to encrypt
            shift: Shift amount
            
        Returns:
            Encrypted ciphertext
        """
        ...
    
    def decrypt(self, ciphertext: CipherText, shift: Shift) -> PlainText:
        """
        Decrypt ciphertext with given shift.
        
        Args:
            ciphertext: Text to decrypt
            shift: Shift amount
            
        Returns:
            Decrypted plaintext
        """
        ...


class FrequencyAnalyzerPort(Protocol):
    """
    Port for analyzing text frequency patterns.
    
    Used for breaking ciphers without knowing the key.
    
    Design Decision:
        Returns FrequencyScore (not Result) because analysis
        always succeeds, even on empty text (returns infinity).
        
    Examples:
        >>> class SimpleAnalyzer:
        ...     def analyze(self, text: str) -> FrequencyScore:
        ...         # Count vowels as simple heuristic
        ...         vowels = sum(1 for c in text if c.lower() in 'aeiou')
        ...         return FrequencyScore(value=100.0 - vowels)
    """
    def analyze(self, text: str) -> FrequencyScore:
        """
        Calculate frequency score for text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Score indicating match to expected pattern (lower is better)
        """
        ...
