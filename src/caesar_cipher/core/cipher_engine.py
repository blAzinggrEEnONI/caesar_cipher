"""
Pure cipher engine with no side effects.

All functions are deterministic - same inputs always produce same outputs.
No I/O, no mutable state, no external dependencies.
"""

from caesar_cipher.domain.values import CipherText, PlainText, Shift

# Constants
ALPHABET_SIZE = 26
UPPERCASE_START = ord('A')
LOWERCASE_START = ord('a')


def shift_character(char: str, shift: Shift) -> str:
    """
    Shift a single character by the given amount.
    
    This is a pure function - no side effects, deterministic.
    
    Args:
        char: Single character to shift
        shift: Amount to shift by
        
    Returns:
        Shifted character (or original if not a letter)
        
    Invariants:
        - Non-letter characters are unchanged
        - Case is preserved
        - Wraps around alphabet (Z+1 = A)
        
    Examples:
        >>> shift_character('A', Shift(3))
        'D'
        >>> shift_character('Z', Shift(1))
        'A'
        >>> shift_character('a', Shift(3))
        'd'
        >>> shift_character('!', Shift(3))
        '!'
        >>> shift_character('Y', Shift(5))
        'D'
        
    Performance:
        O(1) - constant time operation
        
    Design Decision:
        Using ord() and chr() for efficiency over string indexing.
        Handles uppercase and lowercase separately to preserve case.
    """
    if not char.isalpha():
        return char
    
    base = UPPERCASE_START if char.isupper() else LOWERCASE_START
    offset = ord(char) - base
    shifted = (offset + shift.value) % ALPHABET_SIZE
    
    return chr(base + shifted)


def transform_text(text: str, shift: Shift) -> str:
    """
    Apply shift transformation to entire text.
    
    Pure function that transforms text character by character.
    
    Args:
        text: Text to transform
        shift: Shift to apply
        
    Returns:
        Transformed text
        
    Examples:
        >>> transform_text("HELLO", Shift(3))
        'KHOOR'
        >>> transform_text("Hello World!", Shift(3))
        'Khoor Zruog!'
        
    Design Decision:
        Using generator expression for memory efficiency with large texts.
        The join() is more efficient than string concatenation in a loop.
        
    Performance:
        O(n) where n is text length
        Memory: O(n) for result string
    """
    return ''.join(shift_character(char, shift) for char in text)


class PureCipherEngine:
    """
    Pure implementation of Caesar cipher.
    
    This class has no mutable state and all methods are pure functions.
    It implements the CipherEnginePort interface (defined later).
    
    Design Philosophy:
        - No side effects
        - No I/O operations
        - No mutable state
        - Deterministic behavior
        - Easy to test and reason about
    
    Examples:
        >>> engine = PureCipherEngine()
        >>> plaintext = PlainText("HELLO")
        >>> shift = Shift(3)
        >>> ciphertext = engine.encrypt(plaintext, shift)
        >>> ciphertext
        CipherText('KHOOR')
        >>> engine.decrypt(ciphertext, shift)
        PlainText('HELLO')
    """
    
    def encrypt(self, plaintext: PlainText, shift: Shift) -> CipherText:
        """
        Encrypt plaintext by shifting forward.
        
        Args:
            plaintext: Text to encrypt
            shift: Number of positions to shift
            
        Returns:
            Encrypted ciphertext
            
        Mathematical Property:
            decrypt(encrypt(text, s), s) = text (round-trip)
        """
        result = transform_text(plaintext, shift)
        return CipherText(result)
    
    def decrypt(self, ciphertext: CipherText, shift: Shift) -> PlainText:
        """
        Decrypt ciphertext by shifting backward.
        
        Args:
            ciphertext: Text to decrypt
            shift: Number of positions to shift back
            
        Returns:
            Decrypted plaintext
            
        Design Decision:
            Uses inverse shift rather than negative shift for clarity.
            Makes the mathematical relationship explicit.
        """
        inverse_shift = shift.inverse()
        result = transform_text(ciphertext, inverse_shift)
        return PlainText(result)
