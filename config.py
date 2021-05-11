import os

class Config(object):
    project_dir = os.path.dirname(os.path.abspath(__file__))
    database_file = (f'sqlite:///{(os.path.join(project_dir, "Go.db"))}')
    secret_key = ('visualstudiocodebest') # replace with real secret key
    SQLALCHEMY_DATABASE_URI = database_file
    SQLALCHEMY_TRACK_MODIFICATIONS = False