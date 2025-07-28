#sudo apt install python3-tk
#pip install tk
#pip install pandas
#plus2net.com/python/tkinter-df-search.php
#https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver16&tabs=ubuntu18-install%2Calpine17-install%2Cdebian8-install%2Credhat7-13-install%2Crhel7-offline

import tkinter as tk
from tkinter import ttk
import pandas as pd
import requests
from pandas.io.json import read_json

def startForm(name):
    root = tk.Tk()
    root.title(name)
    root.geometry("1200x500")

    frame = ttk.Frame(root)

    #load dataframe
    #df = loadData()
    df = loadDataFromUrl()

    #generate layout table with columns and header
    treeview = generateLayout(frame, df)

    #show data in table
    showData(treeview, df)

    #create a vertical scrollbar
    v_scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=treeview.yview)
    treeview.configure(yscrollcommand=v_scrollbar.set)

    #pack the treeview
    treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    #pack the scrollbar
    v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
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



def loadDataFromUrl():
    url = 'http://localhost:8000/api/view'

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return read_json(data, compression='gizp')        
    else:
        return None


if __name__ == "__main__":
    startForm("Users")