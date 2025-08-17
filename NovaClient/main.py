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
        "-u", "--url", type=str, required=True, help="URL del server [obbligatorio]"
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        required=True,
        help="File JSON di configurazione [obbligatorio]",
    )

    parser.add_argument("-i", "--input", action="store_true", help="Mostra finestra configurazione credenziali [opzionale]", default=False)

    args = parser.parse_args()

    # Default settings based on the user's environment.
    locale.setlocale(locale.LC_ALL, "")
    language, _ = locale.getlocale()
    user_lang = language.split("_")[0]

    if args.input:
        from credentials_config import show_credentials_dialog
        # Usa l'URL fornito per testare le credenziali
        test_url = args.url + "/api"
        if not show_credentials_dialog(test_url):
            sys.exit(0)

    # creo la form
    try:
        App(args.url, args.file, user_lang)
    except Exception as e:
        error_msg = str(e)
        if "Credenziali non trovate" in error_msg or "401" in error_msg or "Unauthorized" in error_msg or "403" in error_msg:
            print("Errore di autenticazione rilevato. Apertura finestra credenziali...")
            from credentials_config import show_credentials_dialog
            test_url = args.url + "/api"
            while True:
                if show_credentials_dialog(test_url):
                    try:
                        # Riprova con le nuove credenziali
                        App(args.url, args.file, user_lang)
                        break  # Se arriva qui, l'autenticazione è andata a buon fine
                    except Exception as retry_error:
                        retry_msg = str(retry_error)
                        if "Credenziali non trovate" in retry_msg or "401" in retry_msg or "Unauthorized" in retry_msg or "403" in retry_msg:
                            continue  # Continua il loop per mostrare di nuovo la finestra
                        else:
                            print(f"Errore non relativo all'autenticazione: {retry_error}")
                            sys.exit(1)
                else:
                    print("Configurazione credenziali annullata.")
                    sys.exit(0)
        else:
            print(f"Errore generale: {e}")
            sys.exit(1)