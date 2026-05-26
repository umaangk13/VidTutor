# VidTutor - Sarvam Voice Tutor 🎓

![VidTutor Interface](screenshot.png)

VidTutor is a modern, voice-first educational AI tutor that allows you to chat with any YouTube video using your voice. It leverages Sarvam AI's cutting-edge APIs for Speech-to-Text (STT), Text-to-Speech (TTS), and OpenAI-compatible Chat for grounded, conversational responses.

## ✨ Features

- **Premium Glassmorphic UI**: Beautiful, dynamic interface featuring a deep space gradient, interactive equalizer animations, and frosted glass elements.
- **Dual Transcript Extraction**: 
  - ⚡ *Method A (Fast Captions)*: Instant captions via `youtube-transcript-api`. Zero cost and near-instant results.
  - 🚀 *Method B (Audio Stream)*: Full audio download via `yt-dlp` and transcription using Sarvam's `saaras:v3` STT. Downsampled to 16kHz Mono to bypass modern cloud security proxy issues.
- **Strict Grounding**: The tutor answers questions *strictly* based on the video's content, preventing hallucinations.
- **Voice-to-Voice Loop**: Record your voice directly in the browser, get it transcribed, processed, and hear the tutor's response out loud using Sarvam's `bulbul:v3` TTS.
- **Robust API Handling**: Automatically chunks long TTS responses to bypass 500-character limits and dynamically clears UI states for a seamless chat experience.

## ⚙️ Prerequisites

- Python 3.8+
- [Sarvam AI API Key](https://dashboard.sarvam.ai)
- FFmpeg (required for `yt-dlp` audio extraction)

## 🚀 Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/umaangk13/VidTutor.git
   cd VidTutor
   ```

2. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

4. **Activate the Workspace**: Once the app opens, enter your Sarvam API Key in the sleek activation screen to unlock the tutor.

## 📖 Usage Guide

1. Enter a YouTube URL and click the **➜** button.
2. Choose your preferred transcript extraction method (Method A or B).
3. Use the **microphone icon** to speak your question or type it in the chat box.
4. Listen to your tutor's dynamic voice response!
