from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, URLField, SelectField, BooleanField
from wtforms.validators import InputRequired, NumberRange, Optional, Email

species = ["cat", "dog", "porcupine"]

class AddPetForm(FlaskForm):
    # name: text, required
    name = StringField("Name", validators=[InputRequired()])

    # species: text, required
    species = SelectField("Species", choices=[(sp, sp) for sp in species])
    
    # photo_url: text, optional
    photo_url = URLField("Photo URL", validators=[Optional()])
    
    # age: integer, optional
    age = IntegerField("Age", validators=[NumberRange(min=0, max=30)])
    
    # notes: text, optional
    notes = StringField("Notes")

class EditPetForm(FlaskForm):
    
    # photo_url: text, optional
    photo_url = URLField("Photo URL", validators=[Optional()])
    
    # notes: text, optional
    notes = StringField("Notes")
    
    # notes: text, optional
    available = BooleanField("Availability")