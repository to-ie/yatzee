from app import db

# Score categories, grouped by section. Routes and templates iterate these
# instead of hardcoding the 13 fields in several places.
UPPER = ['ones', 'twos', 'threes', 'fours', 'fives', 'sixes']
LOWER = ['threex', 'fourx', 'fullhouse', 'small', 'large', 'yahtzee', 'chance']
CATEGORIES = UPPER + LOWER

UPPER_BONUS_THRESHOLD = 63   # upper subtotal that earns the bonus
UPPER_BONUS = 35


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(8), unique=True, index=True)  # shareable join code
    numberofplayers = db.Column(db.Integer)
    nextplayer = db.Column(db.Integer, default=1)

    players = db.relationship(
        'Player',
        backref='game',
        cascade='all, delete-orphan',
        order_by='Player.playerid',
    )

    def __repr__(self):
        return f'<Game {self.id}>'


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    playerid = db.Column(db.Integer, index=True)   # turn order within the game
    name = db.Column(db.String(64))

    # Category scores. NULL means "not entered yet" (distinct from a scored 0).
    ones = db.Column(db.Integer)
    twos = db.Column(db.Integer)
    threes = db.Column(db.Integer)
    fours = db.Column(db.Integer)
    fives = db.Column(db.Integer)
    sixes = db.Column(db.Integer)

    threex = db.Column(db.Integer)
    fourx = db.Column(db.Integer)
    fullhouse = db.Column(db.Integer)
    small = db.Column(db.Integer)
    large = db.Column(db.Integer)
    yahtzee = db.Column(db.Integer)
    chance = db.Column(db.Integer)

    # Totals are derived from the category scores, so they are always current
    # (this is what fixes the old "totals don't update in real time" bug).
    @property
    def subtotalupper(self):
        return sum(getattr(self, c) or 0 for c in UPPER)

    @property
    def bonus(self):
        return UPPER_BONUS if self.subtotalupper >= UPPER_BONUS_THRESHOLD else 0

    @property
    def totallower(self):
        return sum(getattr(self, c) or 0 for c in LOWER)

    @property
    def total(self):
        return self.subtotalupper + self.bonus + self.totallower

    @property
    def full(self):
        """True once every category has been filled in."""
        return all(getattr(self, c) is not None for c in CATEGORIES)

    def __repr__(self):
        return f'<Player {self.playerid} {self.name!r}>'
