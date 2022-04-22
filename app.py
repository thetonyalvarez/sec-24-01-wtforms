from flask import Flask, render_template, flash, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet

from forms import AddPetForm, EditPetForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "oh-so-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///adopt"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def pets_show_all():
    """Show index."""
    pets = Pet.query.all()
    return render_template("index.html", pets=pets)

@app.route('/add', methods=['GET','POST'])
def pet_add():
    """Add pet."""
    
    form = AddPetForm()
    
    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data
        
        pet = Pet(name=name, species=species, photo_url=photo_url, age=age, notes=notes)
        db.session.add(pet)
        db.session.commit()
        
        return redirect("/")
    
    else:
        return render_template("add-pet.html", form=form)
    
@app.route("/pets/<int:id>", methods=["GET", "POST"])
def pet_edit(id):
    """Edit pet."""
    
    pet = Pet.query.get_or_404(id)
    form = EditPetForm(obj=pet)
    
    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data
        db.session.commit()
        flash(f'{pet.name} has been updated!')
        return redirect(f'/pets/{id}')

    else:
        return render_template("pet.html", pet=pet, form=form)
