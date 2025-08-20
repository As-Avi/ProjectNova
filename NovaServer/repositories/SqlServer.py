import pandas as pd
import pyodbc

class SqlServer:
     def __init__(self, connectionString: str):
        self.connectionString = connectionString

        
     ############################################
     # Query Data View
     ############################################
     def loadDataSqlServer(self, query: str, where: str, filter: str):
        cn = pyodbc.connect(self.connectionString)
        cursor = cn.cursor()

        sql = query + " " + where

        sql_final = sql.format(filter)

        df = pd.read_sql(
            sql_final, cn
        )  # warning perchè Sql server nonè un database nativo di pandas (usare SQLAlchemy)
        return df

     ############################################
     # Query Combo
     ############################################
     def loadDataFilterSqlServer(self, query: str):
        cn = pyodbc.connect(self.connectionString)
        cursor = cn.cursor()
        cursor.execute(query)
        results = []
        rows = cursor.fetchall()
        for row in rows:
            results.append(row[0])

        return results