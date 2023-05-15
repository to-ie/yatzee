from app import app, db
from flask import render_template, flash, redirect, url_for
from app.forms import PlayersForm
from app.models import Game, Score

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/numberplayers')
def numberplayers():
    game = Game.query.first()
    print(game)
    # TODO: Serve warning if other game is in progress
    # if game:
    #     # warning
    #     return render_template('numberplayers.html', title='How many players?', numberplayers=numberplayers)
    # else: 
    #     return render_template('warning.html', title='Careful!')
    return render_template('numberplayers.html', title='How many players?', numberplayers=numberplayers)



@app.route('/nametheplayers/<numberplayers>', methods=['GET', 'POST'])
def nametheplayers(numberplayers):
    form = PlayersForm()
    # Write the number of players in the db

    if form.validate_on_submit():
        game = Game(
            numberofplayers=numberplayers,
            playerone = form.player1.data,
            playertwo = form.player2.data,
            playerthree = form.player3.data,
            playerfour = form.player4.data,
            playerfive = form.player5.data)
        db.session.add(game)
        db.session.commit()
        return redirect('/index')

    # TODO: Clear the Game db when this works
    return render_template('nametheplayers.html', title='What are they called?', form=form, numberplayers=numberplayers)


@app.route('/erase')
def erasegame():
    # clear the game db.
    game = Game.query.all()
    for g in game:
        db.session.delete(g)
    db.session.commit()
    return redirect(url_for('numberplayers'))

