import os
import re
import requests
import base64
from openai import OpenAI

def transcribe_audio(audio_path, api_key):
    """Speech-to-Text using saaras:v3 model with proper context management."""
    url = "https://api.sarvam.ai/speech-to-text"
    headers = {"api-subscription-key": api_key}
    
    data = {
        "model": "saaras:v3",
        "mode": "transcribe"
    }
    
    try:
        with open(audio_path, "rb") as f:
            # Explicitly supply the tuple format (filename, file_stream, content_type) 
            # to keep Azure Application Gateway's firewall happy.
            files = {
                "file": (os.path.basename(audio_path), f, "audio/wav")
            }
            response = requests.post(url, headers=headers, files=files, data=data)
        
        if response.status_code == 200:
            return response.json().get("transcript", "")
    except Exception:
        pass  # Proceed to try fallback if there was an exception
        
    # Fallback to translate if standard endpoint fails
    url_translate = "https://api.sarvam.ai/speech-to-text-translate"
    with open(audio_path, "rb") as f:
        files = {
            "file": (os.path.basename(audio_path), f, "audio/wav")
        }
        response_translate = requests.post(url_translate, headers=headers, files=files, data=data)
        
    if response_translate.status_code == 200:
        return response_translate.json().get("transcript", "")
    raise Exception(f"STT Error: {response_translate.text}")

def text_to_speech(text, api_key, language="en-IN", speaker="aditya"):
    """Text-to-Speech using bulbul:v3 model. Handles the 500-char limit by chunking."""
    url = "https://api.sarvam.ai/text-to-speech"
    headers = {
        "api-subscription-key": api_key,
        "Content-Type": "application/json"
    }
    
    # Chunk text into ≤500 char segments at sentence boundaries
    max_chars = 480  # Leave some margin below the 500 limit
    chunks = []
    remaining = text.strip()
    while remaining:
        if len(remaining) <= max_chars:
            chunks.append(remaining)
            break
        # Find the last sentence-ending punctuation within the limit
        cut = max_chars
        for sep in ['. ', '! ', '? ', '.\n', '!\n', '?\n']:
            idx = remaining[:max_chars].rfind(sep)
            if idx != -1:
                cut = idx + len(sep)
                break
        else:
            # No sentence boundary found; fall back to last space
            space_idx = remaining[:max_chars].rfind(' ')
            if space_idx > 0:
                cut = space_idx + 1
        chunks.append(remaining[:cut].strip())
        remaining = remaining[cut:].strip()
    
    # Synthesize each chunk and concatenate audio bytes
    all_audio = b""
    for chunk in chunks:
        if not chunk:
            continue
        payload = {
            "inputs": [chunk],
            "target_language_code": language,
            "speaker": speaker,
            "pace": 1.0,
            "speech_sample_rate": 8000,
            "enable_preprocessing": True,
            "model": "bulbul:v3"
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            audios = response.json().get("audios", [])
            if audios:
                all_audio += base64.b64decode(audios[0])
        else:
            raise Exception(f"TTS Error: {response.text}")
    
    return all_audio if all_audio else None

def get_chat_response(messages, api_key):
    """OpenAI-compatible Chat via Sarvam's own LLM endpoint."""
    client = OpenAI(
        base_url="https://api.sarvam.ai/v1",
        api_key=api_key
    )
    
    # Sarvam requires strict user/assistant alternation starting with a user message.
    # Fold any system prompt into the first user message.
    system_content = ""
    cleaned_messages = []
    for msg in messages:
        role = msg["role"]
        content = msg["content"]
        if role == "system":
            system_content = content
        elif role in ("user", "assistant"):
            cleaned_messages.append({"role": role, "content": content})

    # Prepend system instructions to the first user message
    if system_content and cleaned_messages and cleaned_messages[0]["role"] == "user":
        cleaned_messages[0]["content"] = f"{system_content}\n\nUser question: {cleaned_messages[0]['content']}"

    response = client.chat.completions.create(
        model="sarvam-m",
        messages=cleaned_messages,
        temperature=0.2
    )
    raw_content = response.choices[0].message.content
    # Strip <think>...</think> reasoning traces from sarvam-m responses
    cleaned = re.sub(r"<think>.*?</think>\s*", "", raw_content, flags=re.DOTALL)
    return cleaned.strip()