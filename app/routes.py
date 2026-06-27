from app import app, db
from flask import render_template, redirect, url_for, request, flash
from app.forms import PlayersForm, ScoreForm
from app.models import Game, Player, CATEGORIES


def current_game():
    """The single active game (the app supports one at a time)."""
    return Game.query.first()


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
        game = Game(numberofplayers=count, nextplayer=1)
        db.session.add(game)
        db.session.flush()   # assign game.id before adding players

        names = [form.player1.data, form.player2.data, form.player3.data,
                 form.player4.data, form.player5.data]
        for i in range(count):
            db.session.add(Player(game_id=game.id, playerid=i + 1, name=names[i]))
        db.session.commit()

        return redirect(url_for('score'))

    return render_template('nametheplayers.html', title='What are they called?',
                           form=form, numberplayers=numberplayers)


@app.route('/reset')
def reset():
    for game in Game.query.all():
        db.session.delete(game)   # cascade removes the players
    db.session.commit()
    return redirect(url_for('numberplayers'))


@app.route('/score', methods=['GET', 'POST'])
def score():
    game = current_game()
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
        for c in CATEGORIES:
            setattr(currentplayer, c, getattr(form, c).data)

        # advance to the next player, wrapping around
        game.nextplayer = game.nextplayer + 1
        if game.nextplayer > game.numberofplayers:
            game.nextplayer = 1

        db.session.commit()
        return redirect(url_for('score'))

    elif request.method == 'POST':
        flash('Some scores were invalid — please check the highlighted boxes.')

    return render_template('score.html', title='Score', form=form,
                           currentplayer=currentplayer, players=players)


@app.route('/pause')
def pause():
    return redirect(url_for('index'))


@app.route('/end')
def end():
    game = current_game()
    players = game.players
    winnerscore = max((p.total for p in players), default=0)
    return render_template('end.html', players=players, winnerscore=winnerscore)
