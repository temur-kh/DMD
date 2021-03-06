###################################################
# Tabbed interface script
# www.sunjay-varma.com
###################################################

__doc__ = info = '''
This script was written by Sunjay Varma - www.sunjay-varma.com
This script has two main classes:
Tab - Basic tab used by TabBar for main functionality
TabBar - The tab bar that is placed above tab bodies (Tabs)
It uses a pretty basic structure:
root
-->TabBar(root, init_name) (For switching tabs)
-->Tab    (Place holder for content)
    -->content (content of the tab; parent=Tab)
-->Tab    (Place holder for content)
    -->content (content of the tab; parent=Tab)
-->Tab    (Place holder for content)
    -->content (content of the tab; parent=Tab)
etc.

The module was modified by Temur Kholmatov, email: t.holmatov@innopolis.ru
'''

from tkinter import *

BASE = RAISED
SELECTED = FLAT


# a base tab class
class Tab(Frame):
    def __init__(self, master, name):
        Frame.__init__(self, master)
        self.tab_name = name


# the bulk of the logic is in the actual tab bar
class TabBar(Frame):
    def __init__(self, master, name, init_name=None):
        Frame.__init__(self, master)
        self.tab_name = name
        self.tabs = {}
        self.buttons = {}
        self.current_tab = None
        self.init_name = init_name

    def show(self):
        self.pack(side=TOP, expand=YES, fill=Y)
        self.switch_tab(self.init_name or list(self.tabs.keys())[-1])  # switch the tab to the first tab

    def add(self, tab, btn_config=None):
        tab.pack_forget()  # hide the tab on init

        self.tabs[tab.tab_name] = tab  # add it to the list of tabs
        b = Button(self, text=tab.tab_name, relief=BASE,  # basic button stuff
                   command=(lambda name=tab.tab_name: self.switch_tab(name)))  # set the command to switch tabs
        if btn_config:
            b.config(**btn_config)
        if isinstance(tab, TabBar):
            b.pack(side=LEFT, fill=X)  # pack the button to the left mose of self
        else:
            b.pack(side=TOP, fill=X)
        self.buttons[tab.tab_name] = b  # add it to the list of buttons

    def delete(self, tabname):

        if tabname == self.current_tab:
            self.current_tab = None
            self.tabs[tabname].pack_forget()
            del self.tabs[tabname]
            self.switch_tab(list(self.tabs.keys())[0])

        else:
            del self.tabs[tabname]

        self.buttons[tabname].pack_forget()
        del self.buttons[tabname]

    def switch_tab(self, name):
        if self.current_tab:
            self.buttons[self.current_tab].config(relief=BASE)
            self.tabs[self.current_tab].pack_forget()  # hide the current tab
            # if exists, hide tabs of sub-bars
            if hasattr(self.tabs[self.current_tab], 'tabs'):
                for tab in self.tabs[self.current_tab].tabs:
                    self.tabs[self.current_tab].tabs[tab].pack_forget()
        self.tabs[name].pack(side=LEFT)  # add the new tab to the display
        # if exists, show tabs of sub-bars
        if hasattr(self.tabs[name], 'show'):
            self.tabs[name].show()
        self.current_tab = name  # set the current tab to itself

        self.buttons[name].config(relief=SELECTED)  # set it to the selected style
