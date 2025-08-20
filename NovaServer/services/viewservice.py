
from models.novaParams import ParInWithFilter, ParIn, ParOut, ComboOut
from repositories.SqlServer import SqlServer
from repositories.Csv import Csv


class viewservice:
    def __init__(self, data):
        self.data = data
        self.SQL_SERVER = "SqlServer"

    ############################################
    # Load Combo data
    ############################################
    def loadCombo(self):

        type = self.data["Type"]

        if type == self.SQL_SERVER:
            listOfData = self.__loadDataFilterSqlServer()
        elif type == "CSV":
            return ComboOut(label="Label", values=["Option 1", "Option 2", "Option 3"])
        else:
            raise Exception("Wrong Type")

        label = self.__getValue(self.data["Label"], "")

        return ComboOut(label=label, values=listOfData)

    ############################################
    # Load Combo data SQL Server
    ############################################
    def __loadDataFilterSqlServer(self):
        connectionString = self.data["ConnectionString"]
        query = self.data["QueryFilter"]

        sqlServer = SqlServer(connectionString)
        return sqlServer.loadDataFilterSqlServer(query)

    ############################################
    # Load data View
    ############################################
    def laodView(self, filter: str):
        type = self.data["Type"]

        if type == "SqlServer":
            df = self.__loadDataSqlServer(filter)
        elif type == "CSV":
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
            connectionString = self.data["ConnectionString"]
            query = self.data["Query"]

            where = self.__getValue(self.data["Filter"], "")

            sqlServer = SqlServer(connectionString)
            return sqlServer.loadDataSqlServer(query, where, filter)

        except Exception as e:
            raise Exception(e.args[1])

        return df

    ############################################
    # Load data View CSV file
    ############################################
    def __loadDataCSV(self):
        return Csv().loadDataCSV(self.data["File"])  # da migliorare gestione errore

    def __getValue(self, item, defaultValue="") -> str:
        try:
            return item
        except:
            return defaultValue
