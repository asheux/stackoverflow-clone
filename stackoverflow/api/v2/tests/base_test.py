from unittest import TestCase
from flask_restplus import Api, Resource, cors
from stackoverflow import create_app, settings, V2_API
from migrate import DBMigration

class BaseTestCase(TestCase):

    def setUp(self):
        self.app = create_app(settings.TESTING)
        self.migrate = DBMigration()
        self.migrate.create_all()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()

    def tearDown(self):
        """removes the db and the context"""
        self.migrate.drop_tables()