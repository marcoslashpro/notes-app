from flask_login import current_user
from app.website.models.models import Note, User, db
from flask import jsonify, flash
from sqlalchemy.sql import func

def jsonify_notes(notes: list[Note]):
	list_of_notes: list[dict] = []
	for note in notes:
		note_dict = {"id": note.id,"title": note.note_title, "content": note.note_content}
		list_of_notes.append(note_dict)
	return jsonify(list_of_notes)


def find_similar_notes(query: str) -> list[Note]:
	#Make sure it only returns notes when there is a certain percentage of accuracy.
	return Note.query.filter(
		       	    db.or_(
		            	func.lower(Note.note_title.like(f'{query}')),
		            	func.lower(Note.note_content.like(f'{query}'))
		            	)
		        	).all()


def find_user_notes(notes: list[Note]) -> list[Note]:
	matched_user_notes = []
	for note in notes:
		if note.user_id == current_user.id:
			matched_user_notes.append(note)


	return matched_user_notes


def update_note(id, content, title) -> Note | None:
	try:
		note = Note.query.get(id)
		if note:
			note.note_content = content
			note.note_title = title
			db.session.commit()
			return note
		else:
			flash('No matching notes found', 'error')
	except Exception as e:
		db.session.rollback()
		print(f'Error: {e}')

from flask import Flask
from app.website.models.models import db

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'istillhaventquit'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'

    db.init_app(app)

    from app.website.routes.views import views
    from app.website.routes.auth import auth
    from app.website.routes.agent import agent


    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(agent, url_prefix='/Jarvis/')

    return app


def link_db(db, app):
    with app.app_context():
        db.create_all()
