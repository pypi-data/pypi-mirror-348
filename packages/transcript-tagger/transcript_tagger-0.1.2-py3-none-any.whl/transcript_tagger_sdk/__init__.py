"""
Transcript Tagger - A toolkit for tagging and analyzing transcript content.
"""

__version__ = "0.1.1"

from .transcript_tagger import TranscriptTagger
from .difficulty_analyzer import DifficultyAnalyzer
from .config import Config

__all__ = ["TranscriptTagger", "DifficultyAnalyzer", "Config"] 