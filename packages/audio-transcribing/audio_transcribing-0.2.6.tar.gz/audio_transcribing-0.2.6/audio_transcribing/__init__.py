"""
Package: audio_transcribing

This package provides classes for transcribing and processing audio content.
It supports speaker diarization, stopword removal, and transcription using
different infrastructure.

Classes
-------
NatashaStopwordsRemover:
    Handles text processing and stopword removal.
Transcriber :
    Class for performing audio transcription and processing tasks.
"""

from .infrastructure.natasha_stopwords_remover import *
from .infrastructure.transcriber import *

__all__ = ["Transcriber", "NatashaStopwordsRemover"]
