"""pyfax: a Python library for generating teletext tti files."""

from . import pages
from ._config import config
from .page import Color, Line, Page
from .version import version as __version__
