import pandas as pd
import pyodbc
from models.novaParams import ComboOut
class Csv: 
     def __init__(self):
        pass

     ############################################
     # Load Data from CSV
     ############################################
     def loadDataCSV(self, file: str):
        return pd.read_csv("data/" + file)

     def loadComboCSV(self):
         return ComboOut(label="Label", values=["Option 1", "Option 2", "Option 3"])