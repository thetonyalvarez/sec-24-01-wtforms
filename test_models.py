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

class PetModel(TestCase):
    """Test Pet Model."""
    
    @classmethod
    def setUpClass(cls):
        print("Inside setUpClass")
        
        with app.app_context():
        
            cls.newPet = Pet()
            
            cls.id = 123
            cls.name = "Spot"
            cls.species = ["cat", "dog", "porcupine"]
            cls.photo_url = "https://unionlakepetservices.com/wp-content/uploads/2019/05/ULPS-Ears-AdobeStock_207410873-1080x675.jpg"
            cls.age = 3
            cls.notes = "additional notes here."
            cls.available = True
        
            cls.newPet.id = cls.id
            cls.newPet.name = cls.name
            cls.newPet.species = cls.species[2]
            cls.newPet.photo_url = cls.photo_url
            cls.newPet.age = cls.age
            cls.newPet.notes = cls.notes
            cls.newPet.available = cls.available
    
    def test_id_is_int(self):
        self.assertIsInstance(self.newPet.id, int)
        self.assertNotIsInstance(self.newPet.id, str)
    
    def test_name_is_string(self):
        self.assertIsInstance(self.newPet.name, str)
        self.assertNotIsInstance(self.newPet.name, int)

    def test_name_is_not_none(self):
        self.assertIsNotNone(self.newPet.name, str)

    def test_species_is_string(self):
        self.assertIsInstance(self.newPet.species, str)
        self.assertNotIsInstance(self.newPet.species, int)

    def test_species_is_not_none(self):
        self.assertIsNotNone(self.newPet.species, str)

    def test_species_is_one_of_list(self):
        self.assertIn(self.newPet.species, self.species)

    def test_photo_url_is_string(self):
        self.assertIsInstance(self.newPet.photo_url, str)
        self.assertNotIsInstance(self.newPet.photo_url, int)

    def test_photo_url_is_url(self):
        self.assertIn("http", self.newPet.photo_url)

    def test_age_is_int(self):
        self.assertIsInstance(self.newPet.age, int)
        self.assertNotIsInstance(self.newPet.age, str)

    def test_age_is_within_bounds(self):
        self.assertGreaterEqual(self.newPet.age, 0)
        self.assertLessEqual(self.newPet.age, 30)

    def test_notes_is_string(self):
        self.assertIsInstance(self.newPet.notes, str)
        self.assertNotIsInstance(self.newPet.notes, int)

    def test_available_is_boolean(self):
        self.assertIsInstance(self.newPet.available, bool)
        self.assertNotIsInstance(self.newPet.available, str)
        self.assertTrue(self.newPet.available)