import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="test",
    passwd="test",
    database="company"
)
