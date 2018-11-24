import tkinter as tk
from .tkinter_tabs import *
from sample_data.sample_database import SampleDatabase
from pandastable import Table
from queries import get_all_query_results


class ApplicationWindow(tk.Frame):
    def __init__(self, master, database: SampleDatabase):
        tk.Frame.__init__(self, master)
        self.highlight_color = '#40A9CF'
        self.btn_config = {
            'background': 'white',
            'highlightbackground': self.highlight_color,
            'foreground': 'black',
        }
        self.default_config = {
            'background': 'white',
        }

        self.bar = TabBar(self, 'main_bar')
        self.bar.pack(side=TOP, expand=YES, fill=Y)
        queries_bar = TabBar(self, 'queries')
        tables_bar = TabBar(self, 'tables')

        left_side = tk.Frame(self)
        left_side.pack(side=RIGHT)
        right_side = tk.Frame(self)
        right_side.pack(side=LEFT)
        for db_table in database.tables:
            self.create_tab_with_table(tables_bar, left_side, db_table.name, db_table.get_dataframe())

        for query in get_all_query_results():
            self.create_tab_with_table(queries_bar, left_side, query['name'], query['dataframe'])

        self.set_config([self, left_side, right_side, queries_bar, tables_bar], self.default_config)
        self.bar.add(queries_bar, self.btn_config)
        self.bar.add(tables_bar, self.btn_config)
        self.bar.show()

    def create_tab_with_table(self, bar, master, name, df):
        tab = Tab(master, name)
        table = Table(parent=tab,
                      dataframe=df,  # get all rows from a table in DataFrame format
                      width=1600,
                      height=800,
                      editable=False,
                      cellwidth=1600 / len(df.columns),
                      rowheight=40)
        table.colselectedcolor = table.rowselectedcolor = self.highlight_color
        table.show()
        self.set_config([tab], self.default_config)
        bar.add(tab, self.btn_config)

    @staticmethod
    def set_config(widgets, config):
        """
        Sets the config of widgets
        :param widgets: widgets for changing the bg color
        :param config: configs to be set for widgets
        :return: None
        """
        for widget in widgets:
            widget.configure(**config)
