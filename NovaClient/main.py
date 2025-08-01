#sudo apt install python3-tk
#pip install -r requirements.txt
#plus2net.com/python/tkinter-df-search.php
#https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver16&tabs=ubuntu18-install%2Calpine17-install%2Cdebian8-install%2Credhat7-13-install%2Crhel7-offline

import tkinter as tk
from tkinter import messagebox 
from tkinter import ttk
import pandas as pd
import requests
from pandas.io.json import read_json
import sys
from io import StringIO
from requests.auth import HTTPBasicAuth

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
        messagebox.showerror(title='Error', message=f"Error loading data: {e}")
        return

    #non bisognerebbe fare pulizia del dataframe? Se ho elementi nulli, oppure se ho 1/0 al posto di True/False?
    #df = df.dropna()  
    
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
    response = requests.get(url, auth=HTTPBasicAuth('test', 'test'), verify=False)
    if response.status_code == 200:
        data = response.json()
        return read_json(StringIO(data))        
    else:
        raise Exception(f"Failed to fetch data from URL: {response.url} code: {response.status_code} message: {response.text}")


if __name__ == "__main__":
    
    print(sys.argv)

    #leggo i parametri dalla linea di comando
    param_1 = sys.argv[1] #Title
    param_2 = sys.argv[2] #url
    param_3 = sys.argv[3] #file json
    param_4 = sys.argv[4] #language

    #compongo l'url con i parametri che mi serviranno lato server
    url = param_2 + '?config=' + param_3 + '&language=' + param_4

    #creo la form
    startForm(param_1, url)