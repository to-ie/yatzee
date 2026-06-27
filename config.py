import os
import secrets
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # Set SECRET_KEY in the environment for production (a stable value keeps
    # sessions/CSRF tokens valid across restarts). With none set we fall back
    # to a random per-process key — fine for local dev, and never a secret
    # committed to source.
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False