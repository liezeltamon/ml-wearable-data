from pathlib import Path

def find_project_dir(current_path: Path, marker: str = ".git") -> Path:
    """
    Find the project directory by looking for a marker file or directory.

    Args:
        current_path (Path): Path object for the starting directory.
        marker (str, optional): The name of the file or directory that indicates the project root.
            Defaults to ".git".

    Returns:
        Path: Path object for the project directory.

    Raises:
        FileNotFoundError: If the project root directory with the specified marker is not found.

    Examples:
        >>> find_project_dir(Path("/Users/ltamon/git/ml-wearable-data/utils"))
        Path('/Users/ltamon/git/ml-wearable-data')
    """
    
    for parent in current_path.parents:
        if (parent / marker).exists():
            return parent
    raise FileNotFoundError(f'Project dir with marker "{marker}" not found.')
