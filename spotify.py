"""Spotify API helpers for search-based recommendations."""

import base64
import json
import os
import ssl
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import certifi


AUTH_URL = "https://accounts.spotify.com/api/token"
SEARCH_URL = "https://api.spotify.com/v1/search"
USER_AGENT = "MoodMusicCLI/1.0"


class SpotifyError(Exception):
    """Raised when Spotify authentication or search fails."""


def open_url(request):
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    return urlopen(request, context=ssl_context)


def read_error_message(error):
    try:
        message = error.read().decode("utf-8")
    except Exception:
        return str(error)

    try:
        data = json.loads(message)
    except json.JSONDecodeError:
        return message

    if "error_description" in data:
        return data["error_description"]

    if "error" in data and isinstance(data["error"], dict):
        return data["error"].get("message", message)

    return message


def get_access_token(opener=None):
    opener = open_url if opener is None else opener
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise SpotifyError("Missing SPOTIFY_CLIENT_ID or SPOTIFY_CLIENT_SECRET")

    credentials = f"{client_id}:{client_secret}".encode("utf-8")
    encoded_credentials = base64.b64encode(credentials).decode("utf-8")

    request = Request(
        AUTH_URL,
        data=b"grant_type=client_credentials",
        headers={
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": USER_AGENT,
        },
        method="POST",
    )

    try:
        with opener(request) as response:
            data = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        message = read_error_message(error)
        raise SpotifyError(f"Spotify login failed: {message}") from error
    except URLError as error:
        raise SpotifyError(f"Spotify connection failed: {error.reason}") from error

    access_token = data.get("access_token")
    if not access_token:
        raise SpotifyError("Spotify login failed: access token missing from response.")

    return access_token


def search_songs(query, limit=5, market="US", opener=None):
    opener = open_url if opener is None else opener
    search_query = query.strip()
    if not search_query:
        return []

    access_token = get_access_token(opener=opener)
    params = urlencode(
        {
            "q": search_query,
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
            "User-Agent": USER_AGENT,
        },
    )

    try:
        with opener(request) as response:
            data = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        message = read_error_message(error)
        if "Active premium subscription required for the owner of the app" in message:
            raise SpotifyError(
                "Spotify blocked this app. The app owner's Spotify account needs Premium for this Development Mode app."
            ) from error
        raise SpotifyError(f"Spotify search failed: {message}") from error
    except URLError as error:
        raise SpotifyError(f"Spotify connection failed: {error.reason}") from error

    results = []
    for track in data.get("tracks", {}).get("items", []):
        artist_names = ", ".join(
            artist.get("name", "").strip()
            for artist in track.get("artists", [])
            if artist.get("name", "").strip()
        )
        results.append(
            {
                "name": track.get("name") or "Unknown Track",
                "artist": artist_names or "Unknown Artist",
                "preview_url": track.get("preview_url"),
                "spotify_url": track.get("external_urls", {}).get("spotify"),
            }
        )

    return results
