"""
Module: ivoice_separator

This module defines interfaces and base implementations for speaker separation tasks.

Classes
-------
IVoiceSeparator:
    Abstract interface for separating speakers in audio content.
ResamplingVoiceSeparator:
    A base implementation of the IVoiceSeparator interface, which includes
    resampling utilities through `IAudioProcessing`.
"""

from abc import ABC, abstractmethod

import numpy as np

from .iaudio_processing import IAudioProcessing


class IVoiceSeparator(ABC):
    """
    Interface for implementing speaker separation functionality.

    This interface defines the contract for any class that processes audio
    content to separate speakers. Implementing classes must provide a
    `separate_speakers` method.

    Methods
    -------
    separate_speakers(content, num_speakers):
        Separates the audio content into segments for the specified maximum number of speakers.
    """

    @abstractmethod
    def separate_speakers(
            self,
            content: np.ndarray,
            max_speakers: int
    ) -> list[dict]:
        """
        Separates the given audio content into speaker segments.

        Parameters
        ----------
        content: np.ndarray
            The audio data as a numpy array, typically a waveform.
        max_speakers: int
            The maximum number of speakers to separate in the audio content.

        Returns
        -------
        list[dict]:
            A list of dictionaries, where each dictionary represents a speaker
            segment with data such as start time, end time, and speaker ID.
        """
        pass


class ResamplingVoiceSeparator(IVoiceSeparator, IAudioProcessing):
    """
    Abstract base implementation of the IVoiceSeparator interface.

    This class extends `IVoiceSeparator` and integrates functionality from
    `AudioProcessingMixin` for preprocessing tasks such as resampling audio.

    Methods
    -------
    separate_speakers(content, max_speakers):
        Separates audio content into speaker segments (abstract implementation that must be overridden).
    """

    @abstractmethod
    def separate_speakers(
            self,
            content: np.ndarray,
            max_speakers: int
    ) -> list[dict]: ...
