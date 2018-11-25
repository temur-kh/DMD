import mysql.connector
from mysql.connector import errorcode
import getpass
from create_tables import *
from sample_data.sample_database import SampleDatabase
from faker import Faker
import tkinter as tk
from gui_application.window import ApplicationWindow

print("Input MySQL user name: ")
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
      "\n Want to Load from backup file? Enter 2;"
      "\n Want just to run gui? Enter 3: ")
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
else:
    raise ValueError("Incorrect input!")

root = tk.Tk()
root.wm_title("DMD Assignment 3")
window = ApplicationWindow(root, database)
window.pack()
tk.mainloop()


