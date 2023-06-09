from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class PlayersForm(FlaskForm):
    player1 = StringField('Player 1', validators=[DataRequired()])
    player2 = StringField('Player 2', validators=[DataRequired()])
    player3 = StringField('Player 3')
    player4 = StringField('Player 4')
    player5 = StringField('Player 5')
    submit = SubmitField("Let's play!")


class ScoreForm(FlaskForm):
    ones = StringField()
    twos = StringField()
    threes = StringField()
    fours = StringField()
    fives = StringField()
    sixes = StringField()

    threex = StringField()
    fourx = StringField()
    fullhouse = StringField()
    small = StringField()
    large = StringField()
    yahtzee = StringField()
    chance = StringField()

    submit = SubmitField("Next player")
