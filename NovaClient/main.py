#sudo apt install python3-tk
#pip install tk
#pip install pandas
#plus2net.com/python/tkinter-df-search.php
#https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver16&tabs=ubuntu18-install%2Calpine17-install%2Cdebian8-install%2Credhat7-13-install%2Crhel7-offline

import tkinter as tk
from tkinter import ttk
import pandas as pd
import seaborn as sns
import PySimpleGUI as sg
import requests
from pandas.io.json import read_json

def startForm(name, urls):
    root = tk.Tk()
    root.title(name)
    root.geometry("1200x500")

    # Create a frame to hold the treeview and scrollbars
    frame = ttk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Create a container frame for the treeview
    tree_frame = ttk.Frame(frame)
    tree_frame.pack(fill=tk.BOTH, expand=True)

    try:
        if urls.startswith('http'):
            df = loadDataFromUrl(url)
        else:
            raise ValueError("Invalid URL format. Please provide a valid URL starting with 'http'.")
    except Exception as e:
        print(f"Error loading data: {e}")
        df = sns.load_dataset("titanic")  #dataset casuale, poi modifichiamo 

    #non bisognerebbe fare pulizia del dataframe? Se ho elementi nulli, oppure se ho 1/0 al posto di True/False?
    df = df.dropna()  
    
    for c in df.columns:
        if set(df[c].unique()).issubset({0,1}):
            df[c] = df[c].astype(bool)

    #generate layout table with columns and header
    treeview = generateLayout(tree_frame, df)

    #show data in table
    showData(treeview, df)

    #create a vertical scrollbar
    v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=treeview.yview)
    treeview.configure(yscrollcommand=v_scrollbar.set)

    #create a horizontal scrollbar
    h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=treeview.xview)
    treeview.configure(xscrollcommand=h_scrollbar.set)

    #pack the scrollbar
    treeview.grid(row=0, column=0, sticky='nsew')
    v_scrollbar.grid(row=0, column=1, sticky="ns")
    h_scrollbar.grid(row=1, column=0, sticky="ew")
    #v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    #h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

    #configure the grid
    tree_frame.grid_rowconfigure(0, weight=1)
    tree_frame.grid_columnconfigure(0, weight=1)
    
    #pack the frame
    frame.pack(fill=tk.BOTH,expand=True, padx=10, pady=10)

    root.mainloop()


def generateLayout(frame, df):
    l1 = list(df)
    treeview = ttk.Treeview(frame, columns=(l1), show="headings")
    
    for c in l1:
        treeview.heading(c, text=c, command=lambda c=c: sort_treeview(treeview, c, False))    

    return treeview

# Function to sort the Treeview by column
def sort_treeview(tree, col, descending):
    data = [(tree.set(item, col), item) for item in tree.get_children('')]
    data.sort(reverse=descending)
    for index, (val, item) in enumerate(data):
        tree.move(item, '', index)
    tree.heading(col, command=lambda: sort_treeview(tree, col, not descending))


def showData(treeview, df):
    r_set = df.to_numpy().tolist()
    for dt in r_set:
        v = [r for r in dt]
        treeview.insert("", tk.END, values = v)


def loadDataFromUrl(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return read_json(data, compression='gzip')        
    else:
        raise Exception(f"Failed to fetch data from URL: {response.status_code}")


def input_layout():
    layout = [
    [sg.Text("Endpoint Server:"), sg.Input(key="-ENDPOINT-")],
    [sg.Text("ID Configurazione:"), sg.Input(key="-CONFIG-")],
    [sg.Text("Lingua:"), sg.Combo(["IT", "EN"], key="-LANG-")],
    [sg.Button("Avvia"), sg.Exit()]
    ]

    window = sg.Window("Configurazione", layout)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Exit"):
            break
        elif event == "Avvia":
            if not values['-ENDPOINT-'] or not values['-CONFIG-'] or not values['-LANG-']:
                sg.popup_error("Please fill in all fields.")
                continue
            if values['-ENDPOINT-'].startswith('http') is False:
                sg.popup_error("Endpoint must start with 'http'.")
                continue
            if not values['-CONFIG-'].isdigit():
                sg.popup_error("Configuration ID must be a number.")
                continue
            list = [values['-ENDPOINT-'], values['-CONFIG-'], values['-LANG-']]
            window.close()
            return list

    window.close()


if __name__ == "__main__":
    url = 'http://localhost:8000/api/view'
    lista = input_layout() #ottengo l'endpoint, l'id e la lingua
    startForm("Users", url)