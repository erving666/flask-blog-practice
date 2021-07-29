from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pymysql

pymysql.install_as_MySQLdb()

db = SQLAlchemy()

from restApi.resource.user import User, UserList


def create_app():
    app = Flask(__name__)
    api = Api(app)
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = 'mysql://ervin:yeyuwei@localhost:3306/flask_server'  # mysql+pymysql://...
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate = Migrate(app, db)

    api.add_resource(User, '/api/v1/user/<string:username>')
    api.add_resource(UserList, '/api/v1/users')

    return app
# for floder /api