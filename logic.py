"""
brain pipeline

FLow:
input -> ai -> keywords -> spotify -> results -> format output
"""


import json
from ai import convert_to_emotion
from spotify import search_songs


def build_query(emotion_dict):
    mood_words = {
        "safe": "calm relaxing ambient",
        "calm": "calm relaxing ambient",
        "happy": "happy upbeat feel good",
        "sad": "sad mellow acoustic",
        "angry": "intense rock energy",
        "romantic": "romantic love soft",
    }

    keywords = " ".join(emotion_dict["keywords"])
    mood = emotion_dict["mood"].lower()
    extra_words = mood_words.get(mood, mood)
    return f"{keywords} {extra_words}".strip()


def process_input(user_input):
    emotion = convert_to_emotion(user_input)
    songs = []
    spotify_error = None

    try:
        songs = search_query(emotion)
    except ValueError as error:
        spotify_error = str(error)

    return {
        "emotion": json.loads(emotion),
        "songs": songs,
        "spotify_error": spotify_error,
    }


# this below funtion converts the JSON into a more user friendly format, this is just for demonstration, we can directly use the JSON response from the ai and pass it to spotify to get the results, but for now we will just format the output in a more user friendly way.
def format_output(result):
    emotion_dict = result["emotion"]
    songs = result["songs"]
    spotify_error = result["spotify_error"]

    formatted_output = (
        f"Emotion: {emotion_dict['emotion']}\n"
        f"Mood: {emotion_dict['mood']}\n"
        f"Keywords: {', '.join(emotion_dict['keywords'])}\n"
        f"Energy: {emotion_dict['energy']}\n\n"
        f"Spotify Songs:\n"
    )

    if not songs:
        if spotify_error:
            formatted_output += f"Spotify error: {spotify_error}"
        else:
            formatted_output += "No songs found."
        return formatted_output

    for song in songs:
        preview = song["preview_url"] or "No preview available"
        formatted_output += (
            f"- {song['name']} by {song['artist']}\n"
            f"  Preview: {preview}\n"
        )

    return formatted_output

def search_query(result):
    emotion_dict = json.loads(result)
    query = build_query(emotion_dict)
    songs = search_songs(query, 5)
    return songs
