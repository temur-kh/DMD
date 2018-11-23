import mysql.connector

from create_tables import create_database
from sample_data.sample_database import SampleDatabase
from faker import Faker

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="test"
)

create_database(conn)

fake = Faker()
database = SampleDatabase(conn, fake)
database.upload()
