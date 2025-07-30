"""
Package: audio_transcribing.application
-----------------------------------

This package provides utility classes for directing and managing audio-related
processing tasks, such as transcription and speaker diarization.

Classes
TranscribeProcessorDirector:
VoiceSeparatorDirector:
"""

from .transcribe_processor_director import *
from .voice_separator_director import *

__all__ = ["TranscribeProcessorDirector", "VoiceSeparatorDirector"]
