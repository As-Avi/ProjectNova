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
         return ComboOut(label="Label", values=["Gruppo 1", "Gruppo 2", "Gruppo 3", "Gruppo 4", "Gruppo 5", "Gruppo 6", "Gruppo 7", "Gruppo 8", "Gruppo 9", "Gruppo 10"])