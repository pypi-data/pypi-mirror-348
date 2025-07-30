"""
Module: voice_separator

This module defines the `VoiceSeparatorWithPyAnnote` class, which separates
speakers in audio data using the PyAnnote speaker diarization library.

Classes
-------
VoiceSeparatorWithPyAnnote :
    Speaker diarization with PyAnnote library.
"""

from copy import deepcopy
from typing import Any

import numpy as np
import torch
from pyannote.audio import Pipeline

from .audio_processing import AudioProcessing
from ..domain import ResamplingVoiceSeparator


class VoiceSeparatorWithPyAnnote(AudioProcessing, ResamplingVoiceSeparator):
    """
    Implements speaker separation using PyAnnote.

    Methods
    -------
    separate_speakers(audio, max_speakers):
        Performs speaker diarization on input audio.
    """

    def __init__(
            self,
            token: str,
            model_name: str = "pyannote/speaker-diarization-3.1"
    ):
        """
        Initializes the VoiceSeparatorWithPyAnnote.

        Parameters
        ----------
        token : str
            The HuggingFace token for loading the pretrained model.
        model_name : str, optional
            The name of the HuggingFace model. Defaults to 'pyannote/speaker-diarization-3.1'.
        """

        try:
            self._pipeline = Pipeline.from_pretrained(
                model_name,
                use_auth_token=token
            )

            self._device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self._pipeline.to(self._device)

        except Exception as e:
            raise RuntimeError(f"Failed to load PyAnnote pipeline: {e}")

    def separate_speakers(
            self,
            audio: np.ndarray,
            max_speakers: int = None
    ) -> list[dict]:
        """
        Performs speaker diarization on the given audio data.

        Parameters
        ----------
        audio : np.ndarray
            The input audio data to process.
        max_speakers : int, optional
            The maximum number of speakers to detect. Defaults to None.

        Returns
        -------
        list[dict]
            A list of dictionaries representing speaker segments,
            each containing keys:
            - 'start': float, start time.
            - 'end': float, end time.
            - 'speaker': str, speaker ID.
        """

        audio = audio.astype(np.float32)

        pipelane_args = {
            "waveform": torch.tensor(audio).unsqueeze(0),
            "sample_rate": 16000,
        }
        if max_speakers is not None:
            pipelane_args["max_speakers"] = max_speakers

        timeline = self._pipeline(pipelane_args)

        speaker_segments = []
        for speech_segment in timeline.itertracks(yield_label=True):
            segment, _, speaker = speech_segment
            speaker_segments.append({
                "start": segment.start,
                "end": segment.end,
                "speaker": speaker,
            })

        return self._unite_segments(speaker_segments)

    @staticmethod
    def _unite_segments(segments: list[dict[str, Any]]) -> list[dict[str, Any]]:
        speaker_segments = deepcopy(segments)

        prev_segment = speaker_segments[0]
        for segment in speaker_segments[1:]:
            if prev_segment["speaker"] == segment["speaker"]:
                segment["start"] = prev_segment["start"]
                speaker_segments.remove(prev_segment)

            prev_segment = segment

        return speaker_segments
