from flask import Blueprint, Response, render_template, url_for, request, redirect, jsonify, flash
from flask_login import login_required, current_user
from app.website.models.models import Note, db
from app.website.website_funcs import jsonify_notes, find_similar_notes, find_user_notes, update_note
from sqlalchemy import func
from app.website.models.service import NoteService
from sqlalchemy.exc import SQLAlchemyError


views = Blueprint('views', __name__)
note_service = NoteService()


@views.route('/', methods=["GET", "POST"])
@login_required
def home():
    user_notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template('home.html', notes=user_notes, user=current_user)


@views.route('/profile-page/<int:user_id>')
@login_required
def profile_page(user_id):
    return render_template('profilepage.html', user=current_user)


@views.route('/display-note', methods=["GET", "POST"])
@login_required
def display_note():
    if request.method == "POST":
        note = create_note()
        json_data = note.get_json()

        if json_data['created'] == False:
            flash(json_data['message'], 'error')
            return render_template('notes.html', user=current_user)

        note_id = json_data.get('note_id')
        if not note_id:
            raise ValueError(f"No note Id found in the newly created note: {json_data}")

        note = Note.query.get(json_data['note_id'])
        if not note:
            raise ValueError(f"Something went incredibly wrong and the note was not saved successfully: {json_data}")


        return render_template('notes.html', user=current_user, note=note)

    return render_template('notes.html', user=current_user)

@views.route('/create_note', methods=["POST"])
@login_required
def create_note():
    note_title = request.form.get('title')
    note_content = request.form.get('content')

    if not note_title or not note_content:
        return jsonify({
            'Content-Type': 'apllication/json',
            'created': False,
            'message': 'Please enter both title and content'
            })

    new_note = Note(
        note_title=note_title, note_content=note_content, user_id=current_user.id  # type: ignore[call-args]
    )

    if not new_note:
        return jsonify({
            'Content-Type': 'apllication/json',
            'created': False,
            'message': 'There was an error while creating the Note'
            })

    try:
        db.session.add(new_note)
        db.session.commit()

    except SQLAlchemyError as e:
        return jsonify({
            'Content-Type': 'apllication/json',
            'created': False,
            'message': f'There was a problem while adding the note to the database: {e}'
            })

    flash('Note saved successfully', 'success')
    return jsonify(
        {
            "Content-Type": "application/json",
            'created': True,
            'note_id': new_note.id,
            'note_content': new_note.note_content,
            'note_title': new_note.note_title
        }
    )

@views.route('/get-note/<int:note_id>', methods=["GET", "POST"])
@login_required
def get_note(note_id: int):
    note = Note.query.get(note_id)

    if request.method == "POST":
        title = request.form.get('title')
        content = request.form.get('content')
        updated_note = update_note(
            id=note_id,
            title=title,
            content=content
            )
        return render_template('notes.html', user=current_user, note=updated_note)

    if note:
        return render_template('notes.html', user=current_user, note=note)
    else:
        flash('Note was not accessible', 'error')
        return redirect('views.home')


@views.route('/delete-note/<int:note_id>', methods=["POST"])
@login_required
def delete_note(note_id):
    note = Note.query.get(note_id)

    try:
        db.session.delete(note)
        db.session.commit()
    except Exception as e:
        flash(f'Error: {e}', 'error')


    return redirect(url_for('views.home'))


@views.route('/search-note', methods=["POST"])
@login_required
def search_note():
    data = request.get_json()
    query = data.get('query')
    similar_notes = find_similar_notes(query)
    user_notes = find_user_notes(similar_notes)
    return jsonify_notes(user_notes)