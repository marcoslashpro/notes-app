from typing import Optional
from app.website.models.models import Note, User, db
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
            new_note = Note(
                user_id=current_user.id,  # type: ignore[call-args]
                note_title=note_title,  # type: ignore[call-args]
                note_content=note_content  # type: ignore[call-args]
                )
            db.session.add(new_note)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            flash(f'Error: {e}', 'error')
            return False

    @staticmethod
    def get_most_recent():
        """Retrieve the most recent note"""
        return Note.query.order_by(Note.date.desc()).first()

    @staticmethod
    def get_note_by_id(note_id: int) -> Note | None:
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
    def create_User(email: str, username: str, password: str) -> User:
        new_user = User(email=email, username=username, password=password)  # type: ignore[call-args]

        if not new_user:
            raise ValueError(
                f"Unable to create new user with stats: {email}, {username}, {password}"
            )

        db.session.add(new_user)
        db.session.commit()
        return new_user

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

    @staticmethod
    def get_user_by_id(user_id: int):
        try:
            user = User.query.get(int(user_id))
            if user:
                return User
        except Exception as e:
            print(f'Error: {e}')
            flash('Error getting the user id', 'error')

    @staticmethod
    def get_user_by_email(email: str) -> User | None:
        user: User | None = User.query.filter_by(email=email).first()

        if not user:
            return

        return user


class SignUpInput(UserService):

    @staticmethod
    def sign_up(email: str, username: str, password: str) -> tuple[str, Optional[User]]:
        if UserService.is_username_taken(username):
            return f'Username {username} is already in use', None

        user = UserService.create_User(email, username, SignUpInput.hash_password(password))

        if user:
            return f'User: {username} created successfully', user
        else:
            return f'Was not able to create new user: {username}', None

    @staticmethod
    def is_input_valid(
            password: str | None,
            passw2: str | None,
            username: str | None,
            email: str | None
        ) -> tuple[bool, str]:
        if not email:
            return False, 'Missing email'

        elif not username:
            return False, 'Missing username'

        elif not password or not passw2:
            return False, 'Missing passwords'

        elif len(username) < 5:
            return False, 'Username must be at least 6 characters'

        elif len(password) < 7:
            return False, 'Password must be at least 8 characters'

        elif password != passw2:
            flash("Passwords don't match", 'error')
            return False, "Passwords don't match"

        # Email and Password validations to be added

        elif UserService.get_user_by_email(email) is not None:
            return False, f'User with email {email} already exists'

        elif UserService.is_username_taken(username):
            return False, f'Username {username} already taken'

        else:
            return True, ''

    @staticmethod
    def hash_password(password: str) -> str:
        try:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
            if hashed_password:
                return hashed_password
            else:
                return 'Problem generating the hashed password'
        except Exception as e:
            return f'Error: {e}'


class LoginInput(SignUpInput):
    @staticmethod
    def is_valid(email, password) -> tuple[bool, str]:
        if not email:
            return False, 'Missing email'
        if not password:
            return False, 'Missing password'
        if len(password) < 8:
            return False, 'Password must be at least 8 characters'

        return True, ''
