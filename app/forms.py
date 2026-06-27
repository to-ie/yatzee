from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange, AnyOf, ValidationError


class PlayersForm(FlaskForm):
    player1 = StringField('Player 1', validators=[DataRequired()])
    player2 = StringField('Player 2', validators=[DataRequired()])
    player3 = StringField('Player 3')
    player4 = StringField('Player 4')
    player5 = StringField('Player 5')
    submit = SubmitField("Let's play!")


def multiple_of(n):
    """Validator: the value (if present) must be a multiple of n."""
    def _check(form, field):
        if field.data is not None and field.data % n != 0:
            raise ValidationError(f'Must be a multiple of {n}.')
    return _check


# Upper section: a score is the count of matching dice times the face value,
# so it is bounded by face*5 and is always a multiple of the face.
def _upper(face):
    return IntegerField(validators=[
        Optional(),
        NumberRange(min=0, max=face * 5),
        multiple_of(face),
    ])


# Lower section uses fixed or sum-bounded values; blank = not scored yet.
def _fixed(*allowed):
    return IntegerField(validators=[Optional(), AnyOf(allowed)])


def _ranged(maximum):
    return IntegerField(validators=[Optional(), NumberRange(min=0, max=maximum)])


class ScoreForm(FlaskForm):
    ones = _upper(1)
    twos = _upper(2)
    threes = _upper(3)
    fours = _upper(4)
    fives = _upper(5)
    sixes = _upper(6)

    threex = _ranged(30)      # three of a kind: sum of all five dice
    fourx = _ranged(30)       # four of a kind: sum of all five dice
    fullhouse = _fixed(0, 25)
    small = _fixed(0, 30)     # small straight
    large = _fixed(0, 40)     # large straight
    yahtzee = _fixed(0, 50)
    chance = _ranged(30)      # sum of all five dice

    submit = SubmitField("Next player")
