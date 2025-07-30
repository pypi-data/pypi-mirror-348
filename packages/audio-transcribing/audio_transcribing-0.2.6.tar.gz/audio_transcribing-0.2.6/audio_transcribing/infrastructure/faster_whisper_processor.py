"""
Module: faster_whisper_processor

This module defines the `FasterWhisperProcessor` class for fast
speech-to-text transcription using the Faster Whisper library.

Classes
-------
FasterWhisperProcessor :
    Provides efficient transcription for audio data.
"""

import numpy as np
from faster_whisper import WhisperModel

from .audio_processing import AudioProcessing
from ..domain import WhisperTranscribeProcessor


class FasterWhisperProcessor(AudioProcessing, WhisperTranscribeProcessor):
    """
    A processor for faster audio-to-text transcription using Faster Whisper.
    If using CPU, it is recommended to use 'WhisperProcessor' instead.

    Methods
    -------
    transcribe_audio(audio, language, main_theme):
        Transcribes audio content and optionally detects language.
    """

    def __init__(self, model_size: str = 'base'):
        """
        Initializes the FasterWhisperProcessor.

        Parameters
        ----------
        model_size : str, optional
            The size of the Faster Whisper model to load. Defaults to 'base'.

        Returns
        -------
        None
        """

        self._model_size = model_size
        self._model = WhisperModel(model_size)

    def transcribe_audio(
            self,
            audio: np.ndarray,
            language: str = None,
            main_theme: str = None
    ) -> tuple[str, str]:
        """
        Transcribes the given audio into text and detects the language.

        Parameters
        ----------
        audio : np.ndarray
            The input audio to transcribe.
        language : str, optional
            The language of the audio. Defaults to None (automatic detection).
        main_theme : str, optional
            A contextual prompt to enhance transcription accuracy.

        Returns
        -------
        tuple[str, str]
            A tuple containing the transcribed text, the detected language.
        """

        audio = audio.astype(np.float32)

        options = {
            "language": language,
            "initial_prompt": main_theme
        }
        segments, info = self._model.transcribe(audio, **options)

        transcription = " ".join(segment.text for segment in segments).strip()
        detected_language = info.language if language is None else language

        return transcription, detected_language
