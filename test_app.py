from unittest import TestCase

from app import app
from models import db, Cupcake
from seed import seed_db

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

db.drop_all()
db.create_all()

#write a test for the 

class CupcakeViewsTestCase(TestCase):
    def setUp(self):
        """ Setup for the tests"""
        Cupcake.query.delete()
        db.session.commit()

        #uses seed.py's seed_db() to setup the db for tests
        seed_db()
    
    def tearDown(self):
        """Clean up fouled transactions."""
        db.session.rollback()

    def test_create_cupcake(self):
        """ Tests if POST '/api/cupcakes/ creates a cupcake even with an empty image field. '"""
        with app.test_client() as client:
            resp = client.post("/api/cupcakes", json = {
                "flavor": "test flavor",
                "rating": 10,
                "size": "test size",
                "image": ""
            })
            self.assertEqual(resp.json['cupcake']['image'], "https://tinyurl.com/demo-cupcake")

    def test_update_cupcake(self):
        with app.test_client() as client:
            """ Tests if PATCH '/api/cupcakes/<id> updates a cupcake. '"""
            resp = client.patch("/api/cupcakes/1", json = {
                "flavor": "updated",
                "image": "new_url_2",
                "rating": 10,
                "size": "new_size_2"
            })
            self.assertEqual(resp.json['cupcake']['flavor'], "updated")

    def test_delete_cupcake(self):
        """ Tests if DELETE '/api/cupcakes/<id>' deletes a cupcake. """
        with app.test_client() as client:
            resp = client.delete("/api/cupcakes/2")
            self.assertEqual(resp.json['message'], "Deleted")