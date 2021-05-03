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
'''

