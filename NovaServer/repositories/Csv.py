import pandas as pd
import pyodbc

class Csv: 
     def __init__(self):
        pass

     ############################################
     # Load Data from CSV
     ############################################
     def loadDataCSV(self, file: str):
        return pd.read_csv("data/" +file)