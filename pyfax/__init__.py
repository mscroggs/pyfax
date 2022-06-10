"""pyfax: a Python library for generating teletext tti files."""

from .version import version as __version__
from .page import Color, Page, Line
from . import pages
from ._config import config
