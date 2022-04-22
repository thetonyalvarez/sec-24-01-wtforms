from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
    
class Pet(db.Model):
    """Pet."""
    
    __tablename__ = "pets"
    
    # id: auto-incrementing integer
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # name: text, required
    name = db.Column(db.Text, nullable=False)
    # species: text, required
    species = db.Column(db.Text, nullable=False)
    # photo_url: text, optional
    photo_url = db.Column(db.Text, default="https://www.cartoonizemypet.com/assets/img/harlock-icon.png")
    # age: integer, optional
    age = db.Column(db.Integer)
    # notes: text, optional
    notes = db.Column(db.Text)
    # available: true/false, required, should default to available
    available = db.Column(db.Boolean, nullable=False, default=True)