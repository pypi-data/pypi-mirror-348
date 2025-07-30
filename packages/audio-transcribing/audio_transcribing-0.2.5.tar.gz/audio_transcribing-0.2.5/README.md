# Audio Transcription Toolkit

**A toolkit for audio processing**, including transcription, speaker diarization, and stopword removal.
This project is designed to deliver a seamless pipeline for processing audio data, identifying speakers,
and generating clean text transcriptions using Whisper, PyAnnote, and Natasha.

## Key Features

- **Transcription**: Converts audio to text using `Whisper` and `FasterWhisper` (for faster processing).
- **Speaker Diarization**: Separates and identifies individual speakers using PyAnnote.
- **Text Post-Processing**:
    - Remove stopwords and swear words using Natasha.
    - Customize stopword behaviors by adding your own rules.

---

## Installation

Make sure you have Python 3.8+ installed on your machine. To install this package, run:

```bash
pip install audio_transcribing
```

### Other requirements

If you’re using GPU for better performance, ensure `torch` is installed with GPU support. You can use:

```bash
pip install torch --index-url https://download.pytorch.org/whl/cu117
```

---

## Quick Start

### Transcription of Audio with Speaker Diarization and Cleaned Output

```python
from audio_transcriber.audio_transcribing import Transcriber, NatashaStopwordsRemover

# Initialize the transcriber
transcriber = Transcriber(
  token="your-huggingface-token",  # Token for PyAnnote diarization
  whisper_model="medium",  # Size of Whisper model
  use_faster_whisper=True  # Use Faster Whisper if performance is a priority
)

# Load the audio file
with open("your_file.mp3", "rb") as f:
  audio_content = f.read()

# Transcribe audio
result = transcriber.transcribe(audio_content, language="ru")

print("Transcription with speaker diarization:")
print(result)

# Post-process text (remove stopwords and optional swear words)
cleaned_result = NatashaStopwordsRemover.remove_stopwords(result, remove_swear_words=True)

print("\nCleaned transcription:")
print(cleaned_result)
```

---

### Add Stopwords or Swear Words to Natasha Processor

Natasha can be used only with russian language.

```python
from audio_transcriber.audio_transcribing import NatashaStopwordsRemover

# Initialize Natasha processor
stopwords_remover = NatashaStopwordsRemover()

# Add new custom stopwords
stopwords_remover.add_words_to_stopwords(["эм", "эй"])

# Add additional swear words
stopwords_remover.add_words_to_swear_words(["тварь", ])
```

---

## Modules Overview

### 1. **Transcriber**

The core of the project, managing transcription, speaker diarization, and post-processing. Key methods:

- `transcribe(content: bytes, language=None, max_speakers=None)`:
  Transcribes audio content and includes speaker annotations.

### 2. **NatashaStopwordsRemover**

Text post-processing with Natasha NLP:

- `remove_stopwords(text: str, remove_swear_words=True, go_few_times=False)`:
  Removes stopwords and optionally swear words from transcribed text.
- `remove_words(text: str, words: list[str])`:
  Removes predefined words from text.

---

## Limitations

- **Audio Format**: Tested on WAV and MP3 formats.
- **Speaker Diarization**: PyAnnote separates speakers but does not assign "real names" like "John" or "Mary".
- **Stopword Customization**: Requires russian language input for additional stopwords or swear words.

---

## License

This project is licensed under the MIT License.

---
