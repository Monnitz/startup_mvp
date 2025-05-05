import tkinter as tk
from tkinter import filedialog
import random

# Farbkonvertierungen
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % rgb

# Verlauf zeichnen
def draw_gradient(canvas, color1, color2):
    canvas.delete("gradient")
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    steps = height

    r1, g1, b1 = hex_to_rgb(color1)
    r2, g2, b2 = hex_to_rgb(color2)

    for i in range(steps):
        ratio = i / steps
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        color = rgb_to_hex((r, g, b))
        canvas.create_line(0, i, width, i, fill=color, tags="gradient")

# Kriterienliste (binär bewertete zuerst)
KRITERIEN = [
    # Binär bewertete Kriterien zuerst
    ("1. Risikoprüfung", "Erkennbare Risiken wie Brandschutzprobleme (Ja/Nein).", False),
    ("2. Baurechtliche Konformität", "Entspricht das Projekt den Vorschriften? (Ja/Nein).", False),
    ("3. Barrierefreiheit & soziale Aspekte", "Erfüllt die Barrierefreiheit die Mindestanforderungen? (Erfüllt/Nicht erfüllt).", False),
    
    # Qualitative Kriterien danach
    ("4. Gestalterische Qualität", "Ästhetik und Proportionen sind subjektiv und graduell beurteilbar.", True),
    ("5. Funktionalität und Nutzbarkeit", "Raumorganisation, Tageslicht, Flexibilität lassen sich gut abgestuft bewerten.", True),
    ("6. Tragwerks- und Technikkonzept", "Integration von Technik und Tragwerk kann unterschiedlich durchdacht sein.", True),
    ("7. Nachhaltigkeit und Energieeffizienz", "Kompromisse zwischen guter Dämmung und PV-Anlage können existieren.", True),
    ("8. Kosten- und Flächeneffizienz", "Effizienz lässt sich zwischen teuer aber sinnvoll und unwirtschaftlich differenzieren.", True),
    ("9. Städtebauliche Einbindung", "Gute Kontextanpassung versus sehr gute Kontextanpassung.", True),
    ("10. Darstellung und Kommunikation", "Qualität der Pläne und Visualisierungen lässt sich abgestuft bewerten.", True),
]

# Zufallsbewertung
def get_random_punkte(is_qualitative):
    return random.randint(1, 5) if is_qualitative else random.choice([1, 5])

# Upload-Dialog
def upload_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        text_field.delete("1.0", tk.END)
        for titel, beschreibung, is_qualitative in KRITERIEN:
            punkt = get_random_punkte(is_qualitative)
            punkte_str = " ".join([f"[{i}]" if i == punkt else f"{i}" for i in range(1, 6)]) if is_qualitative else ("Ja" if punkt == 5 else "Nein")
            
            text_field.insert(tk.END, f"{titel.upper()}\n", "bold")
            text_field.insert(tk.END, f"    {beschreibung}\n", "normal")
            text_field.insert(tk.END, f"    Bewertung: {punkte_str}\n\n", "bewertung")

# UI-Elemente erstellen
def create_button(parent, text, command, **kwargs):
    return tk.Button(parent, text=text, command=command, font=("Arial", 14), bg=BUTTON_BG, fg=BUTTON_FG, activebackground="#666666", activeforeground="#ffffff", relief="flat", **kwargs)

# Farben
START_COLOR = "#6f6259"
END_COLOR = "#aca098"
TEXT_COLOR = "#ffffff"  
TEXTFIELD_BG_COLOR = "#534a43"  
BUTTON_BG = "#444444"
BUTTON_FG = "#ffffff"

# Hauptfenster
root = tk.Tk()
root.title("Gebäudebewertung")
root.attributes("-fullscreen", True)

# Canvas als Hintergrund
canvas = tk.Canvas(root, highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True)

# Gradient bei Resize neu zeichnen
def on_resize(event):
    draw_gradient(canvas, START_COLOR, END_COLOR)

canvas.bind("<Configure>", on_resize)

# Frame für Inhalte
frame = tk.Frame(canvas, bg="", highlightthickness=0)
frame.place(relwidth=1, relheight=1)

# Close-Button
close_button = tk.Button(
    frame, text="X", font=("Arial", 14, "bold"), command=root.quit,
    bg="#ff3b30", fg="#ffffff", width=3, height=1, relief="flat"
)
close_button.place(relx=1, x=-10, y=10, anchor="ne")

# Upload-Button
upload_button = tk.Button(
    frame, text="Datei zum Bewerten auswählen", font=("Arial", 14),
    command=upload_file,
    bg=BUTTON_BG, fg=BUTTON_FG, activebackground="#666666", activeforeground="#ffffff"
)
upload_button.pack(pady=20)

# Textfeld - Hintergrundfarbe auf #534a43 gesetzt
text_field = tk.Text(
    frame, wrap=tk.WORD, font=("Arial", 12),
    bg=TEXTFIELD_BG_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR, state=tk.NORMAL
)
text_field.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

# Textformatierungen
text_field.tag_configure("bold", font=("Arial", 12, "bold"), foreground="#aca098")
text_field.tag_configure("bewertung", foreground=TEXT_COLOR)
text_field.tag_configure("normal", foreground=TEXT_COLOR)

# Zu Beginn ein Dialogfeld mit einer Nachricht anzeigen
text_field.insert(tk.END, "Willkommen zur Gebäudebewertung! Bitte wählen Sie eine Datei aus, um zu starten.", "normal")

# Verhindern von Benutzereingaben
def prevent_edit(event):
    return "break"

# Hilfe-Button
def show_help():
    help_text = """Willkommen zur Gebäudebewertung!

1. Klicken Sie auf den 'Datei zum Bewerten auswählen'-Button, um eine Datei auszuwählen.
2. Eine zufällige Bewertung wird für die 10 Kriterien angezeigt.
3. Am Ende wird eine Gesamtbewertung angezeigt.

Viel Spaß bei der Bewertung!"""
    text_field.config(state=tk.NORMAL)
    text_field.delete("1.0", tk.END)
    text_field.insert(tk.END, help_text)
    text_field.config(state=tk.DISABLED)

help_button = create_button(frame, "Hilfe", show_help)
help_button.place(relx=0.05, rely=0.05, anchor="nw")

# Tasteneingaben blockieren
text_field.bind("<Key>", prevent_edit)
text_field.bind("<Button>", prevent_edit)

# ESC beendet Vollbild
root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))

# Starte Fenster
root.mainloop()
