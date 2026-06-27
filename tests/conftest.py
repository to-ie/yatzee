"""Shared pytest fixtures.

These are black-box integration tests that drive the app through its HTTP
routes and assert the resulting database state. They are deliberately
independent of the internal data model so they keep passing across the
planned Game -> Player -> Score refactor (they pin *behaviour*, not schema).
"""
import os
import tempfile

import pytest

# Point the app at a throwaway database BEFORE it is imported, since the
# database URI is read from the environment at import time (config.py).
_db_fd, _db_path = tempfile.mkstemp(suffix=".db")
os.environ.setdefault("DATABASE_URL", "sqlite:///" + _db_path)
os.environ.setdefault("SECRET_KEY", "test-secret")

from app import app as flask_app, db as _db  # noqa: E402
from app.models import Player  # noqa: E402

CATEGORIES = [
    "ones", "twos", "threes", "fours", "fives", "sixes",
    "threex", "fourx", "fullhouse", "small", "large", "yahtzee", "chance",
]


@pytest.fixture
def app():
    flask_app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
    with flask_app.app_context():
        _db.drop_all()
        _db.create_all()
        yield flask_app
        _db.session.remove()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def make_game(client):
    """Create a game by submitting player names; returns the response."""
    def _make(names):
        data = {f"player{i + 1}": name for i, name in enumerate(names)}
        data["submit"] = "Let's play!"
        return client.post(f"/nametheplayers/{len(names)}", data=data)
    return _make


@pytest.fixture
def score_turn(client):
    """Submit a score sheet for whoever's turn it currently is.

    Pass categories as keyword args, e.g. score_turn(ones=5, chance=12).
    Unspecified categories are submitted blank (the app treats them as 0).
    """
    def _turn(**fields):
        data = {c: "" for c in CATEGORIES}
        data.update({k: str(v) for k, v in fields.items()})
        data["submit"] = "Next player"
        return client.post("/score", data=data)
    return _turn


@pytest.fixture
def player(app):
    """Reload a player's Score row fresh from the database by playerid."""
    def _get(pid):
        _db.session.expire_all()
        return Player.query.filter_by(playerid=pid).first()
    return _get


@pytest.fixture
def full_sheet():
    """A complete sheet of legal scores (every category filled)."""
    return {
        "ones": 1, "twos": 2, "threes": 3, "fours": 4, "fives": 5, "sixes": 6,
        "threex": 10, "fourx": 12, "fullhouse": 25,
        "small": 30, "large": 40, "yahtzee": 50, "chance": 15,
    }
