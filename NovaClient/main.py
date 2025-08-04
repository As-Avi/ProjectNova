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
    '''
    parser = argparse.ArgumentParser(description="Strumento per gestire progetti.")
    subparsers = parser.add_subparsers(dest="command", help="Sottocomandi disponibili")

    parser_init = subparsers.add_parser("init", help="Inizializza un nuovo progetto")
    parser_init.add_argument("--Title", type=str, help="Titolo")

    # Sottoparser per 'run'
    parser_run = subparsers.add_parser("run", help="Esegui un'azione")
    parser_run.add_argument("--input", type=str, required=True, help="File di input")
    parser_run.add_argument("--verbose", action="store_true", help="Abilita output dettagliato")

    # Parsing degli argomenti
    args = parser.parse_args()

    # Gestione dei comandi
    if args.command == "init":
        print(f"Inizializzazione progetto: {args.name}")
    elif args.command == "run":
        print(f"Esecuzione con input: {args.input} (verbose={args.verbose})")
    else:
        parser.print_help()  # Mostra help se nessun comando è specificato
    '''
    # leggo i parametri dalla linea di comando
    Title = sys.argv[1]  # Title
    param_2 = sys.argv[2]  # url
    param_3 = sys.argv[3]  # file json
    param_4 = sys.argv[4]  # language

    # compongo l'url con i parametri che mi serviranno lato server
    Url = param_2 + "?config=" + param_3 + "&language=" + param_4

    # creo la form
    App(Title, Url)