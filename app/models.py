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
    name = db.Column(db.String(64), index=True, unique=True)
    

    def __repr__(self):
        return ''.format(self.id)
