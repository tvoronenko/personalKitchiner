from flask_testing import TestCase
from tests.test_models import *
from app import app, db


class BaseTestCase(TestCase):
    """A base test case for flask-tracking."""

    def create_app(self):
        app.config.from_object('config.TestConfiguration')
        return app

    @classmethod
    def setUpClass(self):
        try:
            create_user()
        except RuntimeError:
            print("Cannot create user in user table")

    @classmethod
    def tearDownClass(self):
        try:
            delete_from_table("users")
        except RuntimeError:
            print("Cannot delete table user")

        try:
            delete_from_table("products")
        except RuntimeError:
            print("Cannot delete table products")

        try:
            delete_from_table("recipes")
        except RuntimeError:
            print("Cannot delete table recipes")

        try:
            delete_from_table("recipe_to_product")
        except RuntimeError:
            print("Cannot delete table recipe_to_product")