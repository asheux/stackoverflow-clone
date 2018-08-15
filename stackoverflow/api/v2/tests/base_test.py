from unittest import TestCase
from stackoverflow import create_app, settings
from migrate import Migration

class BaseTestCase(TestCase):

    def setUp(self):
        self.app = create_app(settings.TESTING)
        self.migrate = Migration()
        self.migrate.create_all()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()

    def tearDown(self):
        """removes the db and the context"""
        self.migrate.drop_tables()