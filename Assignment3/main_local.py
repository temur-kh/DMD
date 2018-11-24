import mysql.connector
from mysql.connector import errorcode
import getpass
from create_tables import create_database
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
create_database(conn)

fake = Faker()
database = SampleDatabase(conn, fake)
database.create_data()  # uncomment if need to create sample data
database.upload()       # uncomment if need to upload sample data
root = tk.Tk()
root.wm_title("DMD Assignment 3")
window = ApplicationWindow(root, database)
window.pack()
tk.mainloop()


