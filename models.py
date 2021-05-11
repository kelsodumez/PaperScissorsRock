'''
CLASSES FOR DATABASE BELOW
these tell SQLAlchemy how to take the data from Go.db and make it useable in Python
'''
from flask import Flask, render_template, session, redirect, url_for, request, Blueprint, flash
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, Column, Integer

def models():
    class game(db.Model):
        __tablename__ = 'game'
        gameId = db.Column(db.Integer, primary_key = True)
        user1Id = db.Column(db.ForeignKey('user to game.user'))
        user2Id = db.Column(db.ForeignKey('user to game.user'))
        user1Prisoners = db.Column(db.Integer)
        # add relationship between User1/2Id and UTG

    class user(db.Model):
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

    user_to_game = db.table("user to game", db.Model.metadata,
                    db.Column("utgId", db.Integer, primary_key = True),
                    db.Column("user", db.Integer, db.ForeignKey("user.userId")),
                    db.Column("game", db.Integer, db.ForeignKey("game.gameId")))

    class user_to_game(db.Model):
        utgId = db.Column(db.Integer, primary_key = True)
        user = db.Column(db.Integer, db.ForeignKey("user.userId"))
        game = db.Column(db.Integer, db.ForeignKey("game.gameId"))
