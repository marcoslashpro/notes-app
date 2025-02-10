from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .models import db, User


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'istillhaventquit'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app


def link_db(db, app):
	with app.app_context():
		db.create_all()
