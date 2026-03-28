"""
Handles Spotify API 

Responsible for:
1. Authentication
2. Searching for songs
3. Return:
    a. name
    b. artist
    d. song preview url
"""

import base64
import json
import os
from urllib.parse import urlencode
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


AUTH_URL = "https://accounts.spotify.com/api/token"
SEARCH_URL = "https://api.spotify.com/v1/search"


def read_error_message(error):
    message = error.read().decode("utf-8")

    try:
        data = json.loads(message)
    except json.JSONDecodeError:
        return message

    if "error_description" in data:
        return data["error_description"]

    if "error" in data and isinstance(data["error"], dict):
        return data["error"].get("message", message)

    return message


def get_access_token():
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise ValueError("Missing SPOTIFY_CLIENT_ID or SPOTIFY_CLIENT_SECRET")

    credentials = f"{client_id}:{client_secret}".encode("utf-8")
    encoded_credentials = base64.b64encode(credentials).decode("utf-8")

    request = Request(
        AUTH_URL,
        data=b"grant_type=client_credentials",
        headers={
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "MoodMusicApp/1.0",
        },
        method="POST",
    )

    try:
        with urlopen(request) as response:
            data = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        message = read_error_message(error)
        raise ValueError(f"Spotify login failed: {message}")
    except URLError as error:
        raise ValueError(f"Spotify connection failed: {error.reason}")

    return data["access_token"]


def search_songs(query, limit=5, market="US"):
    access_token = get_access_token()
    params = urlencode(
        {
            "q": query,
            "type": "track",
            "limit": limit,
            "market": market,
        }
    )

    request = Request(
        f"{SEARCH_URL}?{params}",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
            "User-Agent": "MoodMusicApp/1.0",
        },
    )

    try:
        with urlopen(request) as response:
            data = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        message = read_error_message(error)
        if "Active premium subscription required for the owner of the app" in message:
            raise ValueError(
                "Spotify blocked this app. The app owner's Spotify account needs Premium for this Development Mode app."
            )
        raise ValueError(f"Spotify search failed: {message}")
    except URLError as error:
        raise ValueError(f"Spotify connection failed: {error.reason}")

    results = []
    for track in data.get("tracks", {}).get("items", []):
        results.append(
            {
                "name": track["name"],
                "artist": ", ".join(artist["name"] for artist in track["artists"]),
                "preview_url": track["preview_url"],
            }
        )

    return results
