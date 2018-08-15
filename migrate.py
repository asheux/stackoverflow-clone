from stackoverflow.api.v2.models import (
    User,
    BlackList,
    Question,
    Answer
)

class Migration:
    @staticmethod
    def refresh_db():
        Migration.tear_down()
        Migration.create_all()

    @staticmethod
    def create_all():
        """Creates the tables"""
        User.migrate()
        Question.migrate()
        Answer.migrate()
        BlackList.migrate()

    @staticmethod
    def tear_down():
        """Deletes data from the the tables"""
        User.rollback()
        Question.rollback()
        Answer.migrate()
        BlackList.rollback()

    @staticmethod
    def drop_tables():
        """drops all the tables"""
        Answer.drop_all()
        Question.drop_all()
        User.drop_all()
        BlackList.drop_all()