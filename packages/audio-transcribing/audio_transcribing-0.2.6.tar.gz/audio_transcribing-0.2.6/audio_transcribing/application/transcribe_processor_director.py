"""
Module: transcribe_processor_director

This module provides the `TranscribeProcessorDirector` class, which coordinates
audio transcription tasks through a specified `WhisperTranscribeProcessor`.

Classes
-------
TranscribeProcessorDirector:
    Responsible for processing audio transcription tasks.
"""

from ..domain import WhisperTranscribeProcessor


class TranscribeProcessorDirector(object):
    """
    This class directs audio transcription tasks by delegating processing
    responsibilities to a provided `WhisperTranscribeProcessor`.

    Methods
    -------
    set_processor(processor):
        Sets a new processor for transcription tasks.
    transcribe_audio(content, language=None, main_theme=None):
        Processes and transcribes the given audio content.

    Example Usage
    -------------
    processor = WhisperTranscribeProcessor(...)
    director = TranscribeProcessorDirector(processor)
    transcription, language = director.transcribe_audio(content=b"audio bytes")
    """

    def __init__(self, processor: WhisperTranscribeProcessor):
        """
        Represents a utility class for handling a processor instance.

        Parameters
        ----------
        processor : WhisperTranscribeProcessor
            Internal processor instance utilized for transcription-related
            tasks.

        Raises
        ------
        TypeError
            If processor is not an instance of WhisperTranscribeProcessor.
        """

        self._processor: WhisperTranscribeProcessor | None = None
        self.set_processor(processor)

    def set_processor(self, processor: WhisperTranscribeProcessor) -> None:
        """
        A method to set the processor instance for the current object.

        This method allows the assignment or update of the `WhisperTranscribeProcessor`
        instance for handling specific processing tasks.

        Parameters
        ----------
        processor : WhisperTranscribeProcessor
            The processor instance to be set.

        Raises
        ------
        TypeError
            If processor is not an instance of WhisperTranscribeProcessor.
        """
        if not isinstance(processor, WhisperTranscribeProcessor):
            raise TypeError("Processor must be an instance of WhisperTranscribeProcessor.")

        self._processor = processor

    def transcribe_audio(
            self,
            content: bytes,
            language: str = None,
            main_theme: str = None
    ) -> tuple[str, str]:
        """
        Transcribes the given audio content and optionally detects its language.

        This method performs a series of processing steps:
            - Extracts the audio stream from the provided content.
            - Converts the audio to a mono channel.
            - Resamples the audio to match the required sample rate.
            - Uses the `processor` to generate a transcription of the audio.

        To set a new processor, use the `set_processor` method.

        Parameters
        ----------
        content : bytes
            The raw audio content to be transcribed.
        language : str, optional
            Language of the audio. If not provided, it will be detected
            automatically.
        main_theme : str, optional
            A contextual theme or prompt to enhance transcription accuracy.

        Returns
        -------
        tuple[str, str]:
            A tuple containing the transcribed text and the detected language.
        """

        audio, sr = self._processor.get_audio_stream(content)
        audio = self._processor.get_mono_audio(audio)
        audio = self._processor.resample_audio(audio, sr)

        return self._processor.transcribe_audio(audio, language, main_theme)
