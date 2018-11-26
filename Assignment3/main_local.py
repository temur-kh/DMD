import mysql.connector
from mysql.connector import errorcode
import getpass
from create_tables import *
from sample_data.sample_database import SampleDatabase
from faker import Faker
import tkinter as tk
from gui_application.window import ApplicationWindow

print("Input MySQL user name: ", end="")
user = input()
pswd = getpass.getpass("Input password: ")
conn = None
try:
    conn = mysql.connector.connect(
        host="localhost",
        user=user,
        passwd=pswd
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    else:
        print(err)
    exit(0)

print("Want to create database with tables? Enter 1;"
      "\nWant to Load from backup file? Enter 2;"
      "\nWant just to run gui? Enter 3;"
      "\nWant to create sample database only? Enter 4: ", end="")
choice = int(input())
fake = Faker()

if choice == 1:
    create_database(conn)
    database = SampleDatabase(conn, fake)
    database.create_data()
    database.upload()
elif choice == 2:
    load_backup(conn)
    database = SampleDatabase(conn, fake)
elif choice == 3:
    database = SampleDatabase(conn, fake)
elif choice == 4:
    create_database(conn)
    database = SampleDatabase(conn, fake)
    database.create_data()
    database.upload()
    exit(0)
else:
    raise ValueError("Incorrect input!")

cursor = conn.cursor()
cursor.execute("USE `company`")
cursor.execute("SET GLOBAL sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''))")
cursor.close()

root = tk.Tk()
root.wm_title("DMD Assignment 3")
window = ApplicationWindow(root, database)
window.pack()
tk.mainloop()
