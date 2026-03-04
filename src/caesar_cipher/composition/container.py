"""
Composition root - the single place where all dependencies are wired together.

This is the only place in the application that knows about concrete implementations.
Everything else depends on abstractions (Protocols).
"""

import typer

from caesar_cipher.adapters.cli import create_cli_app
from caesar_cipher.adapters.console import ConsoleOutput
from caesar_cipher.core.cipher_engine import PureCipherEngine
from caesar_cipher.domain.services import CipherService


def compose_application() -> typer.Typer:
    """
    Compose the application by wiring all dependencies.
    
    This is the composition root - the single place where we:
    1. Create concrete implementations
    2. Wire dependencies together
    3. Return the fully configured application
    
    Returns:
        Configured Typer CLI application
        
    Design Philosophy:
        - Single Responsibility: Only dependency wiring
        - Dependency Inversion: Depends on abstractions, creates concretions
        - Explicit Dependencies: All dependencies visible in one place
        - Testability: Easy to create test composition with mocks
        
    Design Decision:
        Using manual dependency injection (not a DI framework) because:
        1. Application is small enough to wire manually
        2. Explicit is better than implicit (no magic)
        3. No additional dependencies required
        4. Easy to understand and debug
        
    Examples:
        >>> app = compose_application()
        >>> # app is ready to run with all dependencies wired
        
    Extension Points:
        To swap implementations:
        1. Create new implementation of port interface
        2. Change instantiation here
        3. No other code changes needed
        
        Example - swap cipher engine:
        ```python
        # engine = PureCipherEngine()  # Old
        engine = OptimizedCipherEngine()  # New
        ```
    """
    # Create core implementations (pure, no dependencies)
    cipher_engine = PureCipherEngine()
    
    # Create domain services (inject core implementations)
    cipher_service = CipherService(engine=cipher_engine)
    
    # Create adapters (for I/O and presentation)
    console = ConsoleOutput()
    
    # Create CLI application (inject service and adapters)
    app = create_cli_app(
        cipher_service=cipher_service,
        console=console
    )
    
    return app


def compose_test_application(
    cipher_engine: PureCipherEngine | None = None,
    console: ConsoleOutput | None = None,
) -> typer.Typer:
    """
    Compose application for testing with injectable mocks.
    
    Args:
        cipher_engine: Mock cipher engine (uses real if None)
        console: Mock console (uses real if None)
        
    Returns:
        Configured Typer CLI application for testing
        
    Design Decision:
        Separate test composition makes testing easier.
        Allows injecting mocks without changing production code.
        
    Examples:
        >>> mock_engine = MockCipherEngine()
        >>> mock_console = MockConsole()
        >>> app = compose_test_application(
        ...     cipher_engine=mock_engine,
        ...     console=mock_console
        ... )
    """
    # Use provided mocks or create real implementations
    engine = cipher_engine or PureCipherEngine()
    console_out = console or ConsoleOutput()
    
    # Wire dependencies
    cipher_service = CipherService(engine=engine)
    app = create_cli_app(
        cipher_service=cipher_service,
        console=console_out
    )
    
    return app
