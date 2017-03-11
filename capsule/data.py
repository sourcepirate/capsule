import re
import os
import six
import sqlite3
from os.path import expanduser
from prettytable import PrettyTable

GITHUB_URL_REGEX = r'(https|http)://(?P<hostname>\w+).com/(?P<author>.*)/(?P<repo>[a-zA-Z0-9-_]+)(.git)?'
GITHUB_COMPILED = re.compile(GITHUB_URL_REGEX)
GITHUB_DEFAULT_DB = expanduser("~/.capsule/data.db")
DB_CREATE_SQL = """
CREATE TABLE REPO (
    name  text primary key,
    url   text
);
"""
DB_INSERT_SQL = """
INSERT INTO REPO values (\"{}\", \"{}\");
"""

DB_QUERY_SQL = """
SELECT * FROM REPO WHERE name=\"{}\";
""" 

SELECT_SQL = """
SELECT * FROM REPO;
"""

class CapsuleException(Exception):
    pass

def _safe_create(db_path):
    """Creates folder safely"""
    path = os.path.dirname(db_path)
    if not os.path.exists(path):
        os.mkdir(path)

def is_db_exist(db_path=GITHUB_DEFAULT_DB):
    """
    checks whether the sqlite db exists in 
    the particular path
    Args:
      db_path: path to check
    Returns: a boolean
    """
    return os.path.exists(db_path)

def get_data_db(db_path=GITHUB_DEFAULT_DB):
    """
    checks whether the db exists or not
    if it is then return the connection 
    else create an new one with repo 
    table and returns the connection

    Args:
        db_path: path to check
    Returns:
        connection: An sqlite3 connection object
    """
    if is_db_exist(db_path=db_path):
        return sqlite3.connect(db_path)
    else:
        _safe_create(db_path=db_path)
        connection = sqlite3.connect(db_path)
        connection.execute(DB_CREATE_SQL)
        return connection

def db_execute(sql, args, db_path=GITHUB_DEFAULT_DB, commit=True):
    """
      executes the sql with replaced positional
      arguments from the string template

      Args:
        sql: SQL query template.
        args: Arguments to be replaced in.
        commit: To be commited
      Returns:
        cursor: Sqlite3 query cursor
    """
    try:
        conn = get_data_db(db_path=db_path)
        _replaced = sql.format(*args)
        cursor = conn.execute(_replaced)
        if commit:
            conn.commit()
        return cursor
    except sqlite3.IntegrityError:
        six.print_("Repo with the specified name already exist")
        return None

def get(name, db_path=GITHUB_DEFAULT_DB):
    """
    Gets the record from the sqlite3 database
    for the particular name

    Args:
      name: name of the repo or alias
      db_path: The path to look for the data.db
    Returns:
      record: record instance of sqlite3
    """
    if name is None:
        raise CapsuleException("No name specified")
    cursor = db_execute(DB_QUERY_SQL, [name], db_path=db_path, commit=False)
    return cursor.fetchone()

def set(url, name=None, db_path=GITHUB_DEFAULT_DB):
    """
      Sets the url and name or alias to the data.db
      lite.

      Args:
        url: url of the repository
        name: name or the repository or alias
      
      Returns:
        cursor: None if not results else sqlite3.cursor object
    """
    match = GITHUB_COMPILED.match(url)
    if not match:
        six.print_("Please specify only the valid urls")
        return None
    else:
        hostname = match.group('hostname')
        repo = match.group('repo')
        if hostname.lower() != "github":
            six.print_("Please specify only github repo urls")
            return None
        else:
            conn = get_data_db(db_path=db_path)            
            cursor = db_execute(DB_INSERT_SQL, [name or repo, url], db_path=db_path)
            if cursor:
                six.print_("Saved to capsule")
                return cursor

def get_list(db_path=GITHUB_DEFAULT_DB):
    """
      selects all the record from the database

      Args:
        db_path: path of the  repository

      Returns:
        Array of records
    """
    cursor = db_execute(SELECT_SQL, [], db_path=db_path)
    return cursor.fetchall()

def pp():
    records = get_list()
    table = PrettyTable()
    table.field_names = ["REPO", "URL"]
    for record in records:
        table.add_row(record)
    six.print_(table)