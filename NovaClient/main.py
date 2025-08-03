import sys
from io import StringIO
import os
from dotenv import load_dotenv

from novaClient import App

# Function Min to run the application
if __name__ == "__main__":
    print(sys.argv)

    #leggo i parametri dal file .env
    load_dotenv()

    # leggo i parametri dalla linea di comando
    Title = sys.argv[1]  # Title
    param_2 = sys.argv[2]  # url
    param_3 = sys.argv[3]  # file json
    param_4 = sys.argv[4]  # language

    # compongo l'url con i parametri che mi serviranno lato server
    Url = param_2 + "?config=" + param_3 + "&language=" + param_4

    # creo la form
    App(Title, Url)