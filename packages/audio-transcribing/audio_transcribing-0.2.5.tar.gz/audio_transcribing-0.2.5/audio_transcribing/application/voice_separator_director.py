"""
Module: voice_separator_director

This module defines the `VoiceSeparatorDirector` class, which handles speaker separation
and diarization tasks using a specified `ResamplingVoiceSeparator`.

Classes
-------
VoiceSeparatorDirector:
    Responsible for managing speaker diarization tasks.
"""

from ..domain import ResamplingVoiceSeparator


class VoiceSeparatorDirector(object):
    """
    Manages a voice separation process using a provided separator object.

    This class acts as a director for a given separator implementation, such as
    `ResamplingVoiceSeparator`. It is responsible for managing and delegating
    tasks related to processing audio content to isolate different speakers.

    Methods
    -------
    set_separator(separator):
        Updates the separator instance for handling speaker separation tasks.
    separate_speakers(content, max_speakers=None):
        Performs speaker diarization to separate the provided audio content into
        segments.

    Example Usage
    -------------
    segmenter = ResamplingVoiceSeparator(...)
    director = VoiceSeparatorDirector(processor)
    segments = director.separate_speakers(content, max_speakers=2)
    """

    def __init__(self, separator: ResamplingVoiceSeparator):
        """
        Initializes the `VoiceSeparatorDirector` with the specified separator.

        Parameters
        ----------
        separator : ResamplingVoiceSeparator
            The separator instance used for handling speaker separation tasks.

        Raises
        ------
        TypeError
            If the provided separator is not an instance of ResamplingVoiceSeparator.
        """

        self._separator: ResamplingVoiceSeparator | None = None
        self.set_separator(separator)

    def set_separator(self, separator: ResamplingVoiceSeparator):
        """
        Updates the separator instance used for speaker separation tasks.

        Parameters
        ----------
        separator : ResamplingVoiceSeparator
            The new separator instance to be used for processing speaker isolation.

        Raises
        ------
        TypeError
            If the provided separator is not an instance of ResamplingVoiceSeparator.
        """

        if not isinstance(separator, ResamplingVoiceSeparator):
            raise TypeError("Separator must be an instance of ResamplingVoiceSeparator.")

        self._separator = separator

    def separate_speakers(
            self,
            content: bytes,
            max_speakers: int | None = None
    ) -> list[dict]:
        """
        Separates speakers in the given audio content.

        This method processes the provided audio by:
            - Extracting the audio stream.
            - Converting it to mono channel.
            - Resampling it to the required sample rate.
            - Using the `separator` to separate the audio into speaker segments.

        To update the separator instance, use the `set_separator` method.

        Parameters
        ----------
        content : bytes
            The raw audio bytes to process.
        max_speakers : int, optional
            A limit for the maximum number of speakers to detect. If not
            specified, the detection algorithm determines the number of
            speakers automatically.

        Returns
        -------
        list[dict]:
            A list of dictionaries, each describing a detected speaker segment
            with data such as start and end times.
        """

        audio, sr = self._separator.get_audio_stream(content)
        audio = self._separator.get_mono_audio(audio)
        audio = self._separator.resample_audio(audio, sr)

        return self._separator.separate_speakers(audio, max_speakers)
