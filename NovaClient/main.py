
# sudo apt install python3-tk
# pip install -r requirements.txt
# plus2net.com/python/tkinter-df-search.php
# https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver16&tabs=ubuntu18-install%2Calpine17-install%2Cdebian8-install%2Credhat7-13-install%2Crhel7-offline

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
import requests
from pandas.io.json import read_json
import sys
from io import StringIO
from requests.auth import HTTPBasicAuth


# This is a simple Tkinter application to display data from a JSON endpoint in a table format.
class App(tk.Tk):
    def __init__(self, title, url):
        self.url = url
        self.name = title

        tk.Tk.__init__(self)

        self.title(title)

        self.geometry(self.getWindowsSize())

        # per catturare l'evento key press
        self.bind("<Key>", self.key_press)
        # self.bind("<Motion>", self.change_cursor)

        self.prepare()
        self.startForm()

    # Prepare the main frame and treeview for displaying data
    def prepare(self):
        self.frame = ttk.Frame(self)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        # Create a container frame for the treeview
        self.tree_frame = ttk.Frame(self.frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)

    # TODO: la stringa 1200x500 deve essere presa da un file
    # che si crea la momento della chiusura della form
    # se non esiste il file lo creo con i valori di default 1200x500
    def getWindowsSize(self):
        return "1200x500"

    # Load data from the specified URL
    def loadData(self):
        try:
            if self.url.startswith("http"):
                self.df = self.loadDataFromUrl(self.url)

                for c in self.df.columns:
                    if set(self.df[c].unique()).issubset({0, 1}):
                        self.df[c] = self.df[c].astype(bool)

                # non bisognerebbe fare pulizia del dataframe? Se ho elementi nulli, oppure se ho 1/0 al posto di True/False?
                # df = df.dropna()
            else:
                raise ValueError(
                    "Invalid URL format. Please provide a valid URL starting with 'http'."
                )
        except Exception as e:
            messagebox.showerror(title="Error", message=f"Error loading data: {e}")

    # Start the main form and display the data
    def startForm(self):
        self.change_cursor(True)
        self.loadData()

        # generate layout table with columns and header
        self.generateLayout(self.tree_frame, self.df)

        # show data in table
        self.showData(self.treeview, self.df)

        # # create a vertical scrollbar
        v_scrollbar = ttk.Scrollbar(
            self.tree_frame, orient=tk.VERTICAL, command=self.treeview.yview
        )
        self.treeview.configure(yscrollcommand=v_scrollbar.set)

        # # create a horizontal scrollbar
        h_scrollbar = ttk.Scrollbar(
            self.tree_frame, orient=tk.HORIZONTAL, command=self.treeview.xview
        )
        self.treeview.configure(xscrollcommand=h_scrollbar.set)

        # # pack the scrollbar
        self.treeview.grid(row=0, column=0, sticky="nsew")

        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        # # configure the grid
        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)

        self.change_cursor(False)
        self.mainloop()

    #Function to change the cursor style
    def change_cursor(self, event):
        try:
            if event == True:
                self.config(cursor="circle")
            else:
                self.config(cursor="arrow")
        finally:
            pass

    # Function to generate the layout of the Treeview
    def generateLayout(self, frame, df):
        l1 = list(df)
        self.treeview = ttk.Treeview(frame, columns=(l1), show="headings")

        for c in l1:
            self.treeview.heading(
                c,
                text=c,
                command=lambda c=c: self.sort_treeview(self.treeview, c, False),
            )

    # Function to sort the Treeview by column
    def sort_treeview(self, tree, col, descending):
        data = [(tree.set(item, col), item) for item in tree.get_children("")]
        data.sort(reverse=descending)
        for index, (val, item) in enumerate(data):
            tree.move(item, "", index)
        tree.heading(col, command=lambda: self.sort_treeview(tree, col, not descending))

    # Insert data into the Treeview
    def showData(self, treeview, df):
        r_set = df.to_numpy().tolist()
        for dt in r_set:
            v = [r for r in dt]
            treeview.insert("", tk.END, values=v)

    # Function to load data from a URL
    def loadDataFromUrl(self, url):
        response = requests.get(url, auth=HTTPBasicAuth("test", "test"), verify=False)
        if response.status_code == 200:
            data = response.json()
            return read_json(StringIO(data))
        else:
            raise Exception(
                f"Failed to fetch data from URL: {response.url} code: {response.status_code} message: {response.text}"
            )

    # Function to handle key press events
    def key_press(self, event):
        if event.keycode == 112:
            print("F1 is pressed")
        elif event.keycode == 114:
            print("F3 is pressed")
        elif event.keycode == 121:
            print("F10 is pressed")   
            self.startForm()

    # Function to clean the Treeview
    def clean(self):
        for i in self.treeview.get_children():
            self.treeview.delete(i)


# Function Min to run the application
if __name__ == "__main__":

    print(sys.argv)

    # leggo i parametri dalla linea di comando
    Title = sys.argv[1]  # Title
    param_2 = sys.argv[2]  # url
    param_3 = sys.argv[3]  # file json
    param_4 = sys.argv[4]  # language

    # compongo l'url con i parametri che mi serviranno lato server
    Url = param_2 + "?config=" + param_3 + "&language=" + param_4

    # creo la form
    App(Title, Url)