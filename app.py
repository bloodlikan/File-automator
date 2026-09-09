import os
import subprocess
import sys
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, scrolledtext


BASE_DIR = Path(__file__).parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
SCRIPT_PATH = BASE_DIR / "fileautomator.py"


def ejecutar_automatizador():
    archivos = [archivo for archivo in INPUT_DIR.iterdir() if archivo.is_file()]

    if not archivos:
        messagebox.showwarning(
            "Sin archivos",
            "La carpeta input está vacía.\n\nAgregá archivos y volvé a intentarlo."
        )
        return

    boton_procesar.config(state="disabled")
    texto_resultado.delete("1.0", tk.END)
    texto_resultado.insert(tk.END, "Procesando archivos...\n\n")
    ventana.update()

    resultado = subprocess.run(
        [sys.executable, str(SCRIPT_PATH)],
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    texto_resultado.insert(tk.END, resultado.stdout)

    if resultado.returncode == 0:
        messagebox.showinfo(
            "Proceso terminado",
            "Los archivos fueron organizados correctamente.\n\n"
            "Revisá la carpeta output y el archivo reporte.csv."
        )
    else:
        texto_resultado.insert(tk.END, "\nERROR:\n" + resultado.stderr)
        messagebox.showerror(
            "Ocurrió un error",
            "No se pudieron procesar los archivos. Revisá el detalle en pantalla."
        )

    boton_procesar.config(state="normal")


def abrir_carpeta_input():
    os.startfile(INPUT_DIR)


def abrir_carpeta_output():
    os.startfile(OUTPUT_DIR)


ventana = tk.Tk()
ventana.title("FileAutomator")
ventana.geometry("620x470")
ventana.resizable(False, False)
ventana.configure(bg="#f4f6f8")

titulo = tk.Label(
    ventana,
    text="FileAutomator",
    font=("Arial", 24, "bold"),
    bg="#f4f6f8",
    fg="#1f2937",
)
titulo.pack(pady=(25, 5))

subtitulo = tk.Label(
    ventana,
    text="Organizá tus archivos automáticamente",
    font=("Arial", 12),
    bg="#f4f6f8",
    fg="#4b5563",
)
subtitulo.pack(pady=(0, 20))

boton_abrir_input = tk.Button(
    ventana,
    text="1. Abrir carpeta input",
    font=("Arial", 11),
    width=28,
    command=abrir_carpeta_input,
)
boton_abrir_input.pack(pady=5)

boton_procesar = tk.Button(
    ventana,
    text="2. Organizar archivos",
    font=("Arial", 12, "bold"),
    width=28,
    bg="#2563eb",
    fg="white",
    activebackground="#1d4ed8",
    activeforeground="white",
    command=ejecutar_automatizador,
)
boton_procesar.pack(pady=10)

boton_abrir_output = tk.Button(
    ventana,
    text="3. Ver archivos organizados",
    font=("Arial", 11),
    width=28,
    command=abrir_carpeta_output,
)
boton_abrir_output.pack(pady=5)

etiqueta_resultado = tk.Label(
    ventana,
    text="Resultado de la ejecución",
    font=("Arial", 11, "bold"),
    bg="#f4f6f8",
    fg="#1f2937",
)
etiqueta_resultado.pack(pady=(20, 5))

texto_resultado = scrolledtext.ScrolledText(
    ventana,
    width=70,
    height=11,
    font=("Consolas", 9),
)
texto_resultado.pack(padx=20, pady=(0, 15))

ventana.mainloop()