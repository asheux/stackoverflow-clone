'''
Creating constant queries

'''
QUERY1 = """
    CREATE TABLE IF NOT EXISTS users(
    id serial PRIMARY KEY, name VARCHAR,
    username VARCHAR, email VARCHAR,
    password_hash VARCHAR, registered_on timestamp
    )
    """
QUERY2 = """
    CREATE TABLE IF NOT EXISTS questions(
    id serial PRIMARY KEY,
    title VARCHAR, description VARCHAR,
    created_by INTEGER,
    answers INTEGER, date_created timestamp,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE CASCADE
    )
    """

QUERY3 = """
    CREATE TABLE IF NOT EXISTS answers(
    id serial PRIMARY KEY,
    answer VARCHAR, accepted BOOL, votes INTEGER,
    owner INTEGER REFERENCES users(id) ON DELETE CASCADE,
    question INTEGER REFERENCES questions(id) ON DELETE CASCADE,
    date_created timestamp
    )
    """
