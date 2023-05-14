from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_pymongo import PyMongo
from pymongo.errors import DuplicateKeyError


# db = SQLAlchemy(session_options={"scopefunc": _app_ctx_stack.__ident_func__})
# migrate = Migrate()
load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    #MongoDB
    # client = MongoClient('localhost', 27017)
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    pymongo = PyMongo(app)
    

    # if test_config is None:
    #     app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    #         "SQLALCHEMY_DATABASE_URI")
    # else:
    #     app.config["TESTING"] = True
    #     app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    #         "SQLALCHEMY_TEST_DATABASE_URI")
    # db = SQLAlchemy()
    # db.init_app(app)
    # migrate.init_app(app, db)

    # from model.users import User
    # from model.account import Account
    return app, pymongo
