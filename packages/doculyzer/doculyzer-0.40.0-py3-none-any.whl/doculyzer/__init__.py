"""Automatically generated __init__.py"""
__all__ = ['Config', 'SearchHelper', 'SearchResult', 'config', 'crawl', 'crawler', 'ingest_documents', 'main', 'search',
           'search_with_content']

import os

from . import config
from . import crawler
from . import main
from . import search
from .config import Config
from .crawler import crawl
from .configure_logging import configure_logging
from .main import ingest_documents
from .search import SearchHelper
from .search import SearchResult
from .search import search_with_content
from .vendor import get_vendor_path
from .server import app

configure_logging()

__version__ = "0.40.0"


