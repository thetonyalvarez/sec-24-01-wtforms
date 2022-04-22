from app import db
from models import Pet

db.drop_all()
db.create_all()

u = Pet(
    name="Spot", 
    species="Golden Retriever", 
    photo_url="https://www.puppyarea.com/wp-content/uploads/2020/08/Golden-Retriever-1.jpg", 
    age="3", 
    notes="lovable, friendly companion", 
    available=True)
db.session.add(u)
db.session.commit()
