from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import PlayersForm

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/numberplayers')
def numberplayers():
    return render_template('numberplayers.html', title='How many players?')

@app.route('/nametheplayers')
def nametheplayers():
    form = PlayersForm()
    # if form.validate_on_submit():
    #     # ...
    #     return redirect('/index')
    return render_template('nametheplayers.html', title='What are they called?', form=form)



