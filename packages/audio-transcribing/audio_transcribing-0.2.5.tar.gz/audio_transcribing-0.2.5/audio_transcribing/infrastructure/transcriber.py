"""
Module: transcriber

This module provides the `Transcriber` class, which combines utilities for
transcription and, speaker diarization. It integrates components like Whisper,
Faster Whisper and PyAnnote speaker diarization.

Classes
-------
Transcriber :
    A general-purpose transcription framework that supports multiple infrastructure
    and utilities.
"""

from .audio_segmenter import AudioSegmenter
from .faster_whisper_processor import FasterWhisperProcessor
from .voice_separator import VoiceSeparatorWithPyAnnote
from .whisper_processor import WhisperProcessor
from ..application import TranscribeProcessorDirector, VoiceSeparatorDirector


class Transcriber(object):
    """
    A general-purpose transcription and audio processing utility.

    This class integrates several functionalities for processing audio:
    - Transcription using Whisper/Faster Whisper.
    - Speaker diarization using PyAnnote.

    Methods
    -------
    transcribe(content, language, max_speakers):

    Example Usage
    -------------
    transcriber = Transcriber(token)


    """

    def __init__(
            self,
            token: str,
            whisper_model: str = "medium",
            speaker_diarization_model: str = "pyannote/speaker-diarization-3.1",
            use_faster_whisper: bool = False
    ):
        """
        Initializes the Transcriber with the specified infrastructure and configurations.

        Parameters
        ----------
        token : str
            HuggingFace Authorization token for accessing PyAnnote's speaker
            diarization model.
        whisper_model : str, optional
            Whisper model size to use ('base', 'medium', 'large'). Defaults to
            'medium'.
        speaker_diarization_model : str, optional
            HuggingFace PyAnnote model for speaker diarization. Defaults to
            'pyannote/speaker-diarization-3.1'.
        use_faster_whisper : bool, optional
            Whether to use Faster Whisper instead of Whisper for transcription.
            Defaults to False. Use this option if you are running with CUDA.
        """

        whisper_processor = FasterWhisperProcessor(whisper_model) \
            if use_faster_whisper else WhisperProcessor(whisper_model)
        self._whisper_director = TranscribeProcessorDirector(whisper_processor)

        voice_processor = VoiceSeparatorWithPyAnnote(
            token,
            model_name=speaker_diarization_model
        )
        self._voice_sep_director = VoiceSeparatorDirector(voice_processor)

    def transcribe(
            self,
            content: bytes,
            language: str = None,
            max_speakers: int = None,
            main_theme: str = None,
    ) -> tuple[str, str]:
        """
        Transcribes the given audio content and performs speaker diarization.

        This method processes multi-speaker audio content by separating
        speakers and transcribing each speaker's segments independently.

        Parameters
        ----------
        content : bytes
            The raw audio content in bytes format (e.g., WAV or MP3).
        language : str, optional
            Language of the audio. If None, the model will attempt to detect
            it automatically.
        max_speakers : int, optional
            Maximum number of speakers to identify. If None, the model will
            decide automatically.
        main_theme : str, optional
            Keywords for audio. Special vocabulary.

        Returns
        -------
        tuple[str,str]
            Full transcription of the audio with speaker separation
            annotations, formatted as:
                [Speaker] Transcription...
            Detected language
        """

        segments = self._voice_sep_director.separate_speakers(
            content=content,
            max_speakers=max_speakers
        )

        transcription_results = []

        detected_language = "Not found"
        for segment in segments:
            segment_audio = AudioSegmenter.extract_audio_segment(
                content,
                segment["start"],
                segment["end"],
            )

            segment_text, detected_language = self._whisper_director.transcribe_audio(
                content=segment_audio,
                language=language,
                main_theme=main_theme,
            )

            transcription_results.append(
                f"[{segment["speaker"]}: {segment["start"]}] {segment_text.strip()}"
            )

        full_transcription = "\n\n".join(transcription_results)

        return full_transcription, detected_language
