import tkinter as tk
import subprocess

# Farben definieren
COLORS = {
    "start": "#6f6259",
    "end": "#aca098",
    "text": "#ffffff",
    "textfield_bg": "#534a43",
    "highlight": "#6f6259",
    "button_bg": "#444444",
    "button_fg": "#ffffff"
}

# Funktion für den Button-Click
def bewerten():
    root.quit()  # Das aktuelle Fenster schließen
    subprocess.run(["python", "Interface.py"])  # Die Tkinter-Anwendung aus "Interface.py" starten

# Funktion zum Erstellen von Widgets
def create_widget(widget_type, **kwargs):
    widget = widget_type(root, **kwargs)
    widget.pack(pady=10)
    return widget

# Hauptfenster erstellen
root = tk.Tk()
root.title("Willkommen")
root.attributes("-fullscreen", True)  # Fenster im Vollbildmodus starten
root.configure(bg=COLORS["start"])  # Hintergrundfarbe des Fensters setzen

# Begrüßungslabel hinzufügen
create_widget(tk.Label, text="Willkommen zur Anwendung!", font=("Helvetica", 14), fg=COLORS["text"], bg=COLORS["start"])

# Button "Entwurf bewerten"
bewerten_button = create_widget(tk.Button, text="Entwurf bewerten", font=("Helvetica", 12), 
                                command=bewerten, bg=COLORS["button_bg"], fg=COLORS["button_fg"], highlightbackground=COLORS["highlight"])

# Textfeld mit Beschreibung hinzufügen
beschreibung = create_widget(tk.Text, wrap=tk.WORD, height=5, width=40, bg=COLORS["textfield_bg"], fg=COLORS["text"], font=("Helvetica", 12), bd=0, padx=10, pady=10)
beschreibung.insert(tk.END, "Diese Anwendung hilft Ihnen dabei, Entwürfe zu bewerten und Feedback zu geben.\n\n"
                            "Klicken Sie auf den Button, um die Bewertung fortzusetzen.")
beschreibung.config(state=tk.DISABLED)  # Verhindert, dass der Text bearbeitet wird

# Anwendung starten
root.mainloop()
