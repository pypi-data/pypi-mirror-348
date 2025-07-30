"""
Package: infrastructure

This package provides various components for processing audio, including:
- Speech-to-text transcription with Whisper and Faster Whisper.
- Speaker separation using PyAnnote's diarization pipeline.

Classes
-------
WhisperProcessor:
    Provides transcription using OpenAI's Whisper model.
FasterWhisperProcessor:
    Offers fast transcription via the Faster Whisper library.
VoiceSeparator:
    Implements speaker separation using PyAnnote.
"""

from .natasha_stopwords_remover import *
from .transcriber import *

__all__ = ['Transcriber', 'NatashaStopwordsRemover']
