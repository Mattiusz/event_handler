"""Top-level package for event_handler."""
import os

from dotenv import load_dotenv

__author__ = """Mattiusz"""
__version__ = "0.1"

load_dotenv()


def get_package_root() -> str:
    """
    Returns path to the root folder of event_handler
    package.
    """
    return os.path.dirname(os.path.abspath(__file__))


PACKAGE_PATH = get_package_root()
PACKAGE_VERSION = __version__
