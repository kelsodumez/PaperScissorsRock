'''
Kelso du Mez
3/05/2021 - (date when finished)
SQLAlchemy Go Website (hopefully)
'''
from flask import Flask, render_template, session, redirect, url_for, request, Blueprint, flash
from random import randint, choice
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, Column, Integer
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app) # defines db as sqlalchemy connection to database
import models

#yeah