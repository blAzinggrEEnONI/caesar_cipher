"""
CLI adapter using Typer for command-line interface.

Handles user interaction and delegates to domain services.
"""

from pathlib import Path
from typing import Annotated

import typer

from caesar_cipher.adapters.console import ConsoleOutput
from caesar_cipher.adapters.file_io import (
    ArgumentTextInput,
    FileTextInput,
    FileTextOutput,
    StdinTextInput,
)
from caesar_cipher.core.frequency_analyzer import EnglishFrequencyAnalyzer
from caesar_cipher.domain.services import CipherService
from caesar_cipher.domain.values import CipherText, PlainText, Shift


def _resolve_input(
    text: str | None,
    input_file: Path | None,
) -> ArgumentTextInput | FileTextInput | StdinTextInput:
    """Return the appropriate input adapter based on provided arguments."""
    if text is not None:
        return ArgumentTextInput(text)
    if input_file is not None:
        return FileTextInput(input_file)
    return StdinTextInput()


def create_cli_app(
    cipher_service: CipherService,
    console: ConsoleOutput
) -> typer.Typer:
    """
    Create CLI application with injected dependencies.
    
    Args:
        cipher_service: Domain service for cipher operations
        console: Console output adapter
        
    Returns:
        Configured Typer application
        
    Design Decision:
        Factory function allows dependency injection.
        Makes CLI testable by injecting mock dependencies.
    """
    app = typer.Typer(
        name="caesar-cipher",
        help="Caesar cipher encryption, decryption, and brute-force cracking tool",
        no_args_is_help=True,
    )
    
    @app.command()
    def encrypt(
        text: Annotated[
            str | None,
            typer.Argument(help="Text to encrypt (or use --input-file or stdin)"),
        ] = None,
        key: Annotated[
            int,
            typer.Option("--key", "-k", help="Shift key (0-25)")
        ] = 3,
        input_file: Annotated[
            Path | None,
            typer.Option("--input-file", "-i", help="Input file path")
        ] = None,
        output_file: Annotated[
            Path | None,
            typer.Option("--output-file", "-o", help="Output file path")
        ] = None,
        quiet: Annotated[
            bool,
            typer.Option("--quiet", "-q", help="Suppress output messages")
        ] = False,
    ) -> None:
        """Encrypt text using Caesar cipher with specified shift key."""
        # Create shift
        shift_result = Shift.create(key)
        if shift_result.is_err():
            console.print_error(f"Invalid key: {key}")
            raise typer.Exit(code=1)
        shift = shift_result.unwrap()
        
        # Read input
        text_result = _resolve_input(text, input_file).read_text()
        if text_result.is_err():
            console.format_error(text_result.error)
            raise typer.Exit(code=1)

        plaintext = PlainText(text_result.unwrap())
        
        # Encrypt
        ciphertext = cipher_service.encrypt_text(plaintext, shift)
        
        # Write output
        if output_file is not None:
            output_adapter = FileTextOutput(output_file)
            write_result = output_adapter.write_text(ciphertext)
            if write_result.is_err():
                console.format_error(write_result.error)
                raise typer.Exit(code=1)
            if not quiet:
                console.print_success(f"Encrypted text written to {output_file}")
        else:
            if not quiet:
                console.print_success(f"Encrypted: {ciphertext}")
            else:
                console.print_text(ciphertext)
    
    @app.command()
    def decrypt(
        text: Annotated[
            str | None,
            typer.Argument(help="Text to decrypt (or use --input-file or stdin)"),
        ] = None,
        key: Annotated[
            int,
            typer.Option("--key", "-k", help="Shift key (0-25)")
        ] = 3,
        input_file: Annotated[
            Path | None,
            typer.Option("--input-file", "-i", help="Input file path")
        ] = None,
        output_file: Annotated[
            Path | None,
            typer.Option("--output-file", "-o", help="Output file path")
        ] = None,
        quiet: Annotated[
            bool,
            typer.Option("--quiet", "-q", help="Suppress output messages")
        ] = False,
    ) -> None:
        """Decrypt text using Caesar cipher with specified shift key."""
        # Create shift
        shift_result = Shift.create(key)
        if shift_result.is_err():
            console.print_error(f"Invalid key: {key}")
            raise typer.Exit(code=1)
        shift = shift_result.unwrap()

        # Read input
        text_result = _resolve_input(text, input_file).read_text()
        if text_result.is_err():
            console.format_error(text_result.error)
            raise typer.Exit(code=1)

        ciphertext = CipherText(text_result.unwrap())

        # Decrypt
        plaintext = cipher_service.decrypt_text(ciphertext, shift)
        
        # Write output
        if output_file is not None:
            output_adapter = FileTextOutput(output_file)
            write_result = output_adapter.write_text(plaintext)
            if write_result.is_err():
                console.format_error(write_result.error)
                raise typer.Exit(code=1)
            if not quiet:
                console.print_success(f"Decrypted text written to {output_file}")
        else:
            if not quiet:
                console.print_info(f"Decrypted: {plaintext}")
            else:
                console.print_text(plaintext)
    
    @app.command()
    def crack(
        text: Annotated[
            str | None,
            typer.Argument(help="Text to crack (or use --input-file or stdin)"),
        ] = None,
        input_file: Annotated[
            Path | None,
            typer.Option("--input-file", "-i", help="Input file path")
        ] = None,
        top: Annotated[
            int,
            typer.Option("--top", "-t", help="Show top N candidates")
        ] = 5,
        show_all: Annotated[
            bool,
            typer.Option("--all", "-a", help="Show all 26 possible shifts")
        ] = False,
    ) -> None:
        """Brute-force decrypt text by trying all shifts with frequency analysis ranking."""
        # Read input
        text_result = _resolve_input(text, input_file).read_text()
        if text_result.is_err():
            console.format_error(text_result.error)
            raise typer.Exit(code=1)

        ciphertext = CipherText(text_result.unwrap())
        
        # Crack cipher
        analyzer = EnglishFrequencyAnalyzer()
        display_count = 26 if show_all else top
        
        crack_result = cipher_service.crack_cipher(
            ciphertext,
            analyzer,
            top_n=display_count
        )
        
        if crack_result.is_err():
            console.format_error(crack_result.error)
            raise typer.Exit(code=1)
        
        results = crack_result.unwrap()
        console.format_crack_results(results)
    
    return app
