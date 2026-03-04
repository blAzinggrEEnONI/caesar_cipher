"""
Performance tests for Caesar cipher operations.

Author: Tanatswa D. Muskwe (grimm)

These tests document expected performance characteristics.
They are not strict benchmarks but help identify regressions.
"""

import time

from caesar_cipher.core.cipher_engine import PureCipherEngine
from caesar_cipher.core.frequency_analyzer import EnglishFrequencyAnalyzer
from caesar_cipher.domain.services import CipherService
from caesar_cipher.domain.values import CipherText, PlainText, Shift


class TestCipherPerformance:
    """Test cipher operation performance."""
    
    def test_encrypt_1kb_text(self) -> None:
        """
        Test encryption performance with 1KB text.
        
        Expected: < 10ms for 1KB text
        Complexity: O(n) where n is text length
        """
        engine = PureCipherEngine()
        text = PlainText("A" * 1024)  # 1KB
        shift = Shift(3)
        
        start = time.perf_counter()
        result = engine.encrypt(text, shift)
        elapsed = time.perf_counter() - start
        
        assert len(result) == 1024
        assert elapsed < 0.01  # 10ms
        print(f"1KB encryption: {elapsed*1000:.2f}ms")
    
    def test_encrypt_10kb_text(self) -> None:
        """
        Test encryption performance with 10KB text.
        
        Expected: < 100ms for 10KB text
        Complexity: O(n) where n is text length
        """
        engine = PureCipherEngine()
        text = PlainText("A" * 10240)  # 10KB
        shift = Shift(3)
        
        start = time.perf_counter()
        result = engine.encrypt(text, shift)
        elapsed = time.perf_counter() - start
        
        assert len(result) == 10240
        assert elapsed < 0.1  # 100ms
        print(f"10KB encryption: {elapsed*1000:.2f}ms")
    
    def test_encrypt_100kb_text(self) -> None:
        """
        Test encryption performance with 100KB text.
        
        Expected: < 1s for 100KB text
        Complexity: O(n) where n is text length
        
        Performance Note:
            Using generator expressions for memory efficiency.
            join() is more efficient than string concatenation.
        """
        engine = PureCipherEngine()
        text = PlainText("A" * 102400)  # 100KB
        shift = Shift(3)
        
        start = time.perf_counter()
        result = engine.encrypt(text, shift)
        elapsed = time.perf_counter() - start
        
        assert len(result) == 102400
        assert elapsed < 1.0  # 1 second
        print(f"100KB encryption: {elapsed*1000:.2f}ms")


class TestFrequencyAnalysisPerformance:
    """Test frequency analysis performance."""
    
    def test_analyze_1kb_text(self) -> None:
        """
        Test frequency analysis with 1KB text.
        
        Expected: < 10ms for 1KB text
        Complexity: O(n) for counting + O(26) for chi-squared = O(n)
        
        Note: Chi-squared scores scale with text size.
        """
        analyzer = EnglishFrequencyAnalyzer()
        text = "THE QUICK BROWN FOX " * 50  # ~1KB
        
        start = time.perf_counter()
        score = analyzer.analyze(text)
        elapsed = time.perf_counter() - start
        
        assert score.value > 0  # Should produce a score
        assert elapsed < 0.01  # 10ms
        print(f"1KB analysis: {elapsed*1000:.2f}ms, score: {score.value:.2f}")
    
    def test_analyze_10kb_text(self) -> None:
        """
        Test frequency analysis with 10KB text.
        
        Expected: < 100ms for 10KB text
        """
        analyzer = EnglishFrequencyAnalyzer()
        text = "THE QUICK BROWN FOX " * 500  # ~10KB
        
        start = time.perf_counter()
        score = analyzer.analyze(text)
        elapsed = time.perf_counter() - start
        
        assert score.value > 0
        assert elapsed < 0.1  # 100ms
        print(f"10KB analysis: {elapsed*1000:.2f}ms, score: {score.value:.2f}")
    
    def test_analyze_100kb_text(self) -> None:
        """
        Test frequency analysis with 100KB text.
        
        Expected: < 1s for 100KB text
        
        Performance Note:
            Counter is implemented in C and very efficient.
            Chi-squared calculation is O(26) regardless of text size.
            Scores scale linearly with text size.
        """
        analyzer = EnglishFrequencyAnalyzer()
        text = "THE QUICK BROWN FOX " * 5000  # ~100KB
        
        start = time.perf_counter()
        score = analyzer.analyze(text)
        elapsed = time.perf_counter() - start
        
        assert score.value > 0
        assert elapsed < 1.0  # 1 second
        print(f"100KB analysis: {elapsed*1000:.2f}ms, score: {score.value:.2f}")


class TestCrackPerformance:
    """Test cipher cracking performance."""
    
    def test_crack_short_text(self) -> None:
        """
        Test cracking with short text (50 chars).
        
        Expected: < 50ms
        Complexity: O(26 * n) where n is text length
        
        Performance Note:
            Tries all 26 shifts, each requiring:
            - O(n) decryption
            - O(n) frequency analysis
            Total: O(26 * n) = O(n) since 26 is constant
        """
        engine = PureCipherEngine()
        service = CipherService(engine)
        analyzer = EnglishFrequencyAnalyzer()
        
        text = PlainText("THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG")
        encrypted = engine.encrypt(text, Shift(3))
        
        start = time.perf_counter()
        result = service.crack_cipher(encrypted, analyzer, top_n=5)
        elapsed = time.perf_counter() - start
        
        assert result.is_ok()
        assert elapsed < 0.05  # 50ms
        print(f"Crack short text: {elapsed*1000:.2f}ms")
    
    def test_crack_medium_text(self) -> None:
        """
        Test cracking with medium text (500 chars).
        
        Expected: < 200ms
        
        Design Decision:
            We don't parallelize because 26 iterations is trivial.
            Prefer simplicity over premature optimization.
        """
        engine = PureCipherEngine()
        service = CipherService(engine)
        analyzer = EnglishFrequencyAnalyzer()
        
        text = PlainText("THE QUICK BROWN FOX " * 25)  # ~500 chars
        encrypted = engine.encrypt(text, Shift(7))
        
        start = time.perf_counter()
        result = service.crack_cipher(encrypted, analyzer, top_n=5)
        elapsed = time.perf_counter() - start
        
        assert result.is_ok()
        assert elapsed < 0.2  # 200ms
        print(f"Crack medium text: {elapsed*1000:.2f}ms")
    
    def test_crack_long_text(self) -> None:
        """
        Test cracking with long text (5000 chars).
        
        Expected: < 2s
        
        Performance Note:
            If this becomes a bottleneck, could parallelize the 26 shifts.
            However, for typical use cases, this is fast enough.
        """
        engine = PureCipherEngine()
        service = CipherService(engine)
        analyzer = EnglishFrequencyAnalyzer()
        
        text = PlainText("THE QUICK BROWN FOX " * 250)  # ~5000 chars
        encrypted = engine.encrypt(text, Shift(13))
        
        start = time.perf_counter()
        result = service.crack_cipher(encrypted, analyzer, top_n=5)
        elapsed = time.perf_counter() - start
        
        assert result.is_ok()
        assert elapsed < 2.0  # 2 seconds
        print(f"Crack long text: {elapsed*1000:.2f}ms")


# Performance Summary:
# 
# Encryption/Decryption:
#   - 1KB:   < 10ms   (O(n) complexity)
#   - 10KB:  < 100ms
#   - 100KB: < 1s
#
# Frequency Analysis:
#   - 1KB:   < 10ms   (O(n) complexity)
#   - 10KB:  < 100ms
#   - 100KB: < 1s
#
# Cracking (26 shifts):
#   - 50 chars:   < 50ms   (O(26*n) = O(n))
#   - 500 chars:  < 200ms
#   - 5000 chars: < 2s
#
# Optimization Opportunities:
#   1. Parallelize crack_cipher (26 independent operations)
#   2. Use Cython for hot paths (shift_character)
#   3. Cache frequency analysis results
#
# Current Decision:
#   No optimization needed - performance is acceptable for typical use.
#   Prefer simplicity and readability over premature optimization.
