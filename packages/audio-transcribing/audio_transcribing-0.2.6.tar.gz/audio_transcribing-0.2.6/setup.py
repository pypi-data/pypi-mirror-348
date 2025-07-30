from setuptools import setup, find_packages

setup(
    name="audio_transcribing",
    version="0.2.6",
    description="A toolkit for audio transcription, speaker diarization, and text processing",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Tatsiana Kozlova",
    author_email="tanya126060@gmail.com",
    url="https://github.com/Lymuthien/transcriber-course-work",
    license="MIT",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        "numpy>=1.21.0",
        "soundfile>=0.10.3",
        "torch>=1.10.0",
        "faster-whisper>=1.0.0",
        "pyannote.audio>=2.0.1",
        "openai-whisper>=20240930",
        "torchvision>=0.21.0",
        "natasha>=1.6.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Libraries",
    ],
    include_package_data=True,
    zip_safe=False,
)
