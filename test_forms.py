from unittest import TestCase
from forms import AddPetForm, EditPetForm

from app import app
from models import db

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

class AddPetFormDataTestCase(TestCase):
    """Tests that the data passed to AddPetForm class is validated"""
    
    @classmethod
    def setUpClass(cls):
        print("Inside Set Up Class")
            
        with app.app_context():
            
            cls.name = "Spot"
            cls.species = ["cat", "dog", "porcupine"]
            cls.photo_url = "https://unionlakepetservices.com/wp-content/uploads/2019/05/ULPS-Ears-AdobeStock_207410873-1080x675.jpg"
            cls.age = 3
            cls.notes = "Additional notes here."
            
            cls.form = AddPetForm()
            
            cls.form.name.data = cls.name
            cls.form.species.data = cls.species[1]
            cls.form.photo_url.data = cls.photo_url
            cls.form.age.data = cls.age
            cls.form.notes.data = cls.notes

    @classmethod
    def tearDownClass(cls):
        print("Inside tearDownClass")
        cls.form = ""

    def test_name_is_string(self):
        self.assertIsInstance(self.form.name.data, str)
        self.assertNotIsInstance(self.form.name.data, int)

    def test_name_is_not_none(self):
        self.assertIsNotNone(self.form.name.data, str)

    def test_species_is_string(self):
        self.assertIsInstance(self.form.species.data, str)
        self.assertNotIsInstance(self.form.species.data, int)

    def test_species_is_not_none(self):
        self.assertIsNotNone(self.form.species.data, str)

    def test_species_is_one_of_list(self):
        self.assertIn(self.form.species.data, self.species)

    def test_photo_url_is_string(self):
        self.assertIsInstance(self.form.photo_url.data, str)
        self.assertNotIsInstance(self.form.photo_url.data, int)

    def test_photo_url_is_url(self):
        self.assertIn("http", self.form.photo_url.data)

    def test_age_is_int(self):
        self.assertIsInstance(self.form.age.data, int)
        self.assertNotIsInstance(self.form.age.data, str)

    def test_age_is_within_bounds(self):
        self.assertGreaterEqual(self.form.age.data, 0)
        self.assertLessEqual(self.form.age.data, 30)

    def test_notes_is_string(self):
        self.assertIsInstance(self.form.notes.data, str)
        self.assertNotIsInstance(self.form.notes.data, int)

class EditPetFormDataTestCase(TestCase):
    """Tests that the data passed to AddPetForm class is validated"""
    
    @classmethod
    def setUpClass(cls):
        print("Inside Set Up Class")
            
        with app.app_context():
            
            cls.photo_url = "https://unionlakepetservices.com/wp-content/uploads/2019/05/ULPS-Ears-AdobeStock_207410873-1080x675.jpg"
            cls.notes = "Additional notes here."
            cls.available = True
            
            cls.form = EditPetForm()
            
            cls.form.photo_url.data = cls.photo_url
            cls.form.notes.data = cls.notes
            cls.form.available.data = cls.available

    @classmethod
    def tearDownClass(cls):
        print("Inside tearDownClass")
        cls.form = ""

    def test_photo_url_is_string(self):
        self.assertIsInstance(self.form.photo_url.data, str)
        self.assertNotIsInstance(self.form.photo_url.data, int)

    def test_photo_url_is_url(self):
        self.assertIn("http", self.form.photo_url.data)

    def test_notes_is_string(self):
        self.assertIsInstance(self.form.notes.data, str)
        self.assertNotIsInstance(self.form.notes.data, int)

    def test_available_is_boolean(self):
        self.assertIsInstance(self.form.available.data, bool)
        self.assertNotIsInstance(self.form.available.data, str)
        self.assertTrue(self.form.available.data)