from stackoverflow.api.v2.models import (
    User,
    BlackList,
    Question,
    Answer
)

class Migration:

    @staticmethod
    def create_all():
        """Creates the tables"""
        User.migrate()
        Question.migrate()
        Answer.migrate()
        BlackList.migrate()


    @staticmethod
    def drop_tables():
        """drops all the tables"""
        Answer.drop_all()
        Question.drop_all()
        User.drop_all()
        BlackList.drop_all()

def main():
    from stackoverflow import Database, create_app, settings
    app = create_app(settings.DEVELOPMENT)
    my_db = Database()
    my_db.init_db(app)
    migrate = Migration()
    migrate.create_all()
if __name__ == '__main__':
    main()
