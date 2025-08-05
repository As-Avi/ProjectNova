import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
import requests
from pandas.io.json import read_json
import sys
from io import StringIO
import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

from tkinter.messagebox import showinfo

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

        #chiamata al server per caricare i dati per caricare il combobox
        self.prepare()
        self.startForm()
        self.mainloop()

    # Prepare the main frame and treeview for displaying data
    def prepare(self):
        self.frame = ttk.Frame(self)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        #create of a combo box for selecting endpoints/filters
        self.toolbar_frame = ttk.Frame(self.frame)
        self.toolbar_frame.pack(fill=tk.X, pady=(0, 10))
        # Combobox for endpoint selection
        ttk.Label(self.toolbar_frame, text="Piano di spedizione:", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=(0, 5))
        self.endpoint_combo = ttk.Combobox(self.toolbar_frame, values=["PDS2025000000123", "PDS2025000000456", "PDS2025000000789"], width=20, font=("Arial", 12), state="readonly")
        self.endpoint_combo.pack(side=tk.LEFT, padx=(0, 10))
        # Create a container frame for the treeview
        self.tree_frame = ttk.Frame(self.frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)
        #create a label with info about the F10 key
        self.info_label = ttk.Label(self.tree_frame, text="Premi F1 per l'help, F3 per la ricerca e F10 per aggiornare i dati")
        self.info_label.grid(row=2, column=0, columnspan=2, pady=5)

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
                return True
            else:
                messagebox.showerror(title="Error", message=f"Invalid URL format. Please provide a valid URL starting with 'http'.")
                return False

                # raise ValueError(
                #     "Invalid URL format. Please provide a valid URL starting with 'http'."
                # )
        except Exception as e:
            messagebox.showerror(title="Error", message=f"Error loading data: {e}")
            return False

    # Start the main form and display the data
    def startForm(self):
        self.change_cursor(True)
        ret = self.loadData()
        if ret == False: return
        # generate layout table with columns and header
        self.generateLayout(self.tree_frame, self.df)

        # show data in table
        self.showData(self.treeview, self.df)

        # create a vertical scrollbar
        v_scrollbar = ttk.Scrollbar(
            self.tree_frame, orient=tk.VERTICAL, command=self.treeview.yview
        )
        self.treeview.configure(yscrollcommand=v_scrollbar.set)

        # create a horizontal scrollbar
        h_scrollbar = ttk.Scrollbar(
            self.tree_frame, orient=tk.HORIZONTAL, command=self.treeview.xview
        )
        self.treeview.configure(xscrollcommand=h_scrollbar.set)

        # grid the widgets
        self.treeview.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        # configure the grid weights
        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)
        
        # Force update to ensure proper scrollbar initialization
        self.tree_frame.update_idletasks()

        self.change_cursor(False)

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
            # Set a minimum width for each column to ensure horizontal scrolling works
            self.treeview.column(c, minwidth=100, width=120)

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
            #qua aggiungere filtro con tkinter 
            treeview.insert("", tk.END, values=v)

    # Function to load data from a URL
    def loadDataFromUrl(self, url):
        secret_user = os.getenv("USER")
        secret_password = os.getenv("PWD")
        version = os.getenv("VERSION")
        response = requests.get(url, auth=HTTPBasicAuth(secret_user, secret_password), verify=False, headers={"header-version":version})
        if response.status_code == 200:
            data = response.json()
            return read_json(StringIO(data))
        else:
            raise Exception(
                f"Failed to fetch data from URL: {response.url} code: {response.status_code} message: {response.text}"
            )

    # Function to handle key press events
    def key_press(self, event):
        if event.keysym == "F1":#F1 HELP
            print("F1 is pressed")
        elif event.keysym == "F3":#F3 CERCA
            print("F3 is pressed")
            self.popup_find()
        elif event.keysym == "F10":#F10 REFRESH
            self.clean()
            self.startForm()

    # Function to clean the Treeview
    def clean(self):
        for i in self.treeview.get_children():
            self.treeview.delete(i)

    def popup_find(self):
        win = tk.Toplevel(self)
        win.geometry("300x200")
        win.wm_title("Window")

        e1 = tk.Entry(win)
        e1.grid(row=0, column=0)

        tk.Button(win, text='Find', command=self.clean).grid(row=1, column=0, sticky=tk.W)

