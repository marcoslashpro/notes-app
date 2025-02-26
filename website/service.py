from .models import Note, User, db
from flask_login import current_user
from flask import flash
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash


class NoteService:
    """Service layer for Note model"""

    @staticmethod
    def get_user_notes(user: User):
        """Retrieve all notes for a given user"""
        return Note.query.filter_by(user_id=user.id).order_by(Note.date.desc()).all()

    @staticmethod
    def is_valid(title: str, content: str) -> bool:
        """Check if the title and content are valid"""
        return bool(title and content and len(content) > 1)

    @staticmethod
    def add_note(note_title: str, note_content: str) -> bool:
        """Add a new note for the current user"""
        try:
            new_note = Note(user_id=current_user.id, note_title=note_title, note_content=note_content)
            db.session.add(new_note)
            db.session.commit()
            return new_note
        except SQLAlchemyError as e:
            flash(f'Error: {e}', 'error')
            return False

    @staticmethod
    def get_most_recent():
        """Retrieve the most recent note"""
        return Note.query.order_by(Note.date.desc()).first()

    @staticmethod
    def get_note_by_id(note_id: int) -> Note:
        """Retrieve a note by its ID"""
        try:
            note = Note.query.get(note_id)
            return note if note else None
        except ValueError as e:
            flash(f'Error: {e}', 'error')
            return None

    @staticmethod
    def update_note_title(note_id: int, new_title: str) -> bool:
        """Update the title of a specific note"""
        note = NoteService.get_note_by_id(note_id)
        if note:
            try:
                note.note_title = new_title
                db.session.commit()
                return True
            except SQLAlchemyError as e:
                flash(f'Error: {e}', 'error')
        return False


class UserService(User):

    @staticmethod
    def user_exists(email) -> bool:
        try:
            user = User.query.filter_by(email=email).first()
            if user:
                return user
            else:
                return None
        except Exception as e:
            return {f'Error: {e}'} #to be logged


    @staticmethod
    def create_User(email: str, username: str, password: str) -> User:
        try:
            new_user = User(email=email, username=username, password=password)
            if not UserService.is_username_taken():
                if new_user:
                    db.session.add(new_user)
                    db.session.commit()
                else:
                    return None
        except Exception as e:
            return f'Error: {e}'


    @staticmethod
    def is_username_taken(username: str) -> bool:
        try:
            existing_username = User.query.filter_by(username=username).first()
            if existing_username:
                print(f'Found username: {existing_username}')
                return True
            else:
                print('No username found')
                return False
        except Exception as e:
            print(f'Error: {e}')
            return False


    def get_user_by_id(user_id: int):
        try:
            user = User.query.get(int(user_id))
            if user:
                return User
        except Exception as e:
            print(f'Error: {e}')
            flash('Error getting the user id', 'error')


class SignUpInput(UserService):
    def __init__(self, email, username, password=None, passw2=None):
        self.email = email
        self.username = username
        self.password = passw1
        self.passw2 = passw2


    def is_valid(self) -> bool:
        if not self.email:
            flash('Missing email', 'error')
        elif not self.username:
            flash('Missing username', 'error')
        elif not self.passw1 or not self.passw2:
            flash('Missing password', 'error')
        elif len(self.username) < 5:
            flash('Username must be at least 6 characters', 'error')
        elif len(self.passw1) < 7:
            flash('Password must be at least 8 characters', 'error')
        elif self.passw1 != self.passw2:
            flash("Passwords don't match", 'error')

        # Email and Password validations to be added

        elif UserService.user_exists(self.email):
            flash('User already exists', 'error')
        elif UserService.is_username_taken(self.username):
            flash('Username is already taken', 'error')
        else:
            return True


    def hash_password(self):
        try:
            hashed_password = generate_password_hash(self.passw1, method='pbkdf2:sha256', salt_length=16)
            if hashed_password:
                return hashed_password
            else:
                return 'Problem generating the hashed password'
        except Exception as e:
            return f'Error: {e}'


class LoginInput(SignUpInput):
    def __init__(self, email, password):
        super().__init__(
            email=email,
            username=None,
            password=password,
            )


    def is_valid(self):
        if not self.email:
            flash('Missing email', 'error')
            return False
        if not self.password:
            flash('Missing password', 'error')
            return False
        if len(self.password) < 7:
            flash('Password must be at least 8 characters', 'error')
            return False
        return True 
