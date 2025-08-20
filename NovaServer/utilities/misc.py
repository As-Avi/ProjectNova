class DataSafe:
    def getValueString(self, item: any, filedName:str, defaultValue:str= "") -> str:
        try:
            return item[filedName]
        except:
            return defaultValue
