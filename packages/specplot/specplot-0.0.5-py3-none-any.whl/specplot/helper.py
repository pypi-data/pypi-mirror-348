from os.path import join, dirname, realpath
import sys


def get_current_dir_path():
    """Return the current script directory

    Returns:
        str: path of the current script directory
    """
    return dirname(realpath(sys.argv[0]))


def get_child_dir_path(child, current=None):
    """Return specified child path of current script or supplied directory

    Args:
        child (str): child folder name
        current (str, optional): current folder path if it is None the current script directory is used. Defaults to None.

    Returns:
        str: path of the child directory
    """
    if current is None:
        current = get_current_dir_path()
    return join(current, child)
