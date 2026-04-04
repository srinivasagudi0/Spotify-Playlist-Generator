"""Flask UI for the mood-to-Spotify recommender."""

from importlib.metadata import version

from flask import Flask, render_template, request
import werkzeug

from ai import AIError
from logic import recommend_songs
from main import get_market_code, get_recommendation_limit, get_recommendation_text, validate_config
from spotify import SpotifyError


DEFAULT_FORM_DATA = {
    "mood_text": "",
    "limit": "5",
    "market": "US",
}


if not hasattr(werkzeug, "__version__"):
    werkzeug.__version__ = version("werkzeug")


def create_app():
    app = Flask(__name__)

    @app.route("/", methods=["GET", "POST"])
    def index():
        form_data = dict(DEFAULT_FORM_DATA)
        result = None
        feedback = None

        if request.method == "POST":
            action = request.form.get("action", "recommend")
            form_data["mood_text"] = request.form.get("mood_text", "")
            form_data["limit"] = request.form.get("limit", DEFAULT_FORM_DATA["limit"])
            form_data["market"] = request.form.get("market", DEFAULT_FORM_DATA["market"])

            if action == "check-config":
                try:
                    validate_config()
                    feedback = {
                        "kind": "success",
                        "title": "Everything looks ready.",
                        "message": "OpenAI and Spotify are set up on this machine, so you can jump straight into recommendations.",
                    }
                except ValueError as error:
                    feedback = {
                        "kind": "error",
                        "title": "A little setup is still missing.",
                        "message": str(error),
                    }
            else:
                try:
                    validate_config()
                    mood_text = get_recommendation_text(form_data["mood_text"])
                    limit = get_recommendation_limit(form_data["limit"])
                    market = get_market_code(form_data["market"])
                    form_data["mood_text"] = mood_text
                    form_data["limit"] = str(limit)
                    form_data["market"] = market
                    result = recommend_songs(mood_text, limit=limit, market=market)
                    feedback = {
                        "kind": "success",
                        "title": "Found a direction.",
                        "message": "I turned your note into a mood read and a first set of tracks that should fit it.",
                    }
                except ValueError as error:
                    feedback = {
                        "kind": "error",
                        "title": "Need one small fix.",
                        "message": str(error),
                    }
                except AIError as error:
                    feedback = {
                        "kind": "error",
                        "title": "I could not read that mood cleanly.",
                        "message": str(error),
                    }
                except SpotifyError as error:
                    feedback = {
                        "kind": "error",
                        "title": "Spotify would not cooperate.",
                        "message": str(error),
                    }

        return render_template(
            "index.html",
            feedback=feedback,
            form_data=form_data,
            result=result,
        )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=False)
