import sys
from io import StringIO
import os
from dotenv import load_dotenv
import argparse
import locale

from novaClient import App

# Function Min to run the application
if __name__ == "__main__":
    print(sys.argv)

    # leggo i parametri dal file .env
    load_dotenv()

    parser = argparse.ArgumentParser(description="Parametri da inserire.")

    parser.add_argument(
        "-m",
        "--modulo",
        type=str,
        required=True,
        help="Modulo 0 = VIEW | 1 = FILTEREDVIEW [obbligatorio]",
    )
    parser.add_argument(
        "-u", "--url", type=str, required=True, help="URL del server [obbligatorio]"
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        required=True,
        help="File JSON di configurazione [obbligatorio]",
    )

    args = parser.parse_args()

    # Default settings based on the user's environment.
    locale.setlocale(locale.LC_ALL, "")
    language, _ = locale.getlocale()
    user_lang = language.split("_")[0]

    # creo la form
    App(args.modulo, args.url, args.file, user_lang)