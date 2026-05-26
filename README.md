# VidTutor - Sarvam Voice Tutor 🎓

VidTutor is a modern, voice-first educational AI tutor that allows you to chat with any YouTube video using your voice. It leverages Sarvam AI's cutting-edge APIs for Speech-to-Text (STT) and Text-to-Speech (TTS), and an OpenAI-compatible Chat for grounded, conversational responses.

## Features

- **Dual Transcript Extraction**: 
  - *Method A*: Instant captions via `youtube-transcript-api`.
  - *Method B*: Full audio download via `yt-dlp` and transcription using Sarvam's `saaras:v3` STT.
- **Strict Grounding**: The tutor answers questions *strictly* based on the video's content, preventing hallucinations.
- **Voice-to-Voice Loop**: Record your voice in the browser, get it transcribed, processed, and hear the tutor's response out loud using Sarvam's `bulbul:v3` TTS.
- **Modern UI**: Built with Streamlit, featuring a dark-mode theme and sleek chat interface.

## Prerequisites

- Python 3.8+
- [Sarvam AI API Key](https://dashboard.sarvam.ai)
- FFmpeg (required for `yt-dlp` audio extraction)

## Installation

1. Navigate to the project directory.
2. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your Sarvam API Key:
   Create a `.env` file and add:
   ```env
   SARVAM_API_KEY=your_api_key_here
   ```
   Or, enter it directly in the Streamlit app sidebar.

## Usage

Run the Streamlit application:
```bash
streamlit run app.py
```

1. Enter a YouTube URL.
2. Choose a transcript extraction method.
3. Use the microphone icon to speak your question or type it in the chat box.
4. Listen to your tutor's response!
