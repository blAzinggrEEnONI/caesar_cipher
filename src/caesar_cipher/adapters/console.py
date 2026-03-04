"""
Console output adapter using Rich for formatting.

Keeps all Rich dependencies isolated in this adapter.
"""

from typing import Sequence

from rich.console import Console
from rich.table import Table

from caesar_cipher.domain.errors import DomainError
from caesar_cipher.domain.values import CrackResult


class ConsoleOutput:
    """
    Handles formatted console output using Rich.
    
    Isolates Rich library dependencies to this adapter.
    
    Design Philosophy:
        - Single responsibility: console formatting
        - No business logic
        - Configurable console instance
        
    Examples:
        >>> console_out = ConsoleOutput()
        >>> console_out.print_success("Operation completed")
        >>> console_out.print_error("Something went wrong")
    """
    
    def __init__(self, console: Console | None = None):
        """
        Initialize console output adapter.
        
        Args:
            console: Rich Console instance (creates default if None)
        """
        self._console = console or Console()
    
    def print_success(self, message: str) -> None:
        """
        Print success message in green.
        
        Args:
            message: Success message to display
        """
        self._console.print(f"[green]{message}[/green]")
    
    def print_info(self, message: str) -> None:
        """
        Print info message in blue.
        
        Args:
            message: Info message to display
        """
        self._console.print(f"[blue]{message}[/blue]")
    
    def print_error(self, message: str) -> None:
        """
        Print error message in red.
        
        Args:
            message: Error message to display
        """
        self._console.print(f"[red]Error:[/red] {message}")
    
    def print_text(self, text: str) -> None:
        """
        Print plain text without formatting.
        
        Args:
            text: Text to display
        """
        self._console.print(text)
    
    def format_crack_results(
        self,
        results: Sequence[CrackResult],
        title: str = "Caesar Cipher Brute Force Results"
    ) -> None:
        """
        Display crack results in a formatted table.
        
        Args:
            results: Ranked crack results to display
            title: Table title
            
        Design Decision:
            Truncates long text to 80 characters for readability.
            Shows rank, shift, score, and decrypted text.
        """
        table = Table(title=title)
        table.add_column("Rank", style="cyan", justify="right")
        table.add_column("Shift", style="magenta", justify="right")
        table.add_column("Score", style="yellow", justify="right")
        table.add_column("Decrypted Text", style="green")
        
        for rank, result in enumerate(results, 1):
            # Truncate long text for display
            text_preview = result.plaintext[:80]
            if len(result.plaintext) > 80:
                text_preview += "..."
            
            table.add_row(
                str(rank),
                str(result.shift.value),
                f"{result.score.value:.2f}",
                text_preview
            )
        
        self._console.print(table)
        
        # Show best match
        if results:
            best = results[0]
            self._console.print(
                f"\n[bold]Best match (Shift {best.shift.value}):[/bold] {best.plaintext}"
            )
    
    def format_error(self, error: DomainError) -> None:
        """
        Display formatted error with context.
        
        Args:
            error: Domain error to display
            
        Design Decision:
            Shows error message prominently.
            Displays context as key-value pairs for debugging.
        """
        self.print_error(error.message)
        
        if error.context:
            self._console.print("\n[yellow]Context:[/yellow]")
            for key, value in error.context.items():
                self._console.print(f"  {key}: {value}")
