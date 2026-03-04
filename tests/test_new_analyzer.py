"""Tests for new frequency analyzer."""

from caesar_cipher.core.frequency_analyzer import (
    EnglishFrequencyAnalyzer,
    calculate_chi_squared,
)
from caesar_cipher.domain.values import FrequencyScore


class TestCalculateChiSquared:
    """Test the pure calculate_chi_squared function."""
    
    def test_perfect_match_returns_zero(self) -> None:
        # If observed matches expected exactly, chi-squared should be very low
        observed = {'E': 13, 'T': 9, 'A': 8}
        expected = {'E': 12.7, 'T': 9.06, 'A': 8.17}
        total = 100
        
        result = calculate_chi_squared(observed, expected, total)
        assert result < 1.0  # Very close to expected
    
    def test_poor_match_returns_high_value(self) -> None:
        # If observed is very different from expected, chi-squared should be high
        observed = {'Z': 50, 'Q': 30, 'X': 20}
        expected = {'E': 12.7, 'T': 9.06, 'A': 8.17}
        total = 100
        
        result = calculate_chi_squared(observed, expected, total)
        assert result > 20.0  # Still significantly higher than good match


class TestEnglishFrequencyAnalyzer:
    """Test the EnglishFrequencyAnalyzer class."""
    
    def test_analyze_english_text(self) -> None:
        analyzer = EnglishFrequencyAnalyzer()
        score = analyzer.analyze("THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG")
        
        assert isinstance(score, FrequencyScore)
        assert score.value < 150  # English text should score well
    
    def test_analyze_gibberish(self) -> None:
        analyzer = EnglishFrequencyAnalyzer()
        score = analyzer.analyze("ZZZZZ QQQQQ XXXXX")
        
        assert isinstance(score, FrequencyScore)
        assert score.value > 100  # Gibberish should score poorly
    
    def test_analyze_empty_string(self) -> None:
        analyzer = EnglishFrequencyAnalyzer()
        score = analyzer.analyze("")
        
        assert score.value == float('inf')
    
    def test_analyze_case_insensitive(self) -> None:
        analyzer = EnglishFrequencyAnalyzer()
        score_upper = analyzer.analyze("HELLO WORLD")
        score_lower = analyzer.analyze("hello world")
        
        # Should produce same score regardless of case
        assert score_upper.value == score_lower.value
    
    def test_analyze_ignores_non_letters(self) -> None:
        analyzer = EnglishFrequencyAnalyzer()
        score1 = analyzer.analyze("HELLO")
        score2 = analyzer.analyze("H!E@L#L$O%")
        
        # Should produce same score (non-letters ignored)
        assert score1.value == score2.value


class TestFrequencyScore:
    """Test the FrequencyScore value object."""
    
    def test_is_better_than(self) -> None:
        score1 = FrequencyScore(value=10.5)
        score2 = FrequencyScore(value=20.3)
        
        assert score1.is_better_than(score2)
        assert not score2.is_better_than(score1)
    
    def test_is_better_than_equal(self) -> None:
        score1 = FrequencyScore(value=15.0)
        score2 = FrequencyScore(value=15.0)
        
        assert not score1.is_better_than(score2)
        assert not score2.is_better_than(score1)
