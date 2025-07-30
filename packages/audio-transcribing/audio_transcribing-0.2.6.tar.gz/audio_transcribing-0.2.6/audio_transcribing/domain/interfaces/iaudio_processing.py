"""
Module: iaudio_processing

This module provides the `IAudioProcessing` class, which includes methods
to handle common audio processing tasks.

Classes
-------
IAudioProcessing: An abstract class for audio processing functions.
"""

from abc import abstractmethod, ABC

import numpy as np


class IAudioProcessing(ABC):
    """
    A class that provides methods for audio processing tasks.

    Methods
    -------
    get_audio_stream(content):
        Extracts the audio stream and sample rate from raw audio bytes.
    get_mono_audio(audio):
        Converts audio signal to a mono channel.
    resample_audio(audio, sr):
        Resamples the audio to a fixed sample rate.
    """

    @staticmethod
    @abstractmethod
    def get_audio_stream(content: bytes) -> tuple[np.ndarray, int]:
        """
        Extracts the audio stream and sample rate from the provided raw audio content.

        Parameters
        ----------
        content : bytes
            Raw audio data in byte format.

        Returns
        -------
        tuple[np.ndarray, int]
        """
        pass

    @staticmethod
    @abstractmethod
    def get_mono_audio(audio: np.ndarray) -> np.ndarray:
        """
        Converts multi-channel audio to mono.

        Parameters
        ----------
        audio : np.ndarray
            The audio data array, which may be single- or multi-channel.

        Returns
        -------
        np.ndarray
            The audio data array converted to mono format.
        """
        pass

    @staticmethod
    @abstractmethod
    def resample_audio(audio: np.ndarray, sr: int) -> np.ndarray:
        """
        Resamples the provided audio to a fixed sample rate.

        If the current sample rate does not match the fixed rate,
        this method performs a resampling operation to adjust the sample rate.

        Parameters
        ----------
        audio : np.ndarray
            The raw audio data to be resampled.
        sr : int
            The current sample rate of the audio.

        Returns
        -------
        np.ndarray
            The resampled audio data.
        """
        pass
