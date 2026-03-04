"""
File I/O adapters implementing TextInputPort and TextOutputPort.

Handles all file system interactions with proper error handling.
"""

import sys
from pathlib import Path

from caesar_cipher.core.result import Err, Ok, Result
from caesar_cipher.domain.errors import FileIOError


class FileTextInput:
    """
    Reads text from files.
    
    Implements TextInputPort for file-based input.
    
    Examples:
        >>> input_adapter = FileTextInput(Path("message.txt"))
        >>> result = input_adapter.read_text()
        >>> if result.is_ok():
        ...     text = result.unwrap()
    """
    
    def __init__(self, path: Path):
        """
        Initialize file input adapter.
        
        Args:
            path: Path to file to read
        """
        self._path = path
    
    def read_text(self) -> Result[str, FileIOError]:
        """
        Read text from file.
        
        Returns:
            Ok(str) with file contents, or Err(IOError) on failure
            
        Error Cases:
            - File not found
            - Permission denied
            - Invalid encoding
            - I/O errors
        """
        try:
            content = self._path.read_text(encoding='utf-8')
            return Ok(content)
        except FileNotFoundError:
            return Err(FileIOError(
                message=f"File not found: {self._path}",
                context={
                    "path": str(self._path),
                    "operation": "read",
                    "error_type": "FileNotFoundError"
                }
            ))
        except PermissionError:
            return Err(FileIOError(
                message=f"Permission denied: {self._path}",
                context={
                    "path": str(self._path),
                    "operation": "read",
                    "error_type": "PermissionError"
                }
            ))
        except UnicodeDecodeError as e:
            return Err(FileIOError(
                message=f"Invalid encoding in file: {self._path}",
                context={
                    "path": str(self._path),
                    "operation": "read",
                    "error_type": "UnicodeDecodeError",
                    "encoding": "utf-8",
                    "details": str(e)
                }
            ))
        except OSError as e:
            return Err(FileIOError(
                message=f"I/O error reading file: {self._path}",
                context={
                    "path": str(self._path),
                    "operation": "read",
                    "error_type": "OSError",
                    "details": str(e)
                }
            ))


class FileTextOutput:
    """
    Writes text to files.
    
    Implements TextOutputPort for file-based output.
    
    Examples:
        >>> output_adapter = FileTextOutput(Path("output.txt"))
        >>> result = output_adapter.write_text("Hello, World!")
        >>> if result.is_ok():
        ...     print("Write successful")
    """
    
    def __init__(self, path: Path):
        """
        Initialize file output adapter.
        
        Args:
            path: Path to file to write
        """
        self._path = path
    
    def write_text(self, text: str) -> Result[None, FileIOError]:
        """
        Write text to file.
        
        Args:
            text: Text content to write
            
        Returns:
            Ok(None) on success, or Err(IOError) on failure
            
        Error Cases:
            - Permission denied
            - Disk full
            - Invalid path
            - I/O errors
            
        Design Decision:
            Creates parent directories if they don't exist.
            Overwrites existing files.
        """
        try:
            # Create parent directories if needed
            self._path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file
            self._path.write_text(text, encoding='utf-8')
            return Ok(None)
        except PermissionError:
            return Err(FileIOError(
                message=f"Permission denied: {self._path}",
                context={
                    "path": str(self._path),
                    "operation": "write",
                    "error_type": "PermissionError"
                }
            ))
        except OSError as e:
            return Err(FileIOError(
                message=f"I/O error writing file: {self._path}",
                context={
                    "path": str(self._path),
                    "operation": "write",
                    "error_type": "OSError",
                    "details": str(e)
                }
            ))


class StdinTextInput:
    """
    Reads text from standard input.
    
    Implements TextInputPort for stdin-based input.
    
    Examples:
        >>> input_adapter = StdinTextInput()
        >>> result = input_adapter.read_text()
        >>> if result.is_ok():
        ...     text = result.unwrap()
    """
    
    def read_text(self) -> Result[str, FileIOError]:
        """
        Read text from stdin.
        
        Returns:
            Ok(str) with stdin contents, or Err(IOError) on failure
            
        Design Decision:
            Reads all available input until EOF.
            Strips trailing whitespace for convenience.
        """
        try:
            content = sys.stdin.read().strip()
            return Ok(content)
        except OSError as e:
            return Err(FileIOError(
                message="Error reading from stdin",
                context={
                    "operation": "read",
                    "source": "stdin",
                    "error_type": "OSError",
                    "details": str(e)
                }
            ))


class ArgumentTextInput:
    """
    Provides text from command-line argument.
    
    Implements TextInputPort for argument-based input.
    
    Examples:
        >>> input_adapter = ArgumentTextInput("HELLO WORLD")
        >>> result = input_adapter.read_text()
        >>> result.unwrap()
        'HELLO WORLD'
    """
    
    def __init__(self, text: str):
        """
        Initialize argument input adapter.
        
        Args:
            text: Text from command-line argument
        """
        self._text = text
    
    def read_text(self) -> Result[str, FileIOError]:
        """
        Return the provided text.
        
        Returns:
            Ok(str) with the text (always succeeds)
            
        Design Decision:
            Always returns Ok since text is already in memory.
            No I/O can fail here.
        """
        return Ok(self._text)
