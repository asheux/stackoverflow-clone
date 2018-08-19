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
        answer = Answer()
        quiz = Question()
        my_list = [answer, quiz]
        for i in my_list:
            i.drop_all()
        BlackList.drop_all()
        User.drop_all()

create = Migration()
if __name__ == '__main__':
    create.create_all()
