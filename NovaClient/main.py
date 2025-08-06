import sys
from io import StringIO
import os
from dotenv import load_dotenv
import argparse

from novaClient import App

# Function Min to run the application
if __name__ == "__main__":
    print(sys.argv)

    #leggo i parametri dal file .env
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Parametri da inserire.")
   
    parser.add_argument("-t", "--title", type=str, required=True, help="Titolo del progetto [obbligatorio]")
    parser.add_argument("-u", "--url", type=str, required=True, help="URL del server [obbligatorio]")
    parser.add_argument("-f", "--file", type=str, required=True, help="File JSON di configurazione [obbligatorio]")
    parser.add_argument("-l", "--language", type=str, required=True, help="Lingua del progetto [opzionale, default: 'it']", default="it")

    args = parser.parse_args()

    Title = args.title
    param_2 = args.url
    param_3 = args.file
    param_4 = args.language

    # compongo l'url con i parametri che mi serviranno lato server
    #Url = param_2 + "?config=" + param_3 + "&language=" + param_4

    # creo la form
    App(Title, args.url, args.file,  args.language)