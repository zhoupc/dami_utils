import os
import os.path as osp


def get_parent_dir(path, level=1):
    """
    Get the parent directory of a given path.

    Args:
        path (str): The input file or directory path.
        level (int, optional): The number of directory levels to go up. Defaults to 1.

    Returns:
        str: The path of the parent directory.

    Example:
        If path is '/home/user/documents/file.txt' and level is 2,
        the function will return '/home/user'.
    """
    for _ in range(level):
        # Use os.path.dirname to get the parent directory
        path = osp.dirname(path)
    return path
