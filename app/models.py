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

    ones = db.Column(db.Integer(), index=True)
    twos = db.Column(db.Integer(), index=True)
    threes = db.Column(db.Integer(), index=True)
    fours = db.Column(db.Integer(), index=True)
    fives = db.Column(db.Integer(), index=True)
    sixed = db.Column(db.Integer(), index=True)
    subtotalupper = db.Column(db.Integer(), index=True)
    bonus = db.Column(db.Integer(), index=True, default=0)
    totaluppersection = db.Column(db.Integer(), index=True)

    threex = db.Column(db.Integer(), index=True)
    fourx = db.Column(db.Integer(), index=True)
    fullhouse = db.Column(db.Integer(), index=True)
    small = db.Column(db.Integer(), index=True)
    large = db.Column(db.Integer(), index=True)
    yahtzee = db.Column(db.Integer(), index=True)
    chance = db.Column(db.Integer(), index=True)
    totallower = db.Column(db.Integer(), index=True)
    bonus = db.Column(db.Integer(), index=True, default=0)
    
    total = db.Column(db.Integer(), index=True)




    def __repr__(self):
        return ''.format(self.id)
