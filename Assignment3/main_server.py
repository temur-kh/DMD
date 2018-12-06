"""
Main module cannot be used without a remote server with MySQL and a database 'company'.
"""

import mysql.connector

from sample_data.sample_database import SampleDatabase
from faker import Faker
import tkinter as tk
from gui_application.window import ApplicationWindow

user = "user1"
pswd = "dmd@assignment@3"
db = "company"

print("Input remote host server IP: ", end="")
remote_host = input()

conn = mysql.connector.connect(
    host=remote_host,
    user=user,
    passwd=pswd,
    database=db
)

fake = Faker()
database = SampleDatabase(conn, fake)

root = tk.Tk()
root.wm_title("DMD Assignment 3")
window = ApplicationWindow(root, database)
window.pack()
tk.mainloop()
