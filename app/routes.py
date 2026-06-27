import secrets

from app import app, db
from flask import render_template, redirect, url_for, request, flash, session
from app.forms import PlayersForm, ScoreForm, JoinForm
from app.models import Game, Player, CATEGORIES

# Alphabet for join codes: no 0/O/1/I to avoid confusion when read aloud.
CODE_ALPHABET = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
CODE_LENGTH = 4


def new_game_code():
    """A short code that isn't already in use."""
    while True:
        code = ''.join(secrets.choice(CODE_ALPHABET) for _ in range(CODE_LENGTH))
        if Game.query.filter_by(code=code).first() is None:
            return code


def current_game():
    """The game belonging to this browser session, or None.

    The session cookie stores the game id for convenient auto-resume; a game
    can also be opened from any browser via its shareable code (see /join).
    """
    game_id = session.get('game_id')
    if game_id is None:
        return None
    return db.session.get(Game, game_id)


def join_game(game):
    """Adopt a game into this session (so it auto-resumes here)."""
    session['game_id'] = game.id
    session.permanent = True


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/numberplayers')
def numberplayers():
    if current_game():
        return render_template('warning.html', title='Careful!')
    return render_template('numberplayers.html', title='How many players?')


@app.route('/nametheplayers/<numberplayers>', methods=['GET', 'POST'])
def nametheplayers(numberplayers):
    form = PlayersForm()

    if form.validate_on_submit():
        count = int(numberplayers)
        game = Game(numberofplayers=count, nextplayer=1, code=new_game_code())
        db.session.add(game)
        db.session.flush()   # assign game.id before adding players

        names = [form.player1.data, form.player2.data, form.player3.data,
                 form.player4.data, form.player5.data]
        for i in range(count):
            db.session.add(Player(game_id=game.id, playerid=i + 1, name=names[i]))
        db.session.commit()

        join_game(game)   # remember this game for the rest of the session
        return redirect(url_for('score'))

    return render_template('nametheplayers.html', title='What are they called?',
                           form=form, numberplayers=numberplayers)


@app.route('/g/<code>')
def join_by_link(code):
    game = Game.query.filter_by(code=code.upper()).first()
    if game is None:
        flash('No game found with that code.')
        return redirect(url_for('join'))
    join_game(game)
    return redirect(url_for('score'))


@app.route('/join', methods=['GET', 'POST'])
def join():
    form = JoinForm()
    if form.validate_on_submit():
        return redirect(url_for('join_by_link', code=form.code.data.strip().upper()))
    return render_template('join.html', title='Join a game', form=form)


@app.route('/reset')
def reset():
    game = current_game()
    if game:
        db.session.delete(game)   # cascade removes the players
        db.session.commit()
    session.pop('game_id', None)
    return redirect(url_for('numberplayers'))


@app.route('/score', methods=['GET', 'POST'])
def score():
    game = current_game()
    if game is None:
        return redirect(url_for('index'))
    players = game.players
    currentplayer = next(p for p in players if p.playerid == game.nextplayer)

    # end of game once every player has filled their card
    if all(p.full for p in players):
        return redirect(url_for('end'))

    form = ScoreForm()

    if request.method == 'GET':
        for c in CATEGORIES:
            getattr(form, c).data = getattr(currentplayer, c)

    elif form.validate_on_submit():
        # Only write categories that were actually filled in, so a blank box
        # never wipes a score entered on an earlier turn.
        for c in CATEGORIES:
            value = getattr(form, c).data
            if value is not None:
                setattr(currentplayer, c, value)

        # advance to the next player, wrapping around
        game.nextplayer = game.nextplayer + 1
        if game.nextplayer > game.numberofplayers:
            game.nextplayer = 1

        db.session.commit()
        return redirect(url_for('score'))

    elif request.method == 'POST':
        flash('Some scores were invalid — please check the highlighted boxes.')

    return render_template('score.html', title='Score', form=form,
                           currentplayer=currentplayer, players=players,
                           game=game)


@app.route('/pause')
def pause():
    return redirect(url_for('index'))


@app.route('/end')
def end():
    game = current_game()
    if game is None:
        return redirect(url_for('index'))
    players = game.players
    winnerscore = max((p.total for p in players), default=0)
    return render_template('end.html', players=players, winnerscore=winnerscore)
