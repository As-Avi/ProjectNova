
from models.novaParams import ParInWithFilter, ParIn, ParOut, ComboOut
from repositories.SqlServer import SqlServer
from repositories.Csv import Csv

from utilities.misc import DataSafe

from enum import Enum, IntEnum


class DataSourceType(Enum):
    SQL_SERVER = "SqlServer"
    CSV = "CSV"


class viewservice:
    def __init__(self, data):
        self.SQL_SERVER = DataSourceType.SQL_SERVER.value
        self.CSV = DataSourceType.CSV.value

        self.data = data
        self.module = self.data["Module"] # 0 | 1 | 2
        self.type = self.data["Type"] # SqlServer | CSV

        self.connectionString = DataSafe().getValueString(self.data, "ConnectionString")
        self.query = DataSafe().getValueString(self.data, "Query")
        self.where = DataSafe().getValueString(self.data, "Filter")

    ############################################
    # Load Combo data
    ############################################
    def loadCombo(self):
        if self.type == self.SQL_SERVER:
            listOfData = self.__loadDataFilterSqlServer()
        elif self.type == self.CSV:
            return Csv().loadComboCSV()
        else:
            raise Exception("Wrong Type")

        label = DataSafe().getValueString(self.data, "Label")

        return ComboOut(label=label, values=listOfData)

    ############################################
    # Load Combo data SQL Server
    ############################################
    def __loadDataFilterSqlServer(self):
        sqlServer = SqlServer(self.connectionString)
        queryFilter = DataSafe().getValueString(self.data, "QueryFilter")
        return sqlServer.loadDataFilterSqlServer(queryFilter)

    ############################################
    # Load data View
    ############################################
    def laodView(self, filter: str):
        if self.type == self.SQL_SERVER:
            df = self.__loadDataSqlServer(filter)
        elif self.type == self.CSV:
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
        sqlServer = SqlServer(self.connectionString)
        return sqlServer.loadDataSqlServer(self.query, self.where, filter)

    ############################################
    # Load data View CSV file
    ############################################
    def __loadDataCSV(self):
        return Csv().loadDataCSV(self.data["File"])  # da migliorare gestione errore
