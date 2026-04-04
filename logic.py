"""Core orchestration and presentation logic for the CLI."""

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
    mood = emotion_dict["mood"].lower().strip()
    extra_words = mood_words.get(mood, mood)
    return " ".join(part for part in (keywords, extra_words) if part).strip()


def recommend_songs(user_input, limit=5, market="US"):
    emotion = convert_to_emotion(user_input)
    query = build_query(emotion)
    songs = search_songs(query, limit=limit, market=market)
    return {
        "query": query,
        "emotion": emotion,
        "songs": songs,
    }


def format_output(result):
    emotion_dict = result["emotion"]
    songs = result["songs"]
    lines = [
        f"Emotion: {emotion_dict['emotion']}",
        f"Mood: {emotion_dict['mood']}",
        f"Keywords: {', '.join(emotion_dict['keywords'])}",
        f"Energy: {emotion_dict['energy']}",
        "",
    ]

    if not songs:
        lines.append("No songs found.")
        return "\n".join(lines)

    lines.append("Spotify Songs:")
    for index, song in enumerate(songs, start=1):
        lines.append(f"{index}. {song['name']} by {song['artist']}")
        if song.get("spotify_url"):
            lines.append(f"   Spotify: {song['spotify_url']}")
        if song.get("preview_url"):
            lines.append(f"   Preview: {song['preview_url']}")

    return "\n".join(lines)
