"""Tests for domain services."""

from caesar_cipher.core.cipher_engine import PureCipherEngine
from caesar_cipher.core.frequency_analyzer import EnglishFrequencyAnalyzer
from caesar_cipher.domain.services import CipherService
from caesar_cipher.domain.values import CipherText, PlainText, Shift


class TestCipherService:
    """Test the CipherService domain service."""
    
    def test_encrypt_text(self) -> None:
        engine = PureCipherEngine()
        service = CipherService(engine)
        
        plaintext = PlainText("HELLO")
        shift = Shift(3)
        ciphertext = service.encrypt_text(plaintext, shift)
        
        assert ciphertext == CipherText("KHOOR")
    
    def test_decrypt_text(self) -> None:
        engine = PureCipherEngine()
        service = CipherService(engine)
        
        ciphertext = CipherText("KHOOR")
        shift = Shift(3)
        plaintext = service.decrypt_text(ciphertext, shift)
        
        assert plaintext == PlainText("HELLO")
    
    def test_crack_cipher_success(self) -> None:
        engine = PureCipherEngine()
        service = CipherService(engine)
        analyzer = EnglishFrequencyAnalyzer()
        
        # Encrypt a longer text for better frequency analysis
        original = PlainText("THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG")
        encrypted = engine.encrypt(original, Shift(3))
        
        result = service.crack_cipher(encrypted, analyzer, top_n=5)
        
        assert result.is_ok()
        results = result.unwrap()
        assert len(results) == 5
        
        # Results should be ordered by score (best first)
        for i in range(len(results) - 1):
            assert results[i].score.value <= results[i + 1].score.value
    
    def test_crack_cipher_empty_text(self) -> None:
        engine = PureCipherEngine()
        service = CipherService(engine)
        analyzer = EnglishFrequencyAnalyzer()
        
        result = service.crack_cipher(CipherText(""), analyzer, top_n=5)
        
        assert result.is_err()
        error = result.error
        assert "empty" in error.message.lower()
    
    def test_crack_cipher_top_n_zero(self) -> None:
        engine = PureCipherEngine()
        service = CipherService(engine)
        analyzer = EnglishFrequencyAnalyzer()
        
        result = service.crack_cipher(CipherText("HELLO"), analyzer, top_n=0)
        
        assert result.is_ok()
        results = result.unwrap()
        assert len(results) == 0
    
    def test_crack_cipher_top_n_exceeds_26(self) -> None:
        engine = PureCipherEngine()
        service = CipherService(engine)
        analyzer = EnglishFrequencyAnalyzer()
        
        result = service.crack_cipher(CipherText("HELLO"), analyzer, top_n=100)
        
        assert result.is_ok()
        results = result.unwrap()
        assert len(results) == 26  # Maximum possible shifts
