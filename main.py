'''
Kelso du Mez
3/05/2021 - 29/10/2021
SQLAlchemy PSR Website
git config --global user.email '17232@burnside.school.nz'
git config --global user.name 'kelsodumez'
'''
import models  # imports the models from models.py
from flask import Flask, render_template, session, redirect, url_for, request, Blueprint, flash
from random import randint, choice
from flask_sqlalchemy import SQLAlchemy, model
from sqlalchemy import DateTime, Column, Integer, update
import sqlalchemy
from sqlalchemy.sql.expression import delete
from sqlalchemy.sql.functions import user
from sqlalchemy.sql.sqltypes import NullType
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from config import Config
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from forms import LoginForm

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins='*')
from main import db

@app.route('/')
def home():
    # all users ordered by games won in descending order
    users = models.users.query.order_by(models.users.gamesWon.desc()).all()
    length = len(users)

    upper_split = int((length / 100) * 20)
    lower_split = int((length / 100) * 70)

    upper_quart = users[:(upper_split)]
    middle_quart = users[(upper_split):(lower_split)]
    lower_quart = users[(lower_split):]

    for user in lower_quart:
        lower_user = models.users.query.filter(
            models.users.userId == user.userId).first()
        lower_user.pictureId = 3

    for user in middle_quart:
        middle_user = models.users.query.filter(
            models.users.userId == user.userId).first()
        middle_user.pictureId = 2

    for user in upper_quart:
        upper_user = models.users.query.filter(
            models.users.userId == user.userId).first()
        upper_user.pictureId = 1

    gold_image = models.rank_pictures.query.filter(
        models.rank_pictures.pictureId == 1).first()
    silver_image = models.rank_pictures.query.filter(
        models.rank_pictures.pictureId == 2).first()
    bronze_image = models.rank_pictures.query.filter(
        models.rank_pictures.pictureId == 3).first()

    games = models.game.query.order_by(models.game.gameId.desc()).all()
    dated_games = games[10:]

    for game in dated_games:
        db.session.delete(
            models.game.query.filter(
                models.game.gameId == game.gameId).first())

    db.session.commit()

    games = models.game.query.order_by(models.game.gameId.desc()).all()

    return render_template(
        'home.html',
        users=users,
        gold_image=gold_image,
        silver_image=silver_image,
        bronze_image=bronze_image,
        games=games)


def current_user():
    if session.get('user'):
        return models.users.query.get(session['user'])
    else:
        return False


@app.context_processor
def add_current_user():
    if session.get('user'):
        return dict(current_user=models.users.query.get(session['user']))
    return dict(current_user=None)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        print(login_form.login.data)
        user = models.users.query.filter(
            models.users.username == login_form.login.data).first()
        if user and check_password_hash(
                user.password, login_form.password.data):
            session['user'] = user.userId
            return redirect('/')
        else:
            # redirects back to login page and informs user that login info was
            # incorrect
            return render_template(
                'login.html',
                error='username or password incorrect',
                login_form=login_form)
    return render_template('login.html', login_form=login_form)


@app.route('/logout')
def logout():
    try:
        session.pop('user')  # removes user session
    except BaseException:
        # returns an error if the user tries to type in logout route whilst not
        # logged in
        return redirect('login', error='not currently logged in')
    return redirect('/')


@app.route('/createaccount', methods=['GET', 'POST'])
def createaccount():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        print(login_form.login.data)
        if 5 > len(login_form.login.data) > 12:
            # account will not be created with said username and user is
            # prompted to input a shorter/longer username
            return render_template(
                'createaccount.html',
                error='username must be between 5 and 12 characters')
        elif models.users.query.filter(models.users.username == login_form.login.data).first():
            # account will not be created and user is prompted to use a
            # different username
            return render_template(
                'createaccount.html',
                error='username already in use')
        elif len(login_form.password.data) < 7:
            # account will not be created and user is prompted to make a
            # password of atleast 7 characters
            return render_template(
                'createaccount.html',
                error='password must be a minimum of 7 characters')
        else:
            user_info = models.users(
                username=login_form.login.data,
                # takes password inputted in form and salts and hashes
                password=generate_password_hash(
                    login_form.password.data, salt_length=10),
                gamesWon=0,
                gamesLost=0,
                pictureId=0
            )
            db.session.add(user_info)
            db.session.commit()
    return render_template('createaccount.html', login_form=login_form)


@app.route('/play')
def play():
    users = models.users.query.all()
    if current_user():
        current_username = current_user().username
        return render_template(
            'play.html',
            users=users,
            current_username=current_username)
    else:
        return render_template('play.html')


@socketio.on('join')
def on_join(data):
    user_joined = data['user_joined']
    user = models.users.query.filter(
        models.users.username == user_joined['user']).first()
    user.sessionId = request.sid
    db.session.commit()


@socketio.on('sendAction')
def action(data):
    # these take values from the list generated in the js function and assign
    # them to useable variables
    user_chosen = data['form_data'][0]
    move_chosen = data['form_data'][1]
    user_sent = data['user_sent']

    game_info = models.game(
        username1=(
            models.users.query.filter_by(
                username=user_sent['user']).first()).username, move1=move_chosen, username2=(
            models.users.query.filter_by(
                username=user_chosen).first()).username)

    db.session.add(game_info)
    db.session.commit()

    chosen_sid = models.users.query.filter_by(username=user_chosen).first()
    data = []
    data.append(move_chosen)
    data.append(user_sent)
    data.append(user_chosen)
    data.append(game_info.gameId)
    emit('broadcast-choice', data, room=chosen_sid.sessionId)


@socketio.on('sendResponse')
def response(data):
    user_sent = data['challenger']
    move_chosen = data['move']
    user_received = data['challenged']
    game_info = data['game_info']
    game_to_add = models.game.query.filter_by(
        gameId=game_info,
        username1=user_sent['user'],
        username2=user_received).first()
    game_to_add.move2 = move_chosen
    db.session.commit()

    p1 = models.users.query.filter_by(username=user_sent['user']).first()
    p2 = models.users.query.filter_by(username=user_received).first()

    def p1_win():
        p1.gamesWon += 1
        p2.gamesLost += 1
        db.session.commit()
        data = 'win'
        emit('broadcast-result', data, room=p1.sessionId)
        data = 'loss'
        emit('broadcast-result', data, room=p2.sessionId)

    def p2_win():
        p1.gamesLost += 1
        p2.gamesWon += 1
        db.session.commit()
        data = 'win'
        emit('broadcast-result', data, room=p2.sessionId)
        data = 'loss'
        emit('broadcast-result', data, room=p1.sessionId)

    def tie():
        data = 'tie'
        emit('broadcast-result', data, room=p1.sessionId)
        emit('broadcast-result', data, room=p2.sessionId)

    if game_to_add.move1 == 'rock' and move_chosen == 'rock':
        tie()
    elif game_to_add.move1 == 'rock' and move_chosen == 'paper':
        p2_win()
    elif game_to_add.move1 == 'rock' and move_chosen == 'scissors':
        p1_win()
    elif game_to_add.move1 == 'paper' and move_chosen == 'paper':
        tie()
    elif game_to_add.move1 == 'paper' and move_chosen == 'rock':
        p1_win()
    elif game_to_add.move1 == 'paper' and move_chosen == 'scissors':
        p2_win()
    elif game_to_add.move1 == 'scissors' and move_chosen == 'scissors':
        tie()
    elif game_to_add.move1 == 'scissors' and move_chosen == 'paper':
        p1_win()
    elif game_to_add.move1 == 'scissors' and move_chosen == 'rock':
        p2_win()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


if __name__ == '__main__':
    socketio.run(app, debug=True)