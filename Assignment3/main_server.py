import mysql.connector

from sample_data.sample_database import SampleDatabase
from faker import Faker
import tkinter as tk
from gui_application.window import ApplicationWindow

remote_host = ""
user = ""
pswd = ""

conn = mysql.connector.connect(
    host=remote_host,
    user=user,
    passwd=pswd
)

fake = Faker()
database = SampleDatabase(conn, fake)

root = tk.Tk()
root.wm_title("DMD Assignment 3")
window = ApplicationWindow(root, database)
window.pack()
tk.mainloop()
