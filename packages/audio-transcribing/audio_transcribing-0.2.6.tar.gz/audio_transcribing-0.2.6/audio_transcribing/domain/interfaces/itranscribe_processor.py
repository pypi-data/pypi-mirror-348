"""
Module: itranscribe_processor

This module defines interfaces and base implementations for audio transcription tasks.

Classes:
ITranscribeProcessor:
    Abstract interface for implementing audio transcription.
WhisperTranscribeProcessor:
    Base implementation of the ITranscribeProcessor interface, with additional
    support for audio preprocessing using `IAudioProcessing`.
"""

from abc import ABC, abstractmethod

import numpy as np

from .iaudio_processing import IAudioProcessing


class ITranscribeProcessor(ABC):
    """
    Interface for implementing audio transcription processes.

    This interface defines the contract for classes that transcribe audio content
    into text. Implementing classes must provide a `transcribe_audio` method.

    Methods
    -------
    transcribe_audio(content, language, main_theme):
        Transcribes audio content and optionally detects language.
    """

    @abstractmethod
    def transcribe_audio(
            self,
            content: np.ndarray,
            language: str = None,
            main_theme: str = None
    ) -> tuple[str, str]:
        """
        Transcribes the given audio content into text.

        Parameters
        ----------
        content : np.ndarray
            Raw audio data.
        language : str, optional
            The language of the audio content. If not provided, it should
            be detected automatically.
        main_theme : str, optional
            A contextual theme or prompt for better transcription accuracy.

        Returns
        -------
        tuple[str, str]
            A tuple containing:
            - str: The transcribed text.
            - str: The detected or specified language.
        """
        pass


class WhisperTranscribeProcessor(ITranscribeProcessor, IAudioProcessing):
    """
    Abstract base implementation of the ITranscribeProcessor interface.

    This class extends `ITranscribeProcessor` and integrates functionality from
    `IAudioProcessing` for audio preprocessing tasks, such as resampling or
    extracting audio streams.

    Methods
    -------
    transcribe_audio(content, language, main_theme):
        Transcribes audio content into text (abstract implementation that must be overridden).
    """

    @abstractmethod
    def transcribe_audio(
            self,
            audio: np.ndarray,
            language: str = None,
            main_theme: str = None
    ) -> tuple[str, str]: ...
