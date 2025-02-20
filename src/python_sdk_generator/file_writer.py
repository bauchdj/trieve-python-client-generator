import json
import re
from pathlib import Path
from typing import List, Optional

import click


class ConfigurableFileWriter:
    """A file writer that respects ignore patterns specified in a config file."""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the file writer with an optional config path.
        If no config path is provided, it will look for borea.config.json in the current directory.
        """
        self.config_path = (
            Path(config_path) if config_path else Path("borea.config.json")
        )
        self.ignore_patterns: List[str] = []
        self._load_config()
        self.compiled_patterns = [
            re.compile(pattern) for pattern in self.ignore_patterns
        ]

    def _load_config(self) -> None:
        """Load the configuration file and extract ignore patterns."""
        try:
            with open(self.config_path) as f:
                config = json.load(f)
                self.ignore_patterns = config.get("ignores", [])
        except FileNotFoundError:
            click.echo(
                f"Warning: Config file {self.config_path} not found. No ignore patterns will be applied."
            )
            self.ignore_patterns = []
        except json.JSONDecodeError:
            click.echo(f"Error: Config file {self.config_path} is not valid JSON.")
            raise

    def should_ignore(self, path: str) -> bool:
        """
        Check if a path should be ignored based on the ignore patterns.

        Args:
            path: The path to check against ignore patterns

        Returns:
            bool: True if the path should be ignored, False otherwise
        """
        path = str(Path(path))  # Normalize path separators
        return any(pattern.search(path) for pattern in self.compiled_patterns)

    def write(self, path: str, content: str, mode: str = "w") -> bool:
        """
        Write content to a file if it's not in the ignore list.

        Args:
            path: The path where to write the file
            content: The content to write
            mode: The file opening mode (default: "w")

        Returns:
            bool: True if file was written, False if ignored
        """
        if self.should_ignore(path):
            click.echo(f"Skipping ignored path: {path}")
            return False

        # Create parent directories if they don't exist and aren't ignored
        parent = Path(path).parent
        if not parent.exists():
            # Check each parent directory against ignore patterns
            parents_to_create = []
            current = parent
            while not current.exists():
                if self.should_ignore(str(current)):
                    click.echo(
                        f"Cannot create file: parent directory {current} is ignored"
                    )
                    return False
                parents_to_create.append(current)
                current = current.parent

            # Create parent directories
            for dir_path in reversed(parents_to_create):
                dir_path.mkdir(exist_ok=True)

        # Write the file
        with open(path, mode) as f:
            f.write(content)
        return True

    @classmethod
    def from_click_context(
        cls, config: Optional[str] = None
    ) -> "ConfigurableFileWriter":
        """
        Create a FileWriter instance from Click context.

        Args:
            config: Optional path to the config file

        Returns:
            ConfigurableFileWriter: A new instance of the file writer
        """
        return cls(config_path=config)
