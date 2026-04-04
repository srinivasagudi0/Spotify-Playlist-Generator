"""Beautiful Streamlit UI for the mood-to-Spotify recommender."""

import streamlit as st

from ai import AIError
from logic import format_output, recommend_songs
from main import get_market_code, get_recommendation_limit, get_recommendation_text, validate_config
from spotify import SpotifyError

# Page config
st.set_page_config(
    page_title="🎵 Mood-to-Spotify",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for beautiful styling
st.markdown("""
    <style>
    /* Main theme colors */
    :root {
        --spotify-green: #1DB954;
        --dark-bg: #121212;
        --darker-bg: #0f0f0f;
        --card-bg: #1e1e1e;
        --text-primary: #ffffff;
        --text-secondary: #b3b3b3;
    }
    
    /* Overall styling */
    .main {
        background-color: #0f0f0f;
        color: #ffffff;
    }
    
    /* Smooth scrolling */
    html {
        scroll-behavior: smooth;
    }
    
    /* Custom header */
    .header-container {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #1DB954 0%, #1ed760 100%);
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(29, 185, 84, 0.3);
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .header-subtitle {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.9);
        margin-top: 0.5rem;
    }
    
    /* Card styling */
    .info-card {
        background: linear-gradient(135deg, #1e1e1e 0%, #262626 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #1DB954;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    .emotion-card {
        background: linear-gradient(135deg, #1DB954 0%, #1ed760 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(29, 185, 84, 0.3);
    }
    
    /* Track card styling */
    .track-card {
        background: linear-gradient(135deg, #1e1e1e 0%, #262626 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-top: 3px solid #1DB954;
        margin: 0.75rem 0;
        transition: transform 0.2s, box-shadow 0.2s;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    .track-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(29, 185, 84, 0.2);
    }
    
    .track-index {
        font-size: 2rem;
        font-weight: 700;
        color: #1DB954;
        margin: 0 0 0.5rem 0;
    }
    
    .track-name {
        font-size: 1.2rem;
        font-weight: 600;
        color: white;
        margin: 0.5rem 0;
    }
    
    .track-artist {
        font-size: 1rem;
        color: #b3b3b3;
        margin: 0.25rem 0;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #1DB954 0%, #1ed760 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(29, 185, 84, 0.3);
        width: 100%;
    }
    
    .stButton > button:hover {
        box-shadow: 0 6px 20px rgba(29, 185, 84, 0.5);
        transform: translateY(-2px);
    }
    
    /* Input styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input {
        background-color: #262626 !important;
        color: #ffffff !important;
        border: 1px solid #404040 !important;
        border-radius: 8px !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stNumberInput > div > div > input:focus {
        border: 1px solid #1DB954 !important;
        box-shadow: 0 0 0 0.2rem rgba(29, 185, 84, 0.25) !important;
    }
    
    /* Slider styling */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #1DB954 0%, #1ed760 100%);
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #262626;
        color: #b3b3b3;
        border-radius: 8px 8px 0 0;
        padding: 1rem;
        margin-right: 0.25rem;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #1DB954;
        color: white;
    }
    
    /* Error and success styling */
    .stAlert {
        border-radius: 8px;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-color: #121212;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #262626;
        border-radius: 8px;
    }
    
    .section-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1DB954;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #1DB954;
    }
    
    .example-chip {
        display: inline-block;
        background-color: #262626;
        color: #1DB954;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        border: 1px solid #1DB954;
        margin: 0.5rem 0.25rem;
        cursor: pointer;
        font-size: 0.9rem;
        transition: all 0.2s;
    }
    
    .example-chip:hover {
        background-color: #1DB954;
        color: white;
    }
    
    .divider {
        border-top: 1px solid #404040;
        margin: 2rem 0;
    }
    
    /* Loading animation */
    .loading-container {
        text-align: center;
        padding: 2rem;
    }
    
    .loading-spinner {
        font-size: 3rem;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "form_data" not in st.session_state:
    st.session_state.form_data = {
        "mood_text": "",
        "limit": 5,
        "market": "US",
    }

if "result" not in st.session_state:
    st.session_state.result = None

if "terminal_output" not in st.session_state:
    st.session_state.terminal_output = ""

if "show_loading" not in st.session_state:
    st.session_state.show_loading = False


def set_mood_example(example_text):
    """Set mood text from example."""
    st.session_state.form_data["mood_text"] = example_text


# Header
st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🎵 Mood-to-Spotify</h1>
        <p class="header-subtitle">Turn your mood into the perfect playlist</p>
    </div>
""", unsafe_allow_html=True)

# Main layout
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<p class="section-title">🎯 Command Builder</p>', unsafe_allow_html=True)
    st.markdown("""
        <div class="info-card">
            <strong>Same inputs, same backend, beautiful shell.</strong><br/>
            Match the CLI prompts with an elegant interface.
        </div>
    """, unsafe_allow_html=True)

    # Mood text input
    st.markdown("**How are you feeling today?**")
    mood_text = st.text_area(
        "mood_text",
        value=st.session_state.form_data["mood_text"],
        placeholder="A little hopeful, a little tired, but still moving...",
        height=100,
        label_visibility="collapsed",
        help="Write it the way you would answer the CLI prompt. A full sentence works best."
    )
    st.session_state.form_data["mood_text"] = mood_text

    # Example moods
    st.markdown("**Quick moods:**")
    col_ex1, col_ex2 = st.columns(2)
    with col_ex1:
        if st.button("Warm, slow, late-night"):
            set_mood_example("Something warm, slow, and a little late-night.")
            st.rerun()
        if st.button("Soft and hopeful"):
            set_mood_example("I want something soft and hopeful that does not feel cheesy.")
            st.rerun()
    with col_ex2:
        if st.button("Focused, but alive"):
            set_mood_example("I need focus music that still feels alive, not sterile.")
            st.rerun()
        if st.button("Long-drive reset"):
            set_mood_example("Give me songs for a long drive after a heavy week.")
            st.rerun()

    st.divider()

    # Limit and market controls
    st.markdown("**How many tracks do you want?**")
    limit = st.slider(
        "limit",
        min_value=1,
        max_value=10,
        value=st.session_state.form_data["limit"],
        label_visibility="collapsed",
        help="Keep it short like a quick CLI result set."
    )
    st.session_state.form_data["limit"] = limit

    st.markdown("**Spotify market code**")
    market_options = ["US", "CA", "GB", "AU", "IN", "DE", "FR", "JP", "BR", "MX"]
    market = st.selectbox(
        "market",
        market_options,
        index=market_options.index(st.session_state.form_data["market"]),
        label_visibility="collapsed",
        help="Usually your two-letter country code."
    )
    st.session_state.form_data["market"] = market

    st.divider()

    # Action buttons
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        recommend_clicked = st.button(
            "🎧 Run Recommend",
            use_container_width=True,
            key="recommend_btn"
        )
    with col_btn2:
        check_clicked = st.button(
            "✓ Run Check-Config",
            use_container_width=True,
            key="check_btn"
        )

    # Handle button clicks
    if recommend_clicked or check_clicked:
        st.session_state.show_loading = True

        try:
            if check_clicked:
                # Check config
                try:
                    validate_config()
                    st.session_state.terminal_output = "✓ Configuration looks good!"
                    st.session_state.result = None
                except ValueError as error:
                    st.session_state.terminal_output = f"✗ Error: {str(error)}"
                    st.session_state.result = None
            else:
                # Recommend songs
                try:
                    validate_config()
                    mood_text_processed = get_recommendation_text(st.session_state.form_data["mood_text"])
                    limit_processed = get_recommendation_limit(st.session_state.form_data["limit"])
                    market_processed = get_market_code(st.session_state.form_data["market"])

                    st.session_state.result = recommend_songs(
                        mood_text_processed,
                        limit=limit_processed,
                        market=market_processed
                    )
                    st.session_state.terminal_output = format_output(st.session_state.result)

                except ValueError as error:
                    st.session_state.terminal_output = f"✗ Validation Error: {str(error)}"
                    st.session_state.result = None
                except AIError as error:
                    st.session_state.terminal_output = f"✗ AI Error: {str(error)}"
                    st.session_state.result = None
                except SpotifyError as error:
                    st.session_state.terminal_output = f"✗ Spotify Error: {str(error)}"
                    st.session_state.result = None
        finally:
            st.session_state.show_loading = False
            st.rerun()


with col2:
    st.markdown('<p class="section-title">💻 Session Output</p>', unsafe_allow_html=True)
    st.markdown("""
        <div class="info-card">
            <strong>CLI output mirror</strong><br/>
            Real-time feedback from your mood-to-Spotify engine.
        </div>
    """, unsafe_allow_html=True)

    # Terminal output
    if st.session_state.terminal_output:
        st.code(st.session_state.terminal_output, language="plaintext")
    else:
        st.info("👈 Fill in your mood and click 'Run Recommend' to see results here!")

    # Backend trace
    if st.session_state.result:
        st.markdown("**Backend Trace**")
        st.markdown("**Spotify Query:**")
        st.code(st.session_state.result.get("query", ""), language="plaintext")


# Tracks section
if st.session_state.result and st.session_state.result.get("songs"):
    st.markdown('<p class="section-title">🎵 Track Results</p>', unsafe_allow_html=True)

    emotion = st.session_state.result.get("emotion", {})
    if emotion:
        col_em1, col_em2, col_em3, col_em4 = st.columns(4)
        with col_em1:
            st.markdown("""
                <div class="emotion-card">
                    <strong>Emotion</strong><br/>
                    """ + emotion.get("emotion", "N/A") + """
                </div>
            """, unsafe_allow_html=True)
        with col_em2:
            st.markdown("""
                <div class="emotion-card">
                    <strong>Mood</strong><br/>
                    """ + emotion.get("mood", "N/A") + """
                </div>
            """, unsafe_allow_html=True)
        with col_em3:
            st.markdown("""
                <div class="emotion-card">
                    <strong>Energy</strong><br/>
                    """ + emotion.get("energy", "N/A") + """
                </div>
            """, unsafe_allow_html=True)
        with col_em4:
            st.markdown("""
                <div class="emotion-card">
                    <strong>Keywords</strong><br/>
                    """ + ", ".join(emotion.get("keywords", [])) + """
                </div>
            """, unsafe_allow_html=True)

        st.divider()

    # Display tracks
    songs = st.session_state.result.get("songs", [])
    st.markdown(f"**Found {len(songs)} song{'s' if len(songs) != 1 else ''}**")

    for index, song in enumerate(songs, start=1):
        col_track_num, col_track_info = st.columns([0.1, 0.9])

        with col_track_num:
            st.markdown(f'<p class="track-index">{index}</p>', unsafe_allow_html=True)

        with col_track_info:
            st.markdown(f'<p class="track-name">{song.get("name", "Unknown")}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="track-artist">{song.get("artist", "Unknown Artist")}</p>', unsafe_allow_html=True)

            col_preview, col_link = st.columns(2)

            with col_preview:
                if song.get("preview_url"):
                    st.audio(song.get("preview_url"))
                else:
                    st.info("No preview available")

            with col_link:
                if song.get("spotify_url"):
                    st.markdown(
                        f'<a href="{song.get("spotify_url")}" target="_blank" style="background-color: #1DB954; color: white; padding: 0.5rem 1rem; border-radius: 20px; text-decoration: none; display: inline-block; font-weight: 600;">🎵 Open in Spotify</a>',
                        unsafe_allow_html=True
                    )

            st.divider()


# Sidebar
with st.sidebar:
    st.markdown('<p style="text-align: center; font-size: 1.2rem; font-weight: 700; color: #1DB954; margin-bottom: 1rem;">⚙️ Settings & Info</p>', unsafe_allow_html=True)

    with st.expander("ℹ️ About This App", expanded=True):
        st.markdown("""
        **Mood-to-Spotify** is a Python app that turns a mood description into Spotify track recommendations.
        
        It:
        - Uses **OpenAI** to extract emotions from your mood description
        - Uses **Spotify API** to find matching tracks
        - Presents results with previews and direct Spotify links
        
        **Current Settings:**
        - Platform: Streamlit
        - Backend: Flask/Python
        """)

    with st.expander("📋 How It Works"):
        st.markdown("""
        1. **Describe your mood** - Write how you're feeling in natural language
        2. **Select options** - Choose track count and Spotify market
        3. **Get recommendations** - AI processes your mood and finds matching tracks
        4. **Enjoy music** - Preview tracks or open directly in Spotify
        """)

    with st.expander("🔧 Requirements"):
        st.markdown("""
        - Python 3.10+
        - OpenAI API key
        - Spotify app credentials
        
        Set environment variables:
        ```
        OPENAI_API_KEY
        SPOTIFY_CLIENT_ID
        SPOTIFY_CLIENT_SECRET
        ```
        """)

    with st.expander("🎨 UI Features"):
        st.markdown("""
        ✨ Beautiful dark theme
        🎵 Spotify green accents
        🎯 Intuitive controls
        📱 Fully responsive
        ⚡ Real-time feedback
        """)

    st.divider()

    st.markdown("""
    <div style="text-align: center; color: #b3b3b3; font-size: 0.9rem; margin-top: 2rem;">
        <p>🎧 Made with Streamlit</p>
        <p>Connect your mood to music</p>
    </div>
    """, unsafe_allow_html=True)


