"""
Package: interfaces
-------------------

This package provides abstract interfaces and base implementations for various
audio processing operations, including transcription, speaker separation, and
stopword removal.

Classes
-------
IAudioProcessing:
    Interface for common audio processing operations.
ITranscribeProcessor:
    Interface for audio-to-text transcription.
IVoiceSeparator:
    Interface for separating speakers from audio content.
IStopwordsRemover:
    Interface for removing stopwords from text.
WhisperTranscribeProcessor:
    Base class for transcription with audio preprocessing support.
ResamplingVoiceSeparator:
    Base class for speaker separation with resampling support.
"""

from .iaudio_processing import *
from .istopwords_remover import *
from .itranscribe_processor import *
from .ivoice_separator import *

__all__ = ['ITranscribeProcessor', 'IVoiceSeparator', 'IStopwordsRemover', 'WhisperTranscribeProcessor',
           'ResamplingVoiceSeparator', 'IAudioProcessing']
