
from models.novaParams import ParInWithFilter, ParIn, ParOut, ComboOut
from repositories.SqlServer import SqlServer
from repositories.Csv import Csv

from utilities.misc import DataSafe

class viewservice:
    def __init__(self, data):
        self.data = data
        self.type = self.data["Type"]
        self.SQL_SERVER = "SqlServer"
        self.connectionString = self.data["ConnectionString"]
        self.query = self.data["Query"]
        self.where = DataSafe().getValueString(self.data, "Filter", "")

    ############################################
    # Load Combo data
    ############################################
    def loadCombo(self):
        if self.type == self.SQL_SERVER:
            listOfData = self.__loadDataFilterSqlServer()
        elif self.type == "CSV":
            return ComboOut(label="Label", values=["Option 1", "Option 2", "Option 3"])
        else:
            raise Exception("Wrong Type")

        label = DataSafe().getValueString(self.data, "Label", "")

        return ComboOut(label=label, values=listOfData)

    ############################################
    # Load Combo data SQL Server
    ############################################
    def __loadDataFilterSqlServer(self):
        sqlServer = SqlServer(self.connectionString)
        queryFilter = DataSafe().getValueString(self.data, "QueryFilter", "")
        return sqlServer.loadDataFilterSqlServer(queryFilter)

    ############################################
    # Load data View
    ############################################
    def laodView(self, filter: str):
        if self.type == "SqlServer":
            df = self.__loadDataSqlServer(filter)
        elif self.type == "CSV":
            df = self.__loadDataCSV()
        else:
            raise Exception("Wrong Type")

        if df is None:
            raise Exception("Empty Data Frame")

        return df.to_json(orient="records")

    ############################################
    # Load data View SQL Server
    ############################################
    def __loadDataSqlServer(self, filter):
        try:
            sqlServer = SqlServer(self.connectionString)
            return sqlServer.loadDataSqlServer(self.query, self.where, filter)

        except Exception as e:
            raise Exception(e.args[1])

        return df

    ############################################
    # Load data View CSV file
    ############################################
    def __loadDataCSV(self):
        return Csv().loadDataCSV(self.data["File"])  # da migliorare gestione errore

