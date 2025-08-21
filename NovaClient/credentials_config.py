import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import requests
from requests.auth import HTTPBasicAuth

class Credentials:
    def __init__(self, username="", password=""):
        self.username = username
        self.password = password

class CredentialsDialog:
    def __init__(self, test_url=None):
        self.result = False
        self.credentials = Credentials()
        self.test_url = test_url  # URL per testare le credenziali
        
    def show_dialog(self):
        """Mostra la finestra di dialogo per inserire le credenziali"""
        self.root = tk.Tk()
        self.root.title("Configurazione Credenziali")
        self.root.geometry("450x350+200+200")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")  
        
        self.center_window()
        
        # Frame principale con padding e sfondo
        main_frame = tk.Frame(self.root, bg="#f0f0f0", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titolo con sfondo colorato
        title_frame = tk.Frame(main_frame, bg="#2c3e50", relief="raised", bd=2)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(title_frame, text="Inserisci le Credenziali", 
                              font=("Arial", 16, "bold"), bg="#2c3e50", fg="white", pady=10)
        title_label.pack()
        
        # Frame per i campi input
        input_frame = tk.Frame(main_frame, bg="#f0f0f0")
        input_frame.pack(fill=tk.X, pady=10)
        
        # Campo Username
        tk.Label(input_frame, text="Username:", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(anchor="w", pady=(0, 5))
        self.username_var = tk.StringVar(value="")  # Campo vuoto a ogni riavvio
        self.username_entry = tk.Entry(input_frame, textvariable=self.username_var, 
                                      font=("Arial", 12), width=30, relief="solid", bd=1)
        self.username_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Campo Password
        tk.Label(input_frame, text="Password:", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(anchor="w", pady=(0, 5))
        self.password_var = tk.StringVar(value="")  # Campo vuoto a ogni riavvio
        self.password_entry = tk.Entry(input_frame, textvariable=self.password_var, 
                                      show="*", font=("Arial", 12), width=30, relief="solid", bd=1)
        self.password_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Checkbox per mostrare password
        checkbox_frame = tk.Frame(input_frame, bg="#f0f0f0")
        checkbox_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.show_password_var = tk.BooleanVar()
        show_pass_check = tk.Checkbutton(checkbox_frame, text="Mostra password", 
                                        variable=self.show_password_var,
                                        command=self.toggle_password_visibility,
                                        bg="#f0f0f0", font=("Arial", 10))
        show_pass_check.pack(anchor="w")
        
        # Frame per i bottoni
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        # Bottone Invio - usando tk.Button invece di ttk.Button per miglior controllo
        save_btn = tk.Button(button_frame, text="Invio", 
                            command=lambda: self.test_credentials_validity(
                                self.username_entry.get(), 
                                self.password_entry.get()
                            ),  
                            bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
                            relief="raised", bd=2, padx=20, pady=8,
                            activebackground="#45a049", activeforeground="white")
        save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Bottone Annulla
        cancel_btn = tk.Button(button_frame, text="Annulla", 
                              command=self.cancel,
                              bg="#f44336", fg="white", font=("Arial", 12, "bold"),
                              relief="raised", bd=2, padx=20, pady=8,
                              activebackground="#da190b", activeforeground="white")
        cancel_btn.pack(side=tk.LEFT)
        
        # Info label con sfondo e bordo
        info_frame = tk.Frame(main_frame, bg="#e8f4f8", relief="solid", bd=1)
        info_frame.pack(fill=tk.X, pady=10)
        
        self.info_label = tk.Label(info_frame, text="", font=("Arial", 10, "bold"), 
                                  bg="#e8f4f8", fg="#2c3e50", pady=5)
        self.info_label.pack()
        
        # Gestione eventi
        self.root.protocol("WM_DELETE_WINDOW", self.cancel)
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())
        
        # Focus iniziale sempre sul campo username (campi vuoti)
        self.username_entry.focus()
            
        # Avvia il loop
        self.root.mainloop()
        
        return self.result
    
    def center_window(self):
        """Centra la finestra sullo schermo"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def toggle_password_visibility(self):
        """Mostra/nasconde la password"""
        if self.show_password_var.get():
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")
    
    def save_credentials(self):
        self.result = True
        self.root.destroy()
    
    def get_credentials(self):
        return self.credentials
    
    
    def test_credentials_validity(self, username, password):
        """Testa la validità delle credenziali facendo una chiamata di prova"""
        try:
            # Se non c'è un URL di test specifico, salta la validazione
            if not self.test_url:
                self.info_label.configure(text="Test saltato - nessun URL di verifica", fg="#f39c12", bg="#fff3cd")
                # Salva le credenziali anche senza test
                self.credentials.username = username
                self.credentials.password = password
                self.save_credentials()
                return True
            
            response = requests.get(
                self.test_url+"/api/auth",
                auth=HTTPBasicAuth(username, password),
                timeout=10,
                verify=False
            )
            
            if response.status_code == 200:
                self.info_label.configure(text="Credenziali valide!", fg="#27ae60", bg="#d4edda")
                # Salva le credenziali quando la validazione ha successo
                self.credentials.username = username
                self.credentials.password = password
                self.save_credentials()
                return True
            elif response.status_code == 401:
                self.info_label.configure(text="Credenziali non valide!", fg="#e74c3c", bg="#f8d7da")
                messagebox.showerror("Errore di Autenticazione", 
                                   "Username o password non corretti!")
                return False
            elif response.status_code == 403:
                self.info_label.configure(text="Accesso negato!", fg="#e74c3c", bg="#f8d7da")
                messagebox.showerror("Errore di Autorizzazione", 
                                   "Accesso negato. Verifica i permessi dell'utente.")
                return False
            else:
                self.info_label.configure(text="Errore del server!", fg="#e74c3c", bg="#f8d7da")
                messagebox.showerror("Errore del Server", 
                                   f"Errore del server: {response.status_code}\n{response.text}")
                return False
                
        except requests.exceptions.Timeout:
            self.info_label.configure(text="Timeout della connessione", fg="#e74c3c", bg="#f8d7da")
            messagebox.showerror("Errore di Connessione", 
                               "Timeout della connessione. Verifica la connessione di rete.")
            return False
        except requests.exceptions.ConnectionError:
            self.info_label.configure(text="Errore di connessione", fg="#e74c3c", bg="#f8d7da")
            messagebox.showerror("Errore di Connessione", 
                               "Impossibile connettersi al server. Verifica l'URL e la connessione di rete.")
            return False
        except Exception as e:
            self.info_label.configure(text="Errore durante il test", fg="#e74c3c", bg="#f8d7da")
            messagebox.showerror("Errore", f"Errore durante la verifica delle credenziali:\n{str(e)}")
            return False
    
    def cancel(self):
        """Annulla l'operazione"""
        self.result = False
        self.root.destroy()

def show_credentials_dialog(test_url=None):
    """Funzione helper per mostrare il dialogo delle credenziali"""
    dialog = CredentialsDialog(test_url)
    success = dialog.show_dialog()
    return success, dialog.get_credentials() if success else None

# Test standalone
if __name__ == "__main__":
    success, credentials = show_credentials_dialog()
    print(f"Successo: {success}")
    if credentials:
        print(f"Username: {credentials.username}")
        print(f"Password: {'*' * len(credentials.password)}")  # Nasconde la password per sicurezza
