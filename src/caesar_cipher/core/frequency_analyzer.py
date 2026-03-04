"""
Frequency analysis for breaking Caesar cipher.

Uses chi-squared statistical testing to compare letter frequencies.
All functions are pure with no side effects.
"""

from collections import Counter

from caesar_cipher.domain.values import FrequencyScore

# English letter frequency distribution (%)
# Source: Analysis of Oxford English Dictionary
# These are empirically determined from large English text corpora
ENGLISH_FREQUENCIES = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97,
    'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25,
    'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36,
    'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29,
    'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10,
    'Z': 0.07
}


def calculate_chi_squared(
    observed: dict[str, int],
    expected: dict[str, float],
    total: int
) -> float:
    """
    Calculate chi-squared statistic.
    
    Pure function for statistical analysis.
    
    Formula:
        χ² = Σ((observed - expected)² / expected)
        
    Args:
        observed: Actual letter counts
        expected: Expected frequency percentages
        total: Total number of letters
        
    Returns:
        Chi-squared value (lower = better match)
        
    Mathematical Properties:
        - Always non-negative
        - 0 means perfect match
        - Higher values mean worse match
        
    Examples:
        >>> observed = {'E': 13, 'T': 9, 'A': 8}
        >>> expected = {'E': 12.7, 'T': 9.06, 'A': 8.17}
        >>> chi_sq = calculate_chi_squared(observed, expected, 100)
        >>> chi_sq < 10  # Good match
        True
        
    Performance:
        O(n) where n is alphabet size (26 for English)
        
    Design Decision:
        Separated from class to make it testable in isolation.
        Pure function with no dependencies on instance state.
    """
    chi_squared = 0.0
    
    for letter, expected_pct in expected.items():
        observed_count = observed.get(letter, 0)
        expected_count = (expected_pct / 100.0) * total
        
        if expected_count > 0:
            diff = observed_count - expected_count
            chi_squared += (diff * diff) / expected_count
    
    return chi_squared


class EnglishFrequencyAnalyzer:
    """
    Analyzes text for English language patterns.
    
    Uses chi-squared test to compare letter frequencies against
    expected English distribution.
    
    Design Philosophy:
        - Pure analysis (no side effects)
        - Configurable reference frequencies
        - Returns domain value objects
        
    Examples:
        >>> analyzer = EnglishFrequencyAnalyzer()
        >>> score = analyzer.analyze("HELLO WORLD")
        >>> score.value < 100  # English text scores well
        True
        >>> random_score = analyzer.analyze("XQZPK VWMJL")
        >>> random_score.value > 200  # Random text scores poorly
        True
    """
    
    def __init__(self, reference_frequencies: dict[str, float] | None = None):
        """
        Initialize analyzer with reference frequencies.
        
        Args:
            reference_frequencies: Expected letter frequencies (defaults to English)
            
        Design Decision:
            Allows custom frequency tables for other languages or domains.
            Defaults to English for convenience.
        """
        self._reference = reference_frequencies or ENGLISH_FREQUENCIES
    
    def analyze(self, text: str) -> FrequencyScore:
        """
        Calculate frequency score for text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Score indicating match to English (lower is better)
            
        Edge Cases:
            - Empty text returns infinity (worst possible score)
            - Non-alphabetic characters are ignored
            - Case-insensitive analysis
            
        Examples:
            >>> analyzer = EnglishFrequencyAnalyzer()
            >>> analyzer.analyze("The quick brown fox")
            FrequencyScore(value=...)  # Low score (good match)
            >>> analyzer.analyze("")
            FrequencyScore(value=inf)  # Infinity (no data)
            
        Performance:
            O(n) where n is text length
            - O(n) to extract and count letters
            - O(26) for chi-squared calculation
        """
        # Extract and count only letters (case-insensitive)
        letters = [c.upper() for c in text if c.isalpha()]
        
        if not letters:
            return FrequencyScore(value=float('inf'))
        
        counts = Counter(letters)
        total = len(letters)
        
        score = calculate_chi_squared(
            observed=dict(counts),
            expected=self._reference,
            total=total
        )
        
        return FrequencyScore(value=score)
