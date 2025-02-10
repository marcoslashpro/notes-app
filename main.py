from website import create_app
from website import link_db
from flask_sqlalchemy import SQLAlchemy
from website.models import db, Note, User
from sqlalchemy import text
from flask_login import LoginManager


app = create_app()
link_db(db, app)
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


if __name__ == '__main__':
	app.run(debug=True)