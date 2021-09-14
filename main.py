'''
Kelso du Mez
3/05/2021 - (date when finished)
SQLAlchemy Go Website (hopefully)
git config --global user.email "17232@burnside.school.nz" 
git config --global user.name "kelsodumez"
'''
from flask import Flask, render_template, session, redirect, url_for, request, Blueprint, flash
from random import randint, choice
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, Column, Integer, update
import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from config import Config
from flask_socketio import SocketIO, emit, send, join_room, leave_room


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app) # defines db as sqlalchemy connection to database
socketio = SocketIO(app, cors_allowed_origins='*') # defines the socketIO connection
from main import db # this is kind of weird, for some reason it fixes an issue i was having with sessions

import models # imports the models from models.py

@app.route('/')
def home():
    return render_template('home.html')

def current_user(): # function to grab information of current user session
    if session.get("user"): # if a user session is found return the data sorrounding that user
        return models.users.query.get(session['user'])
    else: # otherwise return False
        return False

@app.context_processor
def add_current_user(): # function to create a user session
    if session.get('user'): # if there is user session
        return dict(current_user = models.users.query.get(session['user']))
    return dict(current_user = None)


@app.route('/login', methods = ['GET', 'POST']) 
def login():
    print(session.get('user')) # debug
    if request.method == 'POST': # if POST method then the form data will be compared to whats in the db, user will be logged in if inputted data matches
        user = models.users.query.filter(models.users.username == request.form.get('username')).first() # checks the username input against database
        if user and check_password_hash(user.password, request.form.get('password')):
            session['user'] = user.userId
            return redirect ('/') # redirect to home
        else:
            return render_template('login.html', error = 'username or password incorrect')
    return render_template('login.html')

@app.route('/logout')
def logout():
    try:
        session.pop('user') # removes user session
    except: # returns an error if the user tries to type in logout route whilst not logged in
        return redirect('login', error = 'not currently logged in') 
    return redirect('/')

@app.route('/createaccount', methods = ['GET', 'POST']) 
def createaccount():
    if request.method == 'POST':
        if 5 > len(request.form.get('username')) > 12: # if the length of the inputted username is lesser than 5 and greater than 12 (characters)
            return render_template('createaccount.html', error = 'username must be between 5 and 12 characters') # account will not be created with said username and user is prompted to input a shorter/longer username     
        elif models.users.query.filter(models.users.username == request.form.get('username')).first(): # if the username already exists in the db
            return render_template('createaccount.html', error = 'username already in use') # account will not be created and user is prompted to use a different username
        elif len(request.form.get('password')) < 7: # if length of inputted username is less than 7 it will not be accepted
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

@app.route('/play')
def play():  
    # games=models.game.query.all()
    users=models.users.query.all()
    current_username = current_user().username # TODO this causes bool error
    # return render_template('play.html', current_username=current_username, backcheck=True, users=users)#, games=games, users=users)
    return render_template('play.html', users=users, current_username=current_username)

'''
@app.route('/leaderboard')
'''
'''
@app.route('/game/<int:gameId>')
def game(gameId):
    # increase_userNo = models.game.query.filter_by(gameId = gameId).first()    
    # userCreated = models.user_to_game.query.filter_by(game = gameId).first()
    # if current_user().username == userCreated.username:
    #     return render_template('game.html', game=game)
    # else:
    #     # increase_userNo.userNo = increase_userNo.userNo + 1
    #     # db.session.add(increase_userNo)
    #     # db.session.commit()
    #     utg_info = models.user_to_game (
    #         username = current_user().username,
    #         game = gameId,
    #         isPlayerOne = False
    #     )
    #     db.session.add(utg_info)
    #     db.session.commit() 
    # game = models.game.query.get(gameId)    
    return render_template('game.html', game=game)
'''


@socketio.on('join')
def on_join(data):
    user_joined = data['user_joined']
    user = models.users.query.filter(models.users.username == user_joined['user']).first()
    user.sessionId = request.sid
    db.session.commit()

@socketio.on('sendAction')    
def action(data):
    user_chosen = data['form_data'][0] # these take values from the list generated in the js function and assign them to useable variables
    move_chosen = data['form_data'][1]
    user_sent = data['user_sent']
    game_info = models.game(
        username1 = (models.users.query.filter_by(username = user_sent['user']).first()).username,
        move1 = move_chosen,
        username2 = (models.users.query.filter_by(username = user_chosen).first()).username
    )
    db.session.add(game_info)
    db.session.commit()

    chosen_sid = models.users.query.filter_by(username = user_chosen).first()
    data = []
    data.append(move_chosen)
    data.append(user_sent)
    print(data)
    emit('broadcast-choice', data, room=chosen_sid.sessionId) # broadcasts the move chosen to the specific user, TODO change this because i need to do thing differently

@socketio.on('sendResponse')
def response(data):
    user_sent = data['challenger']
    move_chosen = data['move']
    # game_to_add = models.game.query.filter_by(username1 = user_sent, username2 = current_user())
    game_to_add = models.game(username1 = user_sent['user'], username2 = current_user().username, move2 = move_chosen)
    print(game_to_add, 'aaaaa\n\n\n\naaaaaa')
    print('\n\n', game_to_add.move2)
    db.session.add(game_to_add)
    db.session.commit()

if __name__ == "__main__": 
    socketio.run(app, debug = True)
    # app.run(debug=True)