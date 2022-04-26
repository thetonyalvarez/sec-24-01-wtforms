from unittest import TestCase

from app import app
from models import db, Pet

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt_test_db'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Don't req CSRF for testing
app.config['WTF_CSRF_ENABLED'] = False

db.drop_all()
db.create_all()

class StartAppTest(TestCase):
    """Test start of app."""

    def test_show_home(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<title>Home', html)

class PetTest(TestCase):
    """Test Add Pet routes."""

    @classmethod
    def setUpClass(cls):
        """Set up test database"""
        print("Inside setUpClass")

        Pet.query.delete();
        
        cls.species = ["cat", "dog", "porcupine"]

        newPet = Pet(
            id = 123,
            name = "Spot",
            species = "porcupine",
            photo_url = "https://unionlakepetservices.,com/wp-content/uploads/2019/05/ULPS-Ears-AdobeStock_207410873-1080x675.jpg",
            age = 3,
            notes = "additional notes here.",
            available = True
        )

        db.session.add(newPet)
        db.session.commit()

        cls.newPet_id = newPet.id
        cls.newPet_name = newPet.name
        cls.newPet_species = newPet.species[2]
        cls.newPet_photo_url = newPet.photo_url
        cls.newPet_age = newPet.age
        cls.newPet_notes = newPet.notes
        cls.newPet_available = newPet.available

    @classmethod
    def tearDownClass(cls):
        """Clean up test database"""
        print("Inside tearDownClass")
        
        db.session.rollback()

    def test_add_get(self):
        """Test GET method for /add url"""

        with app.test_client() as client:
            resp = client.get("/add")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Add Pet', html)
            self.assertNotIn('Home', html)

    def test_add_pet(self):
        """Test POST method for /add url"""
        with app.test_client() as client:
            resp = client.post(
                "/add",
                data={
                    'name': {self.newPet_name},
                    'species': {self.newPet_species},
                    'photo_url': {self.newPet_photo_url},
                    'age': {self.newPet_age},
                    'notes': {self.newPet_notes}
                },
                follow_redirects=True)

            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Spot", html)

            pet = Pet.query.get(self.newPet_id)

            self.assertEquals(pet.name, "Spot")
            self.assertEquals(pet.species, "porcupine")

    def test_show_pet(self):
        """Test a view pet page."""

        with app.test_client() as client:
            resp = client.get(f"/pets/{self.newPet_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Meet Spot', html)
            self.assertNotIn('Home', html)      

    # ! Why is this not working? I am trying to test changing available to False but will not appear on response
    def test_edit_pet(self):
        """Test POST method for /add url"""

        with app.test_client() as client:
            
            testData = {
                    'photo_url': {self.newPet_photo_url},
                    'notes': {self.newPet_notes},
                    'available': False
            }
            
            resp = client.post(
                f"/pets/{self.newPet_id}",
                data = testData,
                follow_redirects = True
            )

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("is available", html)