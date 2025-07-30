"""
Evaluation Kit Core Library.

This package contains core functionality for the Evaluation Kit,
including models, storage, and the main kit interface.
"""
from .models import SpanData, TaskData
from .storage import BaseStorage, MemoryStorage # Might not need to export BaseStorage
from .kit import EvalKit

__version__ = "0.2.0" # Bump version

__all__ = [
    'EvalKit',
    'SpanData',
    'TaskData',
    'MemoryStorage', # Exporting for potential direct use or type hinting
] 