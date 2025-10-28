from app import db

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numberofplayers = db.Column(db.Integer(), index=True)
    nextplayer = db.Column(db.Integer(), index=True, default=1)
    playerone = db.Column(db.String(64), index=True, unique=True)
    playertwo = db.Column(db.String(64), index=True, unique=True)
    playerthree = db.Column(db.String(64), index=True, unique=True)
    playerfour = db.Column(db.String(64), index=True, unique=True)
    playerfive = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return ''.format(self.id)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(64), index=True)
    playerid = db.Column(db.Integer(), index=True)

    ones = db.Column(db.String(64), index=True)
    twos = db.Column(db.String(64), index=True)
    threes = db.Column(db.String(64), index=True)
    fours = db.Column(db.String(64), index=True)
    fives = db.Column(db.String(64), index=True)
    sixes = db.Column(db.String(64), index=True)
    subtotalupper = db.Column(db.Integer(), index=True, default=0)
    bonus = db.Column(db.Integer(), index=True, default=0)
    totaluppersection = db.Column(db.Integer(), index=True)

    threex = db.Column(db.String(64), index=True)
    fourx = db.Column(db.String(64), index=True)
    fullhouse = db.Column(db.String(64), index=True)
    small = db.Column(db.String(64), index=True)
    large = db.Column(db.String(64), index=True)
    yahtzee = db.Column(db.String(64), index=True)
    chance = db.Column(db.String(64), index=True)
    totallower = db.Column(db.Integer(), index=True)
    
    full = db.Column(db.String(64), index=True, default='no')

    total = db.Column(db.Integer(), index=True)

    def __repr__(self):
        return ''.format(self.id)
