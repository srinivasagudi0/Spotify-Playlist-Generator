import streamlit as st

from ai import AIError
from logic import recommend_songs
from main import get_market_code, get_recommendation_limit, get_recommendation_text, validate_config
from spotify import SpotifyError


st.title("Spotify Playlist Generator")
st.set_page_config(page_title="Spotify Playlist Generator", page_icon="🎵", layout="wide")

mood_text = st.selectbox("How are you feeling?", ["Happy", "Sad", "Energetic", "Relaxed", "Calm", "Excited", "Joyful", "Content", "Peaceful", "Hopeful", "Optimistic", "Grateful", "Inspired", "Confident", "Playful", "Cheerful", "Proud", "Amused", "Loved", "Affectionate", "Romantic", "Passionate", "Curious", "Focused", "Motivated", "Determined", "Empowered", "Free", "Adventurous", "Nostalgic", "Dreamy", "Reflective", "Melancholic", "Lonely", "Heartbroken", "Anxious", "Nervous", "Stressed", "Overwhelmed", "Restless", "Confused", "Frustrated", "Angry", "Annoyed", "Irritated", "Jealous", "Guilty", "Ashamed", "Embarrassed", "Disappointed", "Hopeless", "Tired", "Exhausted", "Burned Out", "Sleepy", "Bored", "Empty", "Detached", "Numb", "Sensitive", "Vulnerable", "Tender", "Comforted", "Safe", "Secure", "Satisfied", "Relieved", "Surprised", "Shocked", "Fearful", "Scared", "Panicked", "Bold", "Wild", "Uplifted", "Balanced", "Grounded", "Zen", "Moody", "Dark", "Brooding", "Intense", "Aggressive", "Fiery", "Soft", "Warm", "Cozy", "Chill", "Cool", "Smooth", "Silly", "Goofy", "Whimsical", "Flirty", "Sensual", "Yearning", "Miserable", "Defeated", "Resentful", "Distracted", "Apathetic", "Drained", "Awkward", "Restored", "Rejuvenated", "Alive", "Electric", "Euphoric", "Blissful", "Serene"])
limit = st.number_input("Number of tracks", min_value=1, max_value=10, value=5, step=1)
market = "US"  # Dont need to be very technical for users, so we can just default to US market for now

if st.button("Generate Playlist"):
    try:
        validate_config()
        st.write("Getting suggestions...")
        mood_text = get_recommendation_text(mood_text)
        limit = get_recommendation_limit(limit)
        market = get_market_code(market)
        result = recommend_songs(mood_text, limit=limit, market=market)

        st.write("Emotion:", result["emotion"]["emotion"])
        st.write("Mood:", result["emotion"]["mood"])
        st.write("Keywords:", ", ".join(result["emotion"]["keywords"]))
        st.write("Energy:", result["emotion"]["energy"])

        st.write("Songs:")
        for song in result["songs"]:
            st.write(f"- {song['name']} by {song['artist']}")
            if song.get("spotify_url"):
                st.markdown(f"[Open in Spotify]({song['spotify_url']})")
    except ValueError as error:
        st.error(str(error))
    except AIError as error:
        st.error(str(error))
    except SpotifyError as error:
        st.error(str(error))
