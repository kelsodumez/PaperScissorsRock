'''
Kelso du Mez
3/05/2021 - (date when finished)
SQLAlchemy Go Website (hopefully)
'''
from flask import Flask, render_template, session, redirect, url_for, request, Blueprint, flash
from random import randint, choice
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, Column, Integer
import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app) # defines db as sqlalchemy connection to database

import models

@app.route('/')
def home():
    return render_template('home.html')

def current_user(): # function to create a session for user
    if session.get("user"):
        return models.users.query.get(session['user'])
    else:
        return False

@app.context_processor
def add_current_user():
    if session.get('user'): # if there is user session
        return dict(current_user = models.users.query.get(session['user']))
    return dict(current_user = None)


@app.route('/login', methods = ['GET', 'POST']) # TODO this should be in a dropwdown eventually but for minimum viable product is fine
def login():
    if session.get('user'):
        return redirect('/')
    if request.method == 'POST':
        user = models.users.query.filter(models.users.username == request.form.get('username')).first() # checks the username input against database
        if user and check_password_hash(user.password, request.form.get('password')):
            session['user'] = user.userId
            return redirect ('/')
        else:
            return render_template('login.html', error = 'username or password incorrect')
    return render_template('login.html')

@app.route('/logout')
def logout():
    try:
        session.pop('user')
    except:
        return redirect('/login', error = 'not currently logged in')
    return redirect('/')

@app.route('/createaccount', methods = ['GET', 'POST']) 
def createaccount():
    if request.method == 'POST':
        if 5 > len(request.form.get('username')) > 12: # if the length of the inputted username is lesser than 5 and greater than 12 (characters)
            return render_template('createaccount.html', error = 'username must be between 5 and 12 characters') # account will not be created with said username and user is prompted to input a shorter/longer username     
        elif models.users.query.filter(models.users.username == request.form.get('username')).first(): # if the username already exists in the db
            return render_template('createaccount.html', error = 'username already in use') # account will not be created and user is prompted to use a different username
        elif len(request.form.get('password')) < 7: #
            return render_template('createaccount.html', error = 'password must be a minimum of 7 characters') 
        else:
            user_info = models.users (
                username = request.form.get('username'), # takes username from form
                password = generate_password_hash(request.form.get('password'), salt_length = 10), # takes password inputted in form and salts and hashes it for encryption
                gamesWon = 0, gamesLost = 0 
                )
            db.session.add(user_info)
            db.session.commit()
    return render_template('createaccount.html')

@app.route('/lobbies', methods = ['GET', 'POST'])
def lobbies():
    games=models.game.query.all()
    if request.method == 'POST':
        game_info = models.game (
            gameName = request.form.get('lobbyname')
        )
        db.session.add(game_info)
        db.session.commit()
        utg_info = models.user_to_game (
            user = current_user().username,
            game = models.game.query.filter(models.game.gameName == request.form.get('lobbyname')).first().gameId,
            isPlayerOne = True
        )
        db.session.add(utg_info)
        db.session.commit()
    return render_template('lobbies.html', games=games)
'''
@app.route('/leaderboard')
'''
@app.route('/game/<int:gameId>')
def game(gameId):
    game=models.game.query.get(gameId)
    return render_template('game.html', game=game)

if __name__ == "__main__": 
    app.run(debug=True) # runs with debug active so i can tell how bad my code is