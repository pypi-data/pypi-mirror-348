"""Module for renaming files and directories in the workspace."""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict

from .file_ops import FileOperation


@dataclass(unsafe_hash=True, slots=True)
class RenameOperation(FileOperation):
    """Class to rename a file or folder in the workspace."""

    name = "rename_file"

    def _rename_file_or_folder(self, path: str, new_name: str) -> None:
        """Rename a file or folder.

        Args:
            path: Path to the file or folder to rename
            new_name: New name for the file or folder (not a full path, just the name)

        Raises:
            FileNotFoundError: If the path does not exist
            FileExistsError: If a file or folder with the new name already exists

        """
        root_path = self._root_path
        abs_path = self._validate_path_in_root(root_path, path)

        # Check if source exists
        source_path = Path(abs_path)
        if not source_path.exists():
            raise FileNotFoundError(f"Path does not exist: {path}")

        # Get the parent directory and create the new path
        parent_dir = source_path.parent
        new_path = parent_dir / new_name

        # Check if destination exists
        if new_path.exists():
            raise FileExistsError(f"A file or folder with the name '{new_name}' already exists in the same directory")

        # Rename the file or folder
        os.rename(str(source_path), str(new_path))

    def __call__(self, path: str, new_name: str) -> Dict[str, Any]:
        """Rename a file or folder.

        Args:
            path: Path to the file or folder to rename
            new_name: New name for the file or folder (not a full path, just the name)

        Returns:
            A dictionary containing the status and paths of the renamed file or folder

        """
        try:
            self._rename_file_or_folder(path, new_name)
            return {
                "status": "success",
                "message": f"Successfully renamed {path} to {new_name}",
                "path": path,
                "new_name": new_name,
            }
        except Exception as e:
            return {
                "error": f"Error renaming file or folder: {str(e)}",
                "path": path,
                "new_name": new_name,
            }

    def self_warpper(self) -> Callable:
        """Return the self wrapper function.

        Returns:
            A callable function that wraps the __call__ method

        """

        def self_wrapper(path: str, new_name: str) -> Dict[str, Any]:
            """Rename a file or folder.

            Args:
                path: Path to the file or folder to rename
                new_name: New name for the file or folder (not a full path, just the name)

            Returns:
                A dictionary containing the status and paths of the renamed file or folder

            """
            return self.__call__(path, new_name)

        self_wrapper.__name__ = self.name

        return self_wrapper
