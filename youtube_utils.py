import os
import re
import uuid
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi

def get_video_id(url):
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_transcript_method_a(url):
    """
    Method A: Fetches official or auto-generated transcripts via youtube-transcript-api.
    This fetches the entire video's transcript instantly and at zero cost.
    Uses the v1.2.x instance-based API: YouTubeTranscriptApi().fetch(video_id).
    """
    video_id = get_video_id(url)
    if not video_id:
        raise ValueError("Could not extract a valid YouTube video ID from the provided URL.")
    
    try:
        ytt_api = YouTubeTranscriptApi()
        transcript_snippets = ytt_api.fetch(video_id)
        transcript_text = " ".join([snippet.text for snippet in transcript_snippets])
        return transcript_text
    except Exception as e:
        raise RuntimeError(
            f"Failed to fetch YouTube transcript. The video may not have subtitles/captions enabled. "
            f"Please try Method B (Audio Stream Extraction). Error: {e}"
        )

def download_audio_method_b(url, output_path=None):
    """
    Method B: Highly compressed, 30-second capped audio downloader.
    Automatically clips the video to the first 30 seconds to bypass 
    Azure's maximum duration limit for synchronous STT requests.
    """
    if output_path is None:
        output_path = f"temp_audio_{uuid.uuid4().hex[:8]}.wav"

    if os.path.exists(output_path):
        try:
            os.remove(output_path)
        except OSError:
            pass

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '16',
        }],
        # CRITICAL FIX: 
        # '-ss 00:00:00 -t 30' clips the download to exactly the first 30 seconds.
        # '-ar 16000 -ac 1' ensures the layout matches the optimal STT audio specification.
        'postprocessor_args': [
            '-ss', '00:00:00',
            '-t', '30',
            '-ar', '16000',
            '-ac', '1'
        ],
        'outtmpl': output_path.replace('.wav', ''),
        'quiet': True,
        'no_warnings': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['ios', 'android', 'mweb'],
                'skip': ['dash', 'hls']
            }
        },
        'nocheckcertificate': True
    }
    
    try:
        print("Downloading and trimming first 30 seconds of video for Azure STT compatibility...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        if os.path.exists(output_path):
            file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
            print(f"Audio trimmed and downloaded successfully. Size: {file_size_mb:.2f} MB")
            return output_path
        else:
            raise FileNotFoundError("WAV file clipping and conversion failed.")
            
    except Exception as e:
        raise RuntimeError(f"Method B failed: {e}")