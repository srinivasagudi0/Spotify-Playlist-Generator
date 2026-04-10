# Mood-to-Spotify CLI

A local Python app that turns a mood description into Spotify track recommendations. The repository now contains only the core logic and the interactive CLI. All UI layers were removed.

## Requirements

- Python 3.10+
- An OpenAI API key
- Spotify app credentials with access to the Search API

## Install

```bash
python3 -m pip install -r requirements.txt
```

## Environment Variables

Set these in your shell before running the CLI:

```bash
export OPENAI_API_KEY="your-openai-key"
export SPOTIFY_CLIENT_ID="your-spotify-client-id"
export SPOTIFY_CLIENT_SECRET="your-spotify-client-secret"
```

Optional:

```bash
export OPENAI_MODEL="gpt-3.5-turbo"
```

The CLI does not load a `.env` file in this milestone.

## CLI

Start the interactive CLI:

```bash
python3 main.py
```

You can also jump straight into a flow:

```bash
python3 main.py recommend
python3 main.py check-config
```

The `recommend` flow asks for the mood, track limit, and market in the terminal instead of using `argparse` flags.

Show help:

```bash
python3 main.py --help
```

## Output

Successful recommendations print:

- detected emotion
- mood
- keywords
- energy
- numbered Spotify tracks
- Spotify URL for each track
- preview URL when Spotify provides one

If Spotify returns no matching tracks, the CLI prints `No songs found.` and exits successfully.

## Exit Codes

- `0`: success
- `2`: missing configuration or invalid CLI input
- `3`: OpenAI response or request failure
- `4`: Spotify auth, network, or search failure

## Troubleshooting

`Missing required environment variables`

- One or more required env vars are unset.
- Run `python3 main.py check-config` to confirm which names are missing.

`OpenAI returned invalid JSON`

- The model response did not match the required emotion schema.
- Retry the command or set `OPENAI_MODEL` explicitly if you want to test a different model.

`Spotify login failed`

- Your Spotify client ID or client secret is missing or incorrect.
- Recheck the values you exported in your shell.

`Spotify blocked this app`

- The current Spotify app/account setup is not allowed to perform this request in Development Mode.

## Tests

Run the full test suite with:

```bash
python3 -m unittest discover -s tests -v
```
