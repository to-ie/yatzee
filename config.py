import os
import secrets
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # Set SECRET_KEY in the environment for production (a stable value keeps
    # sessions/CSRF tokens valid across restarts). With none set we fall back
    # to a random per-process key — fine for local dev, and never a secret
    # committed to source.
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)

    # Managed Postgres providers (Render, Heroku) hand out a "postgres://" URL,
    # but SQLAlchemy 2.x only accepts the "postgresql://" scheme.
    _database_url = os.environ.get('DATABASE_URL')
    if _database_url and _database_url.startswith('postgres://'):
        _database_url = _database_url.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = _database_url or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False