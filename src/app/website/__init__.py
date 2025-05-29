from flask import Flask
from .models import db


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'istillhaventquit'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'

    db.init_app(app)

    from .views import views
    from .auth import auth
    from .agent import agent


    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(agent, url_prefix='/Jarvis/')

    return app


def link_db(db, app):
    with app.app_context():
        db.create_all()
