"""
Module: audio_processing_mixin

This module provides the `AudioProcessingMixin` class, which includes static methods
to handle common audio processing tasks. These tasks include audio stream extraction,
conversion to mono channel, and audio resampling.

Classes
-------
AudioProcessingMixin: A utility mixin for audio processing functions.
"""

from io import BytesIO

import numpy as np
import scipy.signal
import soundfile as sf

from ..domain import IAudioProcessing


class AudioProcessing(IAudioProcessing):
    """
    A class that provides static methods for audio processing tasks.

    This class serves as a utility mixin, supplying reusable audio processing
    functions that can be used in other components or classes.

    Methods
    -------
    get_audio_stream(content):
        Extracts the audio stream and sample rate from raw audio bytes.
    get_mono_audio(audio):
        Converts audio signal to a mono channel if it is multi-channel.
    resample_audio(audio, sr):
        Resamples the audio to a fixed sample rate of 16 kHz.

    Example Usage
    --------------
    # Use the mixin as part of another class or call its methods directly as static.

    audio, sr = AudioProcessingMixin.get_audio_stream(content)
    audio = AudioProcessingMixin.get_mono_audio(audio)
    audio = AudioProcessingMixin.resample_audio(audio, sr)
    """

    @staticmethod
    def get_audio_stream(content: bytes) -> tuple[np.ndarray, int]:
        """
        Extracts the audio stream and sample rate from the provided raw audio content.

        This method reads raw audio bytes, extracts the actual audio data,
        and determines its current sample rate.

        Parameters
        ----------
        content : bytes
            Raw audio data in byte format.

        Returns
        -------
        tuple[np.ndarray, int]
            A tuple containing:
            - The raw audio data as an array.
            - The sample rate of the audio.
        """

        audio_stream = BytesIO(content)
        audio, sr = sf.read(audio_stream)

        return audio, sr

    @staticmethod
    def get_mono_audio(audio: np.ndarray) -> np.ndarray:
        """
        Converts multi-channel audio to mono by averaging all channels.

        This method computes the mean across multiple channels for input
        audio signals that are multi-channel (e.g., stereo). If the audio
        is already mono, it returns the input as is.

        Parameters
        ----------
        audio : np.ndarray
            The audio data array, which may be single- or multi-channel.

        Returns
        -------
        np.ndarray
            The audio data array converted to mono format.
        """

        if len(audio.shape) > 1:
            audio = np.mean(audio, axis=1)

        return audio

    @staticmethod
    def resample_audio(audio: np.ndarray, sr: int) -> np.ndarray:
        """
        Resamples the provided audio to a fixed sample rate of 16 kHz.

        If the current sample rate does not match the fixed rate of 16,000 Hz,
        this method performs a resampling operation to adjust the sample rate.
        Audio signals that are already at 16 kHz are returned unchanged.

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

        if sr != 16000:
            number_of_samples = round(len(audio) * float(16000) / sr)
            audio = scipy.signal.resample(audio, number_of_samples)

        return audio
