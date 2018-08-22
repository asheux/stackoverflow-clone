"""
Imports

"""

from datetime import datetime
from flask import json
import psycopg2
from psycopg2.extras import RealDictCursor
from stackoverflow.api.v1.models import (
    MainModel, User,
    Question, Answer
)
from stackoverflow import database_config, settings

class DatabaseCollector(MainModel):
    """This is the base model"""
    __table__ = ""
    config = database_config(settings.DATABASE_URL)

    @classmethod
    def to_json(cls, item):
        """Creates a model object"""
        return json.loads(json.dumps(item, indent=4, sort_keys=True, default=str))

    @classmethod
    def drop_all(cls):
        """Drops all the tables"""
        conn = psycopg2.connect(**cls.config)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute("DROP TABLE {}".format(cls.__table__))
            conn.commit()
        except Exception as error:
            print(error)
        conn.close()

    @classmethod
    def get_all(cls):
        """Get all the items in the database"""
        conn = psycopg2.connect(**cls.config)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute("SELECT * FROM {}".format(cls.__table__))
            items = cur.fetchall()
            item = [cls.to_json(i) for i in items]
        except Exception as error:
            print(error)
        conn.close()
        return item

    @classmethod
    def get_by_field(cls, field, value):
        """Get a user from the database by key or field"""
        conn = psycopg2.connect(**cls.config)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            query = "SELECT * FROM users WHERE {} = %s".format(cls.__table__, field)
            cur.execute(query, (value,))
            items = cur.fetchall()
            item = [cls.to_json(i) for i in items]
        except Exception as error:
            print(error)
        conn.close()
        return item

    @classmethod
    def update(cls, field, item, _id):
        """Update the database"""
        conn = psycopg2.connect(**cls.config)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute(
                "UPDATE {} SET {} = %s WHERE id = %s".format(cls.__table__, field), (
                    item, _id
                )
            )
            conn.commit()
        except Exception as error:
            print(error)
        conn.close()

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
        conn = psycopg2.connect(**cls.config)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute("DELETE FROM {} WHERE id = %s".format(cls.__table__), (_id,))
            conn.commit()
        except Exception as error:
            print(error)
        conn.close()

    @classmethod
    def get_item_by_id(cls, _id):
        """Retrieves an item by the id provided"""
        conn = psycopg2.connect(**cls.config)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute("SELECT * FROM {} WHERE id = %s".format(cls.__table__), (_id,))
            item = cur.fetchone()
            if item is None:
                return None
        except Exception as error:
            print(error)
        conn.close()
        return cls.to_json(item)

class User(User, DatabaseCollector):
    __table__ = "users"
    config = database_config(settings.DATABASE_URL)

    @classmethod
    def create_table(cls):
        """Creates the table users"""
        conn = psycopg2.connect(**cls.config)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
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
        conn.commit()

    def insert(self):
        """save to the database"""
        conn = psycopg2.connect(**self.config)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute(
                "INSERT INTO users(name, username, email,"
                "password_hash, registered_on) VALUES(%s, %s, %s, %s, %s) RETURNING id", (
                    self.name,
                    self.username,
                    self.email,
                    self.password_hash,
                    self.registered_on
                )
            )
            conn.commit()
            result = cur.fetchone()
            if result is not None:
                self.id = result['id']
        except Exception as error:
            print(error)
        conn.close()
        return result

class Question(Question, DatabaseCollector):
    __table__ = "questions"
    config = database_config(settings.DATABASE_URL)

    @classmethod
    def create_table(cls):
        """creates the table questions"""
        conn = psycopg2.connect(**cls.config)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
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
        conn.commit()

    def insert(self):
        """save to the database"""
        conn = psycopg2.connect(**self.config)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            query = """
                    INSERT INTO questions(title, description, created_by, answers, date_created)
                    VALUES(%s, %s, %s, %s, %s) RETURNING id
                    """
            cur.execute(query, (
                self.title, self.description,
                self.created_by, self.answers,
                self.date_created
            ))
            conn.commit()
            result = cur.fetchone()
            if result is not None:
                self.id = result['id']
        except Exception as error:
            print(error)
        conn.close()
        return result

    @classmethod
    def transform_for_search(cls):
        """
        Concatenate and transforms the column
        title and description in metadata
        """
        conn = psycopg2.connect(**cls.config)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute(
                "SELECT title || '. ' || description as document, "
                "to_tsvector(title || '. ' || description) as metadata "
                "FROM questions"
            )
        except Exception as e:
            print(e)
        conn.close()

    @classmethod
    def fts_search_query(cls, search_item):
        """
        Search the transformed document in
        the database and return if found
        """
        conn = psycopg2.connect(**cls.config)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute(
                "SELECT * FROM questions "
                "WHERE to_tsvector(title || '. ' || description) @@ "
                "to_tsquery('{}')".format(search_item)
            )
            result = cur.fetchall()
            items = [cls.to_json(item) for item in result]
        except Exception as error:
            print(error)
        conn.close()
        return items

class Answer(Answer, DatabaseCollector):
    __table__ = "answers"
    config = database_config(settings.DATABASE_URL)

    @classmethod
    def create_table(cls):
        """Creates answer table"""
        conn = psycopg2.connect(**cls.config)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
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
        conn.commit()
        conn.close()

    def insert(self):
        """save to the database"""
        conn = psycopg2.connect(**self.config)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute(
                "INSERT INTO answers(answer, accepted, votes, owner,"
                "question, date_created) VALUES(%s, %s, %s, %s, %s, %s) RETURNING id", (
                    self.answer, self.accepted,
                    self.votes, self.owner,
                    self.question, self.date_created
                )
            )
            conn.commit()
            result = cur.fetchone()
            if result is not None:
                self.id = result['id']
        except Exception as error:
            print(error)
        conn.close()
        return result

class BlackList(DatabaseCollector):
    __table__ = "blacklist"

    def __init__(self, jti, blacklisted_on=datetime.now()):
        self.jti = jti
        self.blacklisted_on = blacklisted_on
        self.config = database_config(settings.DATABASE_URL)

    @classmethod
    def create_table(cls):
        """creates the blacklist table"""
        conn = psycopg2.connect(**cls.config)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS blacklist(
                id serial PRIMARY KEY,
                jti VARCHAR,
                blacklisted_on timestamp
            )
            """
        )
        conn.commit()

    def insert(self):
        """save to the database"""
        conn = psycopg2.connect(**self.config)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute(
                "INSERT INTO blacklist(jti, blacklisted_on) VALUES(%s, %s) RETURNING id", (
                    self.jti, self.blacklisted_on
                )
            )
            conn.commit()
        except Exception as error:
            print(error)
        conn.close()
