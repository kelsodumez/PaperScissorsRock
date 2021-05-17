'''
CLASSES FOR DATABASE BELOW
these tell SQLAlchemy how to take the data from Go.db and make it useable in Python
'''
from main import db

class game(db.Model):
    __tablename__ = 'game'
    gameId = db.Column(db.Integer, primary_key = True)
    gameName = db.Column(db.String)
    user1Id = db.Column(db.ForeignKey('user to game.user'))
    user2Id = db.Column(db.ForeignKey('user to game.user'))
    user1Prisoners = db.Column(db.Integer)
    user2Prisoners = db.Column(db.Integer)

class users(db.Model):
    __tablename__ = 'user'
    userId = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    gamesWon = db.Column(db.Integer)
    gamesLost = db.Column(db.Integer)

class piece(db.Model):
    __tablename__ = 'piece'
    pieceId = db.Column(db.Integer, primary_key = True)
    coordX = db.Column(db.Integer)
    coordY = db.Column(db.Integer)

class user_to_game(db.Model):
    __tablename__ = 'user to game'
    utgId = db.Column(db.Integer, primary_key = True)
    user = db.Column(db.Integer, db.ForeignKey('user.userId'))
    game = db.Column(db.Integer, db.ForeignKey('game.gameId'))

class piece_to_game(db.Model):
    __tablename__ = 'piece to game'
    ptgId = db.Column(db.Integer, primary_key = True)
    piece = db.Column(db.Integer, db.ForeignKey('piece.pieceId'))
    game = db.Column(db.Integer, db.ForeignKey('game.gameId'))
