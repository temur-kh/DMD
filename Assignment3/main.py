import mysql.connector

from create_tables import create_database

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="test"
)

create_database(db)
