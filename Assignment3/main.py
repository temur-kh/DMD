import mysql.connector

from create_tables import create_database
from sample_data.sample_database import SampleDatabase
from faker import Faker
import tkinter as tk
from gui_application.window import ApplicationWindow

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="test"
)

create_database(conn)

fake = Faker()
database = SampleDatabase(conn, fake)
# database.create_data()  # uncomment if need to create sample data
# database.upload()       # uncomment if need to upload sample data
root = tk.Tk()
root.wm_title("DMD Assignment 3")
window = ApplicationWindow(root, database)
window.pack()
tk.mainloop()


