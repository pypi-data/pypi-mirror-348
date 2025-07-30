"""
Module: audio_segmenter

This module provides the `AudioSegmenter` class, which provides methods for
extracting audio segments from an audio file based on specified start and end
timestamps.

Classes
-------
AudioSegmenter :
    A utility class for extracting audio segments.
"""

from io import BytesIO

import soundfile as sf


class AudioSegmenter(object):
    """
    Provides functionality to extract specific segments from audio data.

    This class facilitates the extraction of an audio fragment from a given
    input audio content using specified start and end timestamps. It is
    particularly useful for audio processing tasks where specific sections
    of audio need to be isolated.
    """

    @staticmethod
    def extract_audio_segment(
            content: bytes,
            start_time: float,
            end_time: float
    ) -> bytes:
        """
        Extracts an audio fragment from the complete audio based on the specified timestamps.

        Parameters
        ----------
        content :
            Original audio content in bytes format.
        start_time :
            The starting time of the segment (in seconds).
        end_time :
            The ending time of the segment (in seconds).

        Returns
        -------
        bytes
            The audio fragment in bytes format.
        """

        audio_stream = BytesIO(content)
        audio, sr = sf.read(audio_stream)

        start_sample = int(start_time * sr)
        end_sample = int(end_time * sr)

        segment = audio[start_sample:end_sample]

        segment_stream = BytesIO()
        sf.write(segment_stream, segment, samplerate=sr, format='WAV')
        return segment_stream.getvalue()
