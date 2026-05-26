import streamlit as st
import os
import time
import tempfile
from dotenv import load_dotenv
from audio_recorder_streamlit import audio_recorder

from sarvam_utils import transcribe_audio, text_to_speech, get_chat_response
from youtube_utils import get_transcript_method_a, download_audio_method_b

load_dotenv()

# =========================================================
# 1. SARVAM BRANDING & PREMIUM GLASSMORPHIC DESIGN SYSTEM
# =========================================================
st.set_page_config(
    page_title="Sarvam Voice Tutor — VidTutor", 
    page_icon="🎓", 
    layout="wide"
)

# Premium aesthetic inject with CSS & Custom Google Fonts
st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
    
    <style>
    /* Global Base Styling */
    .stApp {
        background: radial-gradient(circle at 10% 20%, #161233 0%, #0d0a1b 90%);
        color: #f1f5f9;
        font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Elegant Header & Typography */
    .sarvam-title-container {
        padding: 2.5rem 0 1.5rem 0;
        animation: fadeIn 1s ease-out;
    }
    
    .sarvam-header {
        font-family: 'Space Grotesk', sans-serif;
        background: linear-gradient(135deg, #c084fc 0%, #818cf8 50%, #22d3ee 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 800;
        letter-spacing: -2px;
        margin-bottom: 0.5rem;
        line-height: 1.1;
    }
    
    .sarvam-subtitle {
        color: #94a3b8;
        font-size: 1.25rem;
        max-width: 800px;
        line-height: 1.6;
        font-weight: 300;
    }
    
    /* Premium Glassmorphic Cards */
    .sarvam-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 20px;
        padding: 28px;
        backdrop-filter: blur(24px) saturate(180%);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        margin-bottom: 1.8rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .sarvam-card:hover {
        transform: translateY(-4px);
        background: rgba(255, 255, 255, 0.04);
        border-color: rgba(129, 140, 248, 0.3);
        box-shadow: 0 20px 40px rgba(129, 140, 248, 0.1);
    }

    /* Gradient Section Titles */
    .section-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.6rem;
        font-weight: 600;
        background: linear-gradient(90deg, #ffffff 0%, #cbd5e1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Custom Streamlit Input Style Overrides */
    div[data-baseweb="input"] {
        background-color: rgba(15, 11, 35, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        transition: all 0.3s ease;
    }
    
    div[data-baseweb="input"]:focus-within {
        border-color: #818cf8 !important;
        box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.25) !important;
    }
    
    /* Hide Streamlit helper text like "Press Enter to apply" */
    div[data-testid="InputInstructions"] {
        display: none !important;
    }
    
    input {
        color: #ffffff !important;
        font-family: 'Outfit', sans-serif !important;
    }
    
    /* Sidebar Customizations */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0b0818 0%, #06040c 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
    }

    .sidebar-brand {
        text-align: center;
        padding: 2rem 0;
    }

    .sidebar-logo {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #a855f7 0%, #6366f1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 2px;
        margin-bottom: 0.2rem;
    }

    .sidebar-tagline {
        color: #64748b;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 3px;
        font-weight: 600;
    }

    /* Audio Equalizer Animation for Microphone */
    .eq-wave {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 4px;
        height: 30px;
        margin-top: 15px;
    }

    .eq-bar {
        width: 3px;
        height: 100%;
        background-color: #818cf8;
        border-radius: 3px;
        animation: eqPulse 1.2s ease-in-out infinite;
    }

    .eq-bar:nth-child(2) { animation-delay: 0.1s; height: 60%; }
    .eq-bar:nth-child(3) { animation-delay: 0.2s; height: 30%; }
    .eq-bar:nth-child(4) { animation-delay: 0.3s; height: 80%; }
    .eq-bar:nth-child(5) { animation-delay: 0.4s; height: 40%; }

    /* Keyframes */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes eqPulse {
        0%, 100% { transform: scaleY(0.3); }
        50% { transform: scaleY(1); }
    }
    
    /* Footer Credit styling */
    .sarvam-footer {
        text-align: center;
        margin-top: 6rem;
        color: #475569;
        font-size: 0.85rem;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        padding-top: 2rem;
        padding-bottom: 2rem;
        font-family: 'Space Grotesk', sans-serif;
    }

    /* Align input + button columns vertically */
    div[data-testid="stColumns"] {
        align-items: flex-end !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session states cleanly
if "api_key" not in st.session_state:
    st.session_state.api_key = os.getenv("SARVAM_API_KEY", "")
if "messages" not in st.session_state:
    st.session_state.messages = []
if "transcript" not in st.session_state:
    st.session_state.transcript = ""
if "last_processed_audio" not in st.session_state:
    st.session_state.last_processed_audio = None
if "chat_input_counter" not in st.session_state:
    st.session_state.chat_input_counter = 0
if "pending_text_query" not in st.session_state:
    st.session_state.pending_text_query = None

# =========================================================
# 2. SIDEBAR CONFIGURATION (Only shown once key is present)
# =========================================================
if st.session_state.api_key:
    with st.sidebar:
        st.markdown("<div class='sidebar-brand'><div class='sidebar-logo'>SARVAM AI</div><div class='sidebar-tagline'>Voice Intelligent Layer</div></div>", unsafe_allow_html=True)
        st.markdown("---")
        
        st.subheader("🔑 Authentication")
        updated_key = st.sidebar.text_input("Sarvam API Key", type="password", value=st.session_state.api_key)
        if updated_key != st.session_state.api_key:
            st.session_state.api_key = updated_key
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 🎛️ Pipeline Diagnostics")
        st.markdown("**⚡ Method A — Fast Captions**")
        st.caption("Instantly fetches official or auto-generated YouTube captions via the youtube-transcript-api. Zero cost, near-instant results. Works best when the video has subtitles available.")
        st.markdown("**🚀 Method B — Audio Stream**")
        st.caption("Downloads the raw audio stream via yt-dlp, downsamples to 16 kHz Mono WAV, enforces 30-second window bounds, and transcribes through Sarvam Speech-to-Text. Custom-tuned to bypass modern cloud security proxy issues for ultra-fast synchronous processing.")
else:
    # On landing/no key, hide the sidebar widgets cleanly
    with st.sidebar:
        st.markdown("<div class='sidebar-brand'><div class='sidebar-logo'>SARVAM AI</div><div class='sidebar-tagline'>Voice Intelligent Layer</div></div>", unsafe_allow_html=True)
        st.markdown("---")
        st.caption("Enter an API key on the main workspace to begin.")

# If API key is not entered yet, show Access Denied box on the main screen with input field and Submit button
if not st.session_state.api_key:
    st.markdown("""
        <div class='sarvam-card' style='text-align: center; padding: 40px; margin-top: 50px;'>
            <div style='font-size: 4rem; margin-bottom: 20px; animation: eqPulse 2s infinite;'>🔑</div>
            <h2 style='font-family: "Space Grotesk", sans-serif; color: #f43f5e; margin-bottom: 10px; font-weight: 700;'>Access Denied</h2>
            <p style='color: #94a3b8; font-size: 1.1rem; max-width: 600px; margin: 0 auto 12px auto;'>
                Please supply a valid Sarvam API Key below to activate the AI tutor workspace.
            </p>
            <a href='https://dashboard.sarvam.ai' target='_blank' style='color: #818cf8; font-weight: 600; text-decoration: none; font-size: 0.95rem;'>
                Don't have a key? Get a free API Key on Sarvam Dashboard ↗
            </a>
        </div>
    """, unsafe_allow_html=True)
    
    # Render input inside the box on main page
    key_input = st.text_input("Enter your Sarvam API Key:", type="password", placeholder="Paste your sk_... key here")
    
    submit_col1, submit_col2, submit_col3 = st.columns([1, 2, 1])
    with submit_col2:
        if st.button("Submit & Activate Workspace 🚀", use_container_width=True):
            if key_input:
                st.session_state.api_key = key_input
                st.rerun()
    st.stop()

# Local variable alias for compatibility with the rest of the script
api_key = st.session_state.api_key

# =========================================================
# 3. APP HEADER & MAIN CORE WORKSPACE
# =========================================================
st.markdown("""
    <div class='sarvam-title-container'>
        <h1 class='sarvam-header'>🎓 VidTutor</h1>
        <p class='sarvam-subtitle'>An advanced interactive knowledge retrieval engine mapping audio data into immersive conversational tutoring workspaces powered by Sarvam AI.</p>
    </div>
""", unsafe_allow_html=True)

# Clean, structured subheaders with no raw card HTML to prevent empty blue-ish bars
st.markdown("<div class='section-title'>🔗 Video Content Source</div>", unsafe_allow_html=True)

# YouTube URL input with a submit button side-by-side
if "yt_url_submitted" not in st.session_state:
    st.session_state.yt_url_submitted = ""

url_col, btn_col = st.columns([0.9, 0.1], gap="small")
with url_col:
    yt_url_input = st.text_input("Provide YouTube Video URL Target:", placeholder="https://www.youtube.com/watch?v=...", label_visibility="collapsed")
with btn_col:
    url_submit = st.button("➜", key="yt_submit_btn", use_container_width=True)

# Accept URL from either Enter key or button click
if url_submit and yt_url_input:
    st.session_state.yt_url_submitted = yt_url_input
if yt_url_input:
    st.session_state.yt_url_submitted = yt_url_input

youtube_url = st.session_state.yt_url_submitted

# Main layout logic branches once URL is specified
if youtube_url:
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    col_preview, col_controls = st.columns([1.2, 1], gap="large")
    
    with col_preview:
        st.markdown("<div class='section-title'>📺 Native Player Stream</div>", unsafe_allow_html=True)
        st.video(youtube_url)
        
    with col_controls:
        st.markdown("<div class='section-title'>⚡ Execution Management Engines</div>", unsafe_allow_html=True)
        st.caption("Choose an extraction engine pipeline option below to build out the learning context:")
        
        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        
        btn_col1, btn_col2 = st.columns(2)
        
        with btn_col1:
            if st.button("Method A (Fast Captions) ⚡", use_container_width=True):
                with st.spinner("Executing API caption scraping map..."):
                    try:
                        st.session_state.transcript = get_transcript_method_a(youtube_url)
                        st.success("Context loaded natively from captions.")
                    except Exception as e:
                        st.error(f"Method A Execution Fault: {e}")
                        
        with btn_col2:
            # Highlight Method B as the premium choice
            if st.button("Method B (Audio Stream) 🚀", use_container_width=True):
                with st.spinner("Processing deep audio parsing & deploying to Sarvam Speech-to-Text..."):
                    audio_file = None
                    try:
                        audio_file = download_audio_method_b(youtube_url)
                        result = transcribe_audio(audio_file, api_key)
                        if result and result.strip():
                            st.session_state.transcript = result
                            st.success("Context loaded seamlessly from binary stream analysis.")
                        else:
                            st.warning("STT returned an empty transcript. Try Method A instead, or retry when Sarvam services are fully operational.")
                    except Exception as e:
                        st.error(f"Method B Execution Fault: {e}")
                    finally:
                        if audio_file and os.path.exists(audio_file):
                            try:
                                os.remove(audio_file)
                            except OSError:
                                pass

# Expandable Transcript View Panel
if st.session_state.transcript:
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📖 View Decoded Knowledge Source Context Base"):
        st.info("The transcript excerpt shown below constitutes the strict boundary context window used by the underlying model to answer user queries.")
        st.write(st.session_state.transcript[:2000] + "..." if len(st.session_state.transcript) > 2000 else st.session_state.transcript)

    # =========================================================
    # 4. CHAT WORKSPACE & VOICE SYNTHESIS LAYER
    # =========================================================
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>💬 Dialogue with your Intelligent Tutor</div>", unsafe_allow_html=True)
    
    # Display historical dialog frames
    for msg in st.session_state.messages:
        role = msg["role"]
        content = msg["content"]
        with st.chat_message(role):
            st.markdown(content)
            if "audio" in msg and msg["audio"]:
                st.audio(msg["audio"], format="audio/wav")

    # Unified side-by-side Chat Input & Microphone panel at the bottom of dialogue
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    input_col, mic_col = st.columns([0.88, 0.12], gap="small")
    
    with input_col:
        user_text = st.text_input(
            "Message VidTutor...",
            placeholder="Type your question here to message VidTutor...",
            label_visibility="collapsed",
            key=f"chat_text_input_{st.session_state.chat_input_counter}"
        )
        
    with mic_col:
        audio_bytes = audio_recorder(
            text="", 
            recording_color="#f43f5e", 
            neutral_color="#818cf8", 
            icon_name="microphone", 
            icon_size="1x"
        )
    
    # Display glowing equalizer animation when recording/processing
    if audio_bytes and audio_bytes != st.session_state.get("last_processed_audio"):
        st.markdown("""
            <div class="eq-wave">
                <div class="eq-bar"></div>
                <div class="eq-bar"></div>
                <div class="eq-bar"></div>
                <div class="eq-bar"></div>
                <div class="eq-bar"></div>
            </div>
        """, unsafe_allow_html=True)
    
    user_query = None
    
    # Handle physical voice input
    if audio_bytes and audio_bytes != st.session_state.get("last_processed_audio"):
        st.session_state.last_processed_audio = audio_bytes
        # WAV header is 44 bytes; anything under ~2KB is an accidental tap with no real audio
        if len(audio_bytes) < 2000:
            st.warning("Recording too short — hold the mic button and speak, then release.")
        else:
            with st.spinner("Decoding audio frequencies via Sarvam STT Core..."):
                tmp_path = None
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                        tmp.write(audio_bytes)
                        tmp_path = tmp.name
                    user_query = transcribe_audio(tmp_path, api_key)
                except Exception as e:
                    st.error(f"Sarvam Voice Capture Error: {e}")
                finally:
                    if tmp_path and os.path.exists(tmp_path):
                        try:
                            os.remove(tmp_path)
                        except OSError:
                            pass
                
    if user_text:
        user_query = user_text

    # Execute main AI intelligence layer logic
    if user_query:
        # Add tracking data to state parameters
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)
            
        with st.chat_message("assistant"):
            with st.spinner("Consulting knowledge framework maps..."):
                system_prompt = f"""You are VidTutor, an educational AI tutor. 
You must answer the user's questions strictly based on the following transcript from a YouTube video.
If the answer is not in the transcript, say "I can only answer questions based on the video content, and I don't see the answer to that here."
Keep answers concise and conversational, suitable for voice playback.

TRANSCRIPT:
{st.session_state.transcript}"""

                messages = [{"role": "system", "content": system_prompt}]
                for m in st.session_state.messages:
                    if m["role"] == "user":
                        messages.append({"role": "user", "content": m["content"]})
                    elif m["role"] == "assistant":
                        messages.append({"role": "assistant", "content": m["content"]})
                
                try:
                    bot_response = get_chat_response(messages, api_key)
                    st.markdown(bot_response)
                    
                    # Synthesize text back to audio via Sarvam TTS engine
                    with st.spinner("Synthesizing dynamic voice response..."):
                        audio_data = text_to_speech(bot_response, api_key)
                        if audio_data:
                            st.audio(audio_data, format="audio/wav", autoplay=True)
                            st.session_state.messages.append({"role": "assistant", "content": bot_response, "audio": audio_data})
                        else:
                            st.session_state.messages.append({"role": "assistant", "content": bot_response})
                except Exception as e:
                    st.error(f"Inference Engine Exception: {e}")
        
        # Clear the text input by incrementing the key counter and rerunning
        if user_text:
            st.session_state.chat_input_counter += 1
            st.rerun()

# Structural signature footer text
st.markdown("<div class='sarvam-footer'>Core Application UI powered by Sarvam AI Custom Extraction Pipelines • 2026</div>", unsafe_allow_html=True)