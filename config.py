import os
class Config(object):
    project_dir = os.path.dirname(os.path.abspath(__file__))
    database_file = (f'sqlite:///{(os.path.join(project_dir, "psr.db"))}')
    SECRET_KEY = ('reallysupersecureencryptionkey(real)')
    SQLALCHEMY_DATABASE_URI = database_file
    SQLALCHEMY_TRACK_MODIFICATIONS = False