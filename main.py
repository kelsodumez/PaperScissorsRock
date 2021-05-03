from flask import Flask, render_template, session, redirect, url_for, request, Blueprint, flash
from random import randint, choice
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, Column, Integer
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = (f'sqlite:///{(os.path.join(project_dir, "Go.db"))}')
app = Flask(__name__)
app.secret_key = ('visualstudiocodebest') # replace with real secret key
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app) # defines db as sqlalchemy connection to database

'''
CLASSES FOR DATABASE BELOW
these tell SQLAlchemy how to take the data from Go.db and make it useable in Python
'''
class game(db.Model):
    __tablename__ = 'game'
    gameId = db.Column(db.Integer, primary_key=True)
    user1Id = db.Column(db.ForeignKey('user to game.user'))
    user2Id = db.Column(db.ForeignKey('user to game.user'))
    user1Prisoners = db.Column(db.Integer)
    # add relationship between User1/2Id and UTG

class user(db.Model):
    __tablename__ = 'user'
    userId = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    gamesWon = db.Column(db.Integer)
    gamesLost = db.Column(db.Integer)

class user_to_game(db.Model):
    __tablename__ = 'user to game'
    utgId = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.ForeignKey('user.userId'))
    game = db.Column(db.ForeignKey('game.'))