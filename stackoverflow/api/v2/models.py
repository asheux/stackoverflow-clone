from flask import json
from stackoverflow.api.v1.models import (
    MainModel,
    User,
    Question,
    Answer
)
from datetime import datetime
from stackoverflow import v2_db

class DatabaseCollector(MainModel):
    """This is the base model"""
    __table__ = ""

    @classmethod
    def to_json(cls, item):
        """Creates a model object"""
        return json.loads(json.dumps(item, indent=4, sort_keys=True, default=str))

    @classmethod
    def drop_all(cls):
        """Drops all the tables"""
        v2_db.cursor.execute("DROP TABLE {}".format(cls.__table__))
        v2_db.connection.commit()

    def insert(self):
        """Inserts a new item in the database"""
        result = v2_db.cursor.fetchone()
        if result is not None:
            self.id = result['id']
        v2_db.connection.commit()

    @classmethod
    def get_all(cls):
        """Get all the items in the database"""
        try:
            cur = v2_db.cursor
            cur.execute("SELECT * FROM {}".format(cls.__table__))
            items = cur.fetchall()
            item = [cls.to_json(i) for i in items]
            return item
            cur.close()
        except Exception as e:
            print(e)

    @classmethod
    def get_by_field(cls, field, value):
        """Get a user from the database by key or field"""
        try:
            cur1 = v2_db.cursor
            query = "SELECT * FROM users WHERE {} = %s".format(cls.__table__, field)
            cur1.execute(query, (value,))
            items = cur1.fetchall()
            item = [cls.to_json(i) for i in itemss]
            return item
            cur1.close()
        except Exception as e:
            print(e)

    @classmethod
    def get_one_by_field(cls, field, value):
        """Get a user from the database by key or field"""
        if cls.get_all() is None:
            return []
        for item in cls.get_all():
            if item[field] == value:
                return item

    @classmethod
    def delete(cls, _id):
        """deletes an item from the database"""
        try:
            cur2 = v2_db.cursor
            cur2.execute("DELETE FROM {} WHERE id = %s".format(cls.__table__), (_id,))
            v2_db.connection.commit()
        except Exception as e:
            print(e)

    @classmethod
    def get_item_by_id(cls, _id):
        """Retrieves an item by the id provided"""
        try:
            cur3 = v2_db.cursor
            cur3.execute("SELECT * FROM {} WHERE id = %s".format(cls.__table__), (_id,))
            item = cur3.fetchone()
            if item is None:
                return None
            return cls.to_json(item)
            cur3.close()
        except Exception as e:
            print(e)

class User(User, DatabaseCollector):
    __table__ = "users"

    @classmethod
    def migrate(cls):
        v2_db.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users(
                id serial PRIMARY KEY,
                name VARCHAR,
                username VARCHAR,
                email VARCHAR,
                password_hash VARCHAR,
                registered_on timestamp
            )
            """
        )
        v2_db.connection.commit()

    def insert(self):
        """save to the database"""
        v2_db.cursor.execute(
            "INSERT INTO users(name, username, email,"
            "password_hash, registered_on) VALUES(%s, %s, %s, %s, %s) RETURNING id", (
                self.name,
                self.username,
                self.email,
                self.password_hash,
                self.registered_on
            )
        )
        super().insert()

class Question(Question, DatabaseCollector):
    __table__ = "questions"

    @classmethod
    def migrate(cls):
        v2_db.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS questions(
                id serial PRIMARY KEY,
                title VARCHAR,
                description VARCHAR,
                created_by INTEGER,
                answers INTEGER,
                date_created timestamp,
                FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE CASCADE
            )
            """
        )
        v2_db.connection.commit()

    def insert(self):
        """save to the database"""
        v2_db.cursor.execute(
            "INSERT INTO questions(title, description, created_by,"
            "answers, date_created) VALUES(%s, %s, %s, %s, %s) RETURNING id", (
                self.title,
                self.description,
                self.created_by,
                self.answers,
                self.date_created
            )
        )
        super().insert()

    @classmethod
    def transform_for_search(cls):
        try:
            v2_db.cursor.execute(
                "SELECT title || '. ' || description as document, "
                "to_tsvector(title || '. ' || description) as metadata "
                "FROM questions"
            )
        except Exception as e:
            print(e)

    @classmethod
    def fts_search_query(cls, search_item):
        try:
            v2_db.cursor.execute(
                "SELECT * FROM questions "
                "WHERE to_tsvector(title || '. ' || description) @@ "
                "to_tsquery('{}')".format(search_item)
            )
            result = v2_db.cursor.fetchall()
            items = [cls.to_json(item) for item in result]
            return items
        except Exception as e:
            print(e)

    @classmethod
    def updatequestion(cls, answers, _id):
        try:
            v2_db.cursor.execute(
                "UPDATE questions SET answers = %s WHERE id = %s", (
                    answers,
                    _id
                )
            )
            v2_db.connection.commit()
        except Exception as e:
            print(e)

class Answer(Answer, DatabaseCollector):
    __table__ = "answers"

    @classmethod
    def migrate(cls):
        v2_db.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS answers(
                id serial PRIMARY KEY,
                answer VARCHAR,
                accepted BOOL,
                votes INTEGER,
                owner INTEGER REFERENCES users(id) ON DELETE CASCADE,
                question INTEGER REFERENCES questions(id) ON DELETE CASCADE,
                date_created timestamp
            )
            """
        )
        v2_db.connection.commit()

    def insert(self):
        """save to the database"""
        v2_db.cursor.execute(
            "INSERT INTO answers(answer, accepted, votes, owner,"
            "question, date_created) VALUES(%s, %s, %s, %s, %s, %s) RETURNING id", (
                self.answer,
                self.accepted,
                self.votes,
                self.owner,
                self.question,
                self.date_created
            )
        )
        super().insert()

    @classmethod
    def accepteandupdate(cls, accepted, _id):
        try:
            v2_db.cursor.execute(
                "UPDATE answers SET accepted = %s WHERE id = %s", (
                    accepted,
                    _id
                )
            )
            v2_db.connection.commit()
        except Exception as e:
            print(e)

    @classmethod
    def voteandupdate(cls, votes, _id):
        try:
            v2_db.cursor.execute(
                "UPDATE answers SET votes = %s WHERE id = %s", (
                    votes,
                    _id
                )
            )
            v2_db.connection.commit()
        except Exception as e:
            print(e)

class BlackList(DatabaseCollector):
    __table__ = "blacklist"

    def __init__(self, jti, blacklisted_on=datetime.now()):
        self.jti = jti
        self.blacklisted_on = blacklisted_on

    @classmethod
    def migrate(cls):
        v2_db.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS blacklist(
                id serial PRIMARY KEY,
                jti VARCHAR,
                blacklisted_on timestamp
            )
            """
        )
        v2_db.connection.commit()

    def insert(self):
        """save to the database"""
        v2_db.cursor.execute(
            "INSERT INTO blacklist(jti, blacklisted_on) VALUES(%s, %s) RETURNING id", (
                self.jti,
                self.blacklisted_on
            )
        )
        v2_db.connection.commit()
