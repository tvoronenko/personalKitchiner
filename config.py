import os

_basedir = os.path.abspath(os.path.dirname(__file__))
# config.py

# base configuration
class BaseConfiguration(object):
    DEBUG = False
    TESTING = False

    DATABASE = 'my_recipes.db'

    DATABASE_PATH = os.path.join(_basedir, DATABASE)
    DATABASE_URI = 'sqlite:///' + DATABASE_PATH

# test configuration
class TestConfiguration(BaseConfiguration):
    TESTING = True

    DATABASE = 'tests.db'
    DATABASE_PATH = os.path.join(_basedir, DATABASE)
    DATABASE_URI = 'sqlite:///' + DATABASE_PATH

# development configuration
class DebugConfiguration(BaseConfiguration):
    DEBUG = True