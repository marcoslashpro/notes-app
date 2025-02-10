from flask_login import current_user
from .models import Note, User, db
from flask import jsonify
from sqlalchemy.sql import func

def jsonify_notes(notes: Note):
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
