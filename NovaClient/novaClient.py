import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
import requests
from pandas.io.json import read_json
import sys
from io import StringIO
import os
import json
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

from tkinter.messagebox import showinfo


# This is a simple Tkinter application to display data from a JSON endpoint in a table format.
class App(tk.Tk):
    def __init__(self, title, url, file, language):
        self.url = url
        self.name = title
        self.file = file
        self.language = language
        self.config_file = "window_config.json"  # File per salvare le impostazioni
        self.ComboList = None
        self.endpoint_combo = None
        self.treeview = None

        tk.Tk.__init__(self)

        self.title(title)

        # Carica le dimensioni e posizione salvate
        self.load_window_config()

        # Intercetta l'evento di chiusura della finestra
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # per catturare l'evento key press
        self.bind("<Key>", self.key_press)
        # self.bind("<Motion>", self.change_cursor)

        # loadata from server for combo
        ######################################################
        self.loadDataCombo()
        ######################################################

        # chiamata al server per caricare i dati per caricare il combobox
        self.prepare()
        self.loadView(False)
        self.mainloop()

    # Prepare the main frame and treeview for displaying data
    def prepare(self):
        self.frame = ttk.Frame(self)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        # create of a combo box for selecting endpoints/filters
        self.toolbar_frame = ttk.Frame(self.frame)
        self.toolbar_frame.pack(fill=tk.X, pady=(0, 10))
        # Combobox for endpoint selection
        if self.ComboList is not None:
            ttk.Label(
                self.toolbar_frame,
                text="Piano di spedizione:",
                font=("Arial", 12, "bold"),
            ).pack(side=tk.LEFT, padx=(0, 5))

            self.endpoint_combo = ttk.Combobox(
                self.toolbar_frame,
                values=self.ComboList,
                width=20,
                font=("Arial", 12),
                state="readonly",
            )
            self.endpoint_combo.pack(side=tk.LEFT, padx=(0, 10))

        button = tk.Button(
            self.toolbar_frame,
            text="Carica Dati (F10)",
            command=self.button_clicked,
            activebackground="blue",
            activeforeground="white",
            anchor="center",
            bd=3,
            bg="lightgray",
            cursor="hand2",
            disabledforeground="gray",
            fg="black",
            font=("Arial", 12),
            height=1,
            highlightbackground="black",
            highlightcolor="green",
            highlightthickness=2,
            # justify="right",
            overrelief="raised",
            padx=0,
            pady=0,
            width=15,
            wraplength=0,
        )

        button.pack(padx=20, pady=20)

        # Create a container frame for the treeview
        self.tree_frame = ttk.Frame(self.frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)
        # create a label with info about the F10 key
        self.info_label = ttk.Label(
            self.tree_frame,
            text="Premi F1 per l'help, F3 per la ricerca e F10 per aggiornare i dati",
        )
        self.info_label.grid(row=2, column=0, columnspan=2, pady=5)

    def button_clicked(self):
        self.loadView(True)

    # Load window configuration from file
    def load_window_config(self):
        # Carica la configurazione della finestra dal file JSON
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, "r") as f:
                    config = json.load(f)

                # Imposta geometria (dimensioni e posizione)
                width = config.get("width", 1200)
                height = config.get("height", 500)
                x = config.get("x", 100)
                y = config.get("y", 100)

                # Verifica che le coordinate non siano fuori schermo
                screen_width = self.winfo_screenwidth()
                screen_height = self.winfo_screenheight()

                if x < 0 or x > screen_width - 100:
                    x = 100
                if y < 0 or y > screen_height - 100:
                    y = 100

                self.geometry(f"{width}x{height}+{x}+{y}")

                # Ripristina stato finestra (normale/massimizzata)
                if config.get("maximized", False):
                    self.state("zoomed")  # Linux/Windows

            else:
                # Valori di default se il file non esiste
                self.geometry("1200x500+100+100")

        except Exception as e:
            print(f"Errore nel caricamento configurazione: {e}")
            self.geometry("1200x500+100+100")

    def save_window_config(self):
        # Salva la configurazione attuale della finestra nel file JSON
        try:
            # Ottieni dimensioni e posizione attuali
            geometry = self.geometry()

            # Parse della stringa geometry (es: "1200x500+100+50")
            size_part, pos_part = geometry.split("+", 1)
            width, height = map(int, size_part.split("x"))

            # La posizione può avere segni negativi
            pos_parts = pos_part.replace("-", "+-").split("+")
            x = int(pos_parts[0]) if pos_parts[0] else int(pos_parts[1])
            y = int(pos_parts[-1])

            config = {
                "width": width,
                "height": height,
                "x": x,
                "y": y,
                "maximized": self.state() == "zoomed",
            }

            with open(self.config_file, "w") as f:
                json.dump(config, f, indent=2)

        except Exception as e:
            print(f"Errore nel salvataggio configurazione: {e}")

    def on_closing(self):
        # Salva la configurazione prima di chiudere
        self.save_window_config()
        # Chiudi l'applicazione
        self.destroy()

    # Load data from the specified URL
    def loadDataCombo(self):
        try:
            if self.url.startswith("http"):
                self.ComboList = self.loadJsonFromUrl(
                    self.url
                    + "/api/combo"
                    + "?config="
                    + self.file
                    + "&language="
                    + self.language
                )
                return True
            else:
                messagebox.showerror(
                    title="Error",
                    message=f"Invalid URL format. Please provide a valid URL starting with 'http'.",
                )
                return False

                # raise ValueError(
                #     "Invalid URL format. Please provide a valid URL starting with 'http'."
                # )
        except Exception as e:
            messagebox.showerror(title="Error", message=f"Error loading data: {e}")
            return False

    # Load data from the specified URL
    def loadData(self, filter: str):
        try:
            if self.url.startswith("http"):
                self.df = self.loadDataFromUrl(
                    self.url
                    + "/api/view"
                    + "?config="
                    + self.file
                    + "&language="
                    + self.language
                    + "&filter="
                    + filter
                )
                return True
            else:
                messagebox.showerror(
                    title="Error",
                    message=f"Invalid URL format. Please provide a valid URL starting with 'http'.",
                )
                return False

                # raise ValueError(
                #     "Invalid URL format. Please provide a valid URL starting with 'http'."
                # )
        except Exception as e:
            messagebox.showerror(title="Error", message=f"Error loading data: {e}")
            return False

    # Start the main form and display the data
    def loadView(self, cleanData=False):
        self.change_cursor(True)

        if cleanData:
            self.clean()

        ######################################################
        if self.endpoint_combo is not None:
            filter = self.endpoint_combo.get()
        else:
            filter = ""

        ret = self.loadData(filter)
        ######################################################
        if ret == False:
            return
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

    # Function to change the cursor style
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
        a = 0
        for dt in r_set:
            a = a + 1
            v = [r for r in dt]
            # qua aggiungere filtro con tkinter
            if a % 2 == 0:
                treeview.insert("", tk.END, values=v, tags=("oddrow",))
            else:
                treeview.insert("", tk.END, values=v, tags=("evenrow",))

        treeview.tag_configure("oddrow", background="whitesmoke")
        treeview.tag_configure("evenrow", background="white")

    # Function to load data from a URL
    def loadDataFromUrl(self, url):
        secret_user = os.getenv("USER")
        secret_password = os.getenv("PWD")
        version = os.getenv("VERSION")
        response = requests.get(
            url,
            auth=HTTPBasicAuth(secret_user, secret_password),
            verify=False,
            headers={"header-version": version},
        )
        if response.status_code == 200:
            data = response.json()
            return read_json(StringIO(data))
        else:
            raise Exception(
                f"Failed to fetch data from URL: {response.url} code: {response.status_code} message: {response.text}"
            )

    def loadJsonFromUrl(self, url):
        secret_user = os.getenv("USER")
        secret_password = os.getenv("PWD")
        version = os.getenv("VERSION")
        response = requests.get(
            url,
            auth=HTTPBasicAuth(secret_user, secret_password),
            verify=False,
            headers={"header-version": version},
        )
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            raise Exception(
                f"Failed to fetch data from URL: {response.url} code: {response.status_code} message: {response.text}"
            )

    # Function to handle key press events
    def key_press(self, event):
        if event.keysym == "F1":  # F1 HELP
            print("F1 is pressed")
        elif event.keysym == "F3":  # F3 CERCA
            print("F3 is pressed")
            self.popup_find()
        elif event.keysym == "F10":  # F10 REFRESH
            self.loadView(True)

    # Function to clean the Treeview
    def clean(self):
        if self.treeview is not None:
            for i in self.treeview.get_children():
                self.treeview.delete(i)

    def popup_find(self):
        win = tk.Toplevel(self)
        win.geometry("300x200")
        win.wm_title("Window")

        e1 = tk.Entry(win)
        e1.grid(row=0, column=0)

        tk.Button(win, text="Find", command=self.clean).grid(
            row=1, column=0, sticky=tk.W
        )
