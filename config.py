import os

class Config(object):
    project_dir = os.path.dirname(os.path.abspath(__file__))
    database_file = (f'sqlite:///{(os.path.join(project_dir, "Go.db"))}')
    secret_key = ('MEVo8l)@eg~}f(s?)Wt${rgwm7cGIPR5W&,Q4I^70.m(`]{.C1xPfaZJg@h}+')
    SQLALCHEMY_DATABASE_URI = database_file
    SQLALCHEMY_TRACK_MODIFICATIONS = False