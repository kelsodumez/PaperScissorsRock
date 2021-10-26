'''
Kelso du Mez
3/05/2021 - (date when finished)
SQLAlchemy PSR Website
git config --global user.email "17232@burnside.school.nz" 
git config --global user.name "kelsodumez"
'''
from flask import Flask, render_template, session, redirect, url_for, request, Blueprint, flash
from random import randint, choice
from flask_sqlalchemy import SQLAlchemy, model
from sqlalchemy import DateTime, Column, Integer, update
import sqlalchemy
from sqlalchemy.sql.expression import delete
from sqlalchemy.sql.functions import user
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
    users = (models.users.query.order_by(models.users.gamesWon.desc()).all()) # all users ordered by games won in descending order
    length = len(users)
    upper_split = int((length/100) * 20)
    lower_split = int((length/100) * 70)

    upper_quart = users[:(upper_split)]
    middle_quart = users[(upper_split):(lower_split)]
    lower_quart = users[(lower_split):]
    print(upper_quart, middle_quart, lower_quart)

    for user in upper_quart:
        upper_user = models.user_to_picture.query.filter(models.user_to_picture.userId == user.userId).first()
        upper_user.pictureId = 1

    for user in middle_quart:
        middle_user = models.user_to_picture.query.filter(models.user_to_picture.userId == user.userId).first()
        middle_user.pictureId = 2

    for user in lower_quart:
        lower_user = models.user_to_picture.query.filter(models.user_to_picture.userId == user.userId).first()
        lower_user.pictureId = 3      

    db.session.commit()
    user_ranks = models.user_to_picture.query.all()
    gold_image = models.rank_pictures.query.filter(models.rank_pictures.pictureId == 1).first()
    silver_image = models.rank_pictures.query.filter(models.rank_pictures.pictureId == 2).first()
    bronze_image = models.rank_pictures.query.filter(models.rank_pictures.pictureId == 3).first()
    return render_template('home.html', users=users, user_ranks=user_ranks, gold_image=gold_image, silver_image=silver_image, bronze_image=bronze_image)

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

            user_added = models.users.query.filter(models.users.username == request.form.get('username')).first()

            utp_info = models.user_to_picture (
                userId = user_added.userId
                )
            db.session.add(utp_info)
            db.session.commit()
    return render_template('createaccount.html')

@app.route('/play')
def play():  
    users=models.users.query.all()
    if current_user():
        current_username = current_user().username
        return render_template('play.html', users=users, current_username=current_username)
    else:
        return render_template('play.html')


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
    print(current_user().username) # for some reason this print statement fixes a bug caused by current_user().username in the following line, i have no idea why lol
    game_to_add = models.game.query.filter_by(username1 = user_sent['user'], username2 = current_user().username).first()
    p1 = models.users.query.filter_by(username = user_sent['user']).first()
    p2 = models.users.query.filter_by(username = current_user().username).first()

    def p1_win():
        p1.gamesWon += 1
        p2.gamesLost += 1
        delete(models.game).where(models.game == game_to_add)
        db.session.commit()
        data = "win"
        emit('broadcast-result', data, room=p1.sessionId)
        data = "loss"
        emit('broadcast-result', data, room=p2.sessionId)

    def p2_win():
        p1.gamesLost += 1
        p2.gamesWon += 1
        delete(models.game).where(models.game == game_to_add)
        db.session.commit()

    def tie():
        print('aa')

    if game_to_add.move1 == 'rock' and move_chosen == 'rock':
        tie()
    elif game_to_add.move1 == 'rock' and move_chosen == 'paper':
        p2_win()
    elif game_to_add.move1 == 'rock' and move_chosen == 'scissors':
        p1_win()
    elif game_to_add.move1 == 'paper' and move_chosen == 'paper':
        tie()
    elif game_to_add.move1 == 'paper' and move_chosen == 'rock':
        p2_win()
    elif game_to_add.move1 == 'paper' and  move_chosen == 'scissors':
        p1_win()
    elif game_to_add.move1 == 'scissors' and move_chosen == 'scissors':
        tie()
    elif game_to_add.move1 == 'scissors' and move_chosen == 'paper':
        p2_win()
    elif game_to_add.move1 == 'scissors' and move_chosen == 'rock':
        p1_win()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

if __name__ == "__main__": 
    socketio.run(app, debug = True)
    # app.run(debug=True)