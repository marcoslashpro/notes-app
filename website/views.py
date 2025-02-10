from flask import Blueprint, render_template, url_for, request, redirect, jsonify, flash
from flask_login import login_required, current_user
from .models import Note, db
from .website_funcs import jsonify_notes, find_similar_notes, find_user_notes
from sqlalchemy import func
from .service import NoteService 


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
        try:
            json_note = create_note()
            note_data = json_note.get_json()
        except AttributeError as e:
            pass

        if note_data:
            note = Note.query.get(note_data['note_id'])
            return render_template('notes.html', user=current_user, note=note)

    return render_template('notes.html', user=current_user)



@views.route('/create_note', methods=["POST"])
@login_required
def create_note():
    if request.method == "POST":
        note_title = request.form.get('title')
        note_content = request.form.get('content')

        print(f'Note content: {note_content}, Note title: {note_title}')
        
        if note_title and note_content:
            new_note = Note(note_title=note_title, 
                note_content=note_content,
                user_id=current_user.id)
            if new_note:
                db.session.add(new_note)
                db.session.commit()
                flash('Note saved successfully', 'success')
                return jsonify({
                    "Content-Type": "application/json",
                    'note_id': new_note.id,
                    'note_content': new_note.note_content,
                    'note_title': new_note.note_title
                    })
            else:
                print('Note not generated')
        else:
            flash('Please enter both title and content', 'error')


    return render_template('notes.html', user=current_user)


@views.route('/get-note/<int:note_id>', methods=["GET", "POST"])
@login_required
def get_note(note_id: int):
    note = Note.query.get(note_id)
    if note:
        return render_template('notes.html', user=current_user, note=note)
    else:
        flash('Note was not accessible', 'error')
        return redirect('views.home', user=current_user)


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