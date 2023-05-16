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
    game = Game.query.all()    

    if game:
        return render_template('warning.html', title='Careful!')
    else: 
        return render_template('numberplayers.html', title='How many players?')
    return render_template('numberplayers.html', title='How many players?')



@app.route('/nametheplayers/<numberplayers>', methods=['GET', 'POST'])
def nametheplayers(numberplayers):
    form = PlayersForm()

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
        return redirect('/score')

    return render_template('nametheplayers.html', title='What are they called?', form=form, numberplayers=numberplayers)


@app.route('/reset')
def reset():
    game = Game.query.all()
    for g in game:
        db.session.delete(g)
    db.session.commit()
    return redirect(url_for('numberplayers'))

@app.route('/score')
def score():
    return render_template('score.html', title='Score')
