import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="test",
    database="company"
)
