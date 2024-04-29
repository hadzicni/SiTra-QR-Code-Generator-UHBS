import tkinter as tk
from tkinter import PhotoImage
import subprocess

def run_main():
    # Führt die main.py als separaten Prozess aus
    subprocess.run(["python", "main.py"])

def create_gui():
    window = tk.Tk()
    window.title("SiTra QR Code Generator")
    window.geometry("400x200")

    try:
        # Laden des Bildes
        image = PhotoImage(file="usblogogui.png")

        # Anzeige des Bildes in einem Label mit den angegebenen Abmessungen
        label = tk.Label(window, image=image, width=198, height=41)
        label.pack(pady=10)
    except tk.TclError as e:
        print("Fehler beim Laden des Bildes:", e)

    # Button, der main.py ausführt
    button = tk.Button(window, text="Generiere QR Codes für SiTra Test", command=run_main)
    button.pack(pady=10)

    window.mainloop()

if __name__ == "__main__":
    create_gui()
