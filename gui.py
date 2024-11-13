import tkinter as tk
from tkinter import PhotoImage
import subprocess

def run_main():
    subprocess.run(["python", "main.py"])

def create_gui():
    window = tk.Tk()
    window.title("SiTra QR Code Generator")
    window.geometry("400x200")

    try:
        image = PhotoImage(file="usblogogui.png")

        label = tk.Label(window, image=image, width=198, height=41)
        label.pack(pady=10)
    except tk.TclError as e:
        print("Fehler beim Laden des Bildes:", e)

    button = tk.Button(window, text="Generiere QR Codes für SiTra Test", command=run_main)
    button.pack(pady=10)

    window.mainloop()

if __name__ == "__main__":
    create_gui()
