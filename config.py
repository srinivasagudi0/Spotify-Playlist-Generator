"""Configuration helpers for the CLI."""

import os


REQUIRED_ENV_VARS = (
    "OPENAI_API_KEY",
    "SPOTIFY_CLIENT_ID",
    "SPOTIFY_CLIENT_SECRET",
)
DEFAULT_OPENAI_MODEL = "gpt-3.5-turbo"


def get_missing_env_vars(env=None):
    """Return the required environment variables that are not set."""
    env = os.environ if env is None else env
    return [name for name in REQUIRED_ENV_VARS if not env.get(name)]


def format_missing_env_error(missing_vars):
    """Format a user-facing configuration error message."""
    joined_names = ", ".join(missing_vars)
    return f"Missing required environment variables: {joined_names}"


def validate_required_env_vars(env=None):
    """Raise a ValueError when required environment variables are missing."""
    missing_vars = get_missing_env_vars(env=env)
    if missing_vars:
        raise ValueError(format_missing_env_error(missing_vars))


def get_openai_model(env=None):
    """Return the configured OpenAI model or the default."""
    env = os.environ if env is None else env
    return env.get("OPENAI_MODEL") or DEFAULT_OPENAI_MODEL
