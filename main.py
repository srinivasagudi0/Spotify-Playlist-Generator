"""Interactive CLI entrypoint for the mood-to-Spotify recommender."""

import sys

from ai import AIError
from config import validate_required_env_vars
from logic import format_output, recommend_songs
from spotify import SpotifyError


EXIT_CONFIG = 2
EXIT_AI = 3
EXIT_SPOTIFY = 4

HELP_FLAGS = {"-h", "--help", "help"}
COMMAND_ALIASES = {
    "1": "recommend",
    "recommend": "recommend",
    "rec": "recommend",
    "r": "recommend",
    "2": "check-config",
    "check-config": "check-config",
    "check": "check-config",
    "config": "check-config",
    "3": "exit",
    "exit": "exit",
    "quit": "exit",
    "q": "exit",
}


def parse_limit(value):
    normalized_value = str(value).strip()
    try:
        parsed_value = int(normalized_value)
    except ValueError as error:
        raise ValueError("limit must be an integer between 1 and 10") from error

    if not 1 <= parsed_value <= 10:
        raise ValueError("limit must be between 1 and 10")
    return parsed_value


def print_help():
    print("Mood-to-Spotify CLI")
    print("")
    print("Usage:")
    print("  python3 main.py")
    print("  python3 main.py recommend")
    print("  python3 main.py check-config")
    print("")
    print("The recommend flow is interactive and asks for:")
    print("  - your mood")
    print("  - number of tracks to return (1-10, default 5)")
    print("  - Spotify market code (default US)")


def prompt_input(prompt, default=None):
    suffix = f" [{default}]" if default is not None else ""
    response = input(f"{prompt}{suffix}\n> ")
    return response.strip()


def resolve_command(command):
    normalized_command = str(command).strip().lower()
    resolved_command = COMMAND_ALIASES.get(normalized_command)
    if resolved_command is None:
        raise ValueError("Choose `recommend`, `check-config`, or `exit`.")
    return resolved_command


def prompt_for_command():
    print("Mood-to-Spotify CLI")
    print("1. Recommend songs")
    print("2. Check configuration")
    print("3. Exit")
    return resolve_command(prompt_input("Choose an option"))


def get_recommendation_text(text=None):
    if text is None:
        text = prompt_input("How are you feeling today?")

    normalized_text = text.strip()
    if not normalized_text:
        raise ValueError("Mood text cannot be empty.")
    return normalized_text


def get_recommendation_limit(limit=None):
    if limit is None:
        limit = prompt_input("How many tracks do you want?", default="5") or "5"
    return parse_limit(limit)


def get_market_code(market=None):
    if market is None:
        market = prompt_input("Spotify market code?", default="US") or "US"

    normalized_market = market.strip().upper()
    if not normalized_market:
        return "US"
    return normalized_market


def validate_config():
    validate_required_env_vars()


def run_check_config():
    try:
        validate_config()
    except ValueError as error:
        print(str(error))
        return EXIT_CONFIG

    print("Configuration looks good.")
    return 0


def run_recommend(text=None, limit=None, market=None):
    try:
        validate_config()
        mood_text = get_recommendation_text(text)
        parsed_limit = get_recommendation_limit(limit)
        market_code = get_market_code(market)
        result = recommend_songs(
            mood_text,
            limit=parsed_limit,
            market=market_code,
        )
    except ValueError as error:
        print(str(error))
        return EXIT_CONFIG
    except AIError as error:
        print(str(error))
        return EXIT_AI
    except SpotifyError as error:
        print(str(error))
        return EXIT_SPOTIFY

    print(format_output(result))
    return 0


def validate_recommend_argv(argv):
    if any(argument.startswith("-") for argument in argv[1:]):
        raise ValueError(
            "This CLI is interactive now. Run `python3 main.py recommend` and answer the prompts."
        )

    if len(argv) > 4:
        raise ValueError("Too many arguments. Run `python3 main.py --help` for usage.")


def main(argv=None):
    argv = sys.argv[1:] if argv is None else list(argv)

    try:
        if argv:
            command_token = argv[0]
            if command_token in HELP_FLAGS:
                print_help()
                return 0

            command = resolve_command(command_token)
        else:
            command = prompt_for_command()
    except ValueError as error:
        print(str(error))
        return EXIT_CONFIG

    if command == "exit":
        print("Goodbye.")
        return 0

    if command == "check-config":
        return run_check_config()

    try:
        validate_recommend_argv(argv)
    except ValueError as error:
        print(str(error))
        return EXIT_CONFIG

    text = argv[1] if len(argv) > 1 else None
    limit = argv[2] if len(argv) > 2 else None
    market = argv[3] if len(argv) > 3 else None
    return run_recommend(text=text, limit=limit, market=market)


if __name__ == "__main__":
    raise SystemExit(main())
