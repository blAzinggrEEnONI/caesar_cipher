"""Tests for new pure cipher engine."""

import pytest

from caesar_cipher.core.cipher_engine import PureCipherEngine, shift_character, transform_text
from caesar_cipher.domain.values import CipherText, PlainText, Shift


class TestShiftCharacter:
    """Test the pure shift_character function."""
    
    def test_shift_uppercase_letter(self) -> None:
        assert shift_character('A', Shift(3)) == 'D'
        assert shift_character('X', Shift(3)) == 'A'
    
    def test_shift_lowercase_letter(self) -> None:
        assert shift_character('a', Shift(3)) == 'd'
        assert shift_character('x', Shift(3)) == 'a'
    
    def test_preserves_non_letters(self) -> None:
        assert shift_character('!', Shift(3)) == '!'
        assert shift_character(' ', Shift(5)) == ' '
        assert shift_character('1', Shift(10)) == '1'
    
    def test_wraparound(self) -> None:
        assert shift_character('Z', Shift(1)) == 'A'
        assert shift_character('z', Shift(1)) == 'a'


class TestTransformText:
    """Test the pure transform_text function."""
    
    def test_transform_simple_text(self) -> None:
        assert transform_text("HELLO", Shift(3)) == "KHOOR"
    
    def test_transform_mixed_case(self) -> None:
        assert transform_text("Hello World", Shift(3)) == "Khoor Zruog"
    
    def test_transform_with_punctuation(self) -> None:
        assert transform_text("Hello, World!", Shift(3)) == "Khoor, Zruog!"
    
    def test_transform_empty_string(self) -> None:
        assert transform_text("", Shift(5)) == ""


class TestPureCipherEngine:
    """Test the PureCipherEngine class."""
    
    def test_encrypt_basic(self) -> None:
        engine = PureCipherEngine()
        plaintext = PlainText("HELLO")
        ciphertext = engine.encrypt(plaintext, Shift(3))
        assert ciphertext == CipherText("KHOOR")
    
    def test_decrypt_basic(self) -> None:
        engine = PureCipherEngine()
        ciphertext = CipherText("KHOOR")
        plaintext = engine.decrypt(ciphertext, Shift(3))
        assert plaintext == PlainText("HELLO")
    
    def test_round_trip(self) -> None:
        engine = PureCipherEngine()
        original = PlainText("The Quick Brown Fox!")
        shift = Shift(13)
        
        encrypted = engine.encrypt(original, shift)
        decrypted = engine.decrypt(encrypted, shift)
        
        assert decrypted == original
    
    def test_zero_shift(self) -> None:
        engine = PureCipherEngine()
        plaintext = PlainText("HELLO")
        ciphertext = engine.encrypt(plaintext, Shift(0))
        assert ciphertext == CipherText("HELLO")
    
    def test_preserves_case(self) -> None:
        engine = PureCipherEngine()
        plaintext = PlainText("HeLLo WoRLd")
        ciphertext = engine.encrypt(plaintext, Shift(3))
        assert ciphertext == CipherText("KhOOr ZrUOg")


class TestShiftValueObject:
    """Test the Shift value object."""
    
    def test_create_valid_shift(self) -> None:
        result = Shift.create(3)
        assert result.is_ok()
        assert result.unwrap().value == 3
    
    def test_create_normalizes_large_value(self) -> None:
        result = Shift.create(27)
        assert result.is_ok()
        assert result.unwrap().value == 1
    
    def test_create_normalizes_negative_value(self) -> None:
        result = Shift.create(-5)
        assert result.is_ok()
        assert result.unwrap().value == 21
    
    def test_inverse(self) -> None:
        shift = Shift(3)
        inverse = shift.inverse()
        assert inverse.value == 23
    
    def test_inverse_of_zero(self) -> None:
        shift = Shift(0)
        inverse = shift.inverse()
        assert inverse.value == 0
    
    def test_shift_plus_inverse_is_zero(self) -> None:
        shift = Shift(7)
        inverse = shift.inverse()
        assert (shift.value + inverse.value) % 26 == 0
