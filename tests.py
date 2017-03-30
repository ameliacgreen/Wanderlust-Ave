from unittest import TestCase, main

from server import app
from model import db, example_data, connect_to_db


class BucketTests(TestCase):
    """Tests for WanderList."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn("ADVENTURE AWAITS", result.data)

    def test_mylists(self):
        """Test if user can't see my-lists if they are not signed in"""
        result = self.client.get("/my-lists", follow_redirects=True)
        self.assertIn("You are not signed in", result.data)

    def test_public_map(self):
        result = self.client.get("/map")
        self.assertIn("See The Eiffel Tower", result.data)

    def test_item_page(self):
        result = self.client.get("/my-lists/1")
        self.assertIn("Add a new item", result.data)

    # def test_registration(self):
    #     result = self.client.post("/register", data={"first-name": "Auden",
    #                                                  "last-name": "Ezra",
    #                                                  "username": "cats",
    #                                                  "password": "purr",
    #                                                  "email": "auden@gmail.com"},
    #                                             follow_redirects=True)
    #     self.assertIn("Hi cats!", result.data)

    def test_duplicate_registration(self):
        result = self.client.post("/register", data={"first-name": "Hackbright",
                                                     "last-name": "Academy",
                                                     "username": "balloonicorn",
                                                     "password": "party",
                                                     "email": "balloonicorn@gmail.com"},
                                                follow_redirects=True)
        self.assertIn("balloonicorn already exists", result.data)


    def test_login(self):
        result = self.client.post("/login", data={"username": "balloonicorn",
                                                  "password": "party"},
                                            follow_redirects=True)
        self.assertIn("Create a new list", result.data)



    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database (uncomment when testing database)
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data (uncomment when testing database)
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        # (uncomment when testing database)
        db.session.close()
        db.drop_all()

if __name__ == '__main__':
    main()