from website import create_app, db
from website.models import Note

app = create_app()
with app.app_context():
    notes = Note.query.filter_by(user_id=3).all()
    print(notes)  # Should return a list of notes
