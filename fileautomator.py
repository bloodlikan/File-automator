from pathlib import Path
import csv
import logging
import shutil
from datetime import datetime


# Carpeta donde está guardado este script
BASE_DIR = Path(__file__).parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"
REPORT_FILE = BASE_DIR / "reporte.csv"


def configurar_logs():
    """Crea el archivo de log y define el formato de los mensajes."""
    LOGS_DIR.mkdir(exist_ok=True)

    logging.basicConfig(
        filename=LOGS_DIR / "execution.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8",
    )


def clasificar_archivo(archivo):
    """Devuelve la carpeta de destino según el nombre o extensión."""
    nombre = archivo.name.lower()
    extension = archivo.suffix.lower()

    if nombre.startswith("factura"):
        return "facturas"

    if nombre.startswith("contrato"):
        return "contratos"

    if nombre.startswith("cliente"):
        return "clientes"

    if extension in {".jpg", ".jpeg", ".png", ".gif", ".webp"}:
        return "imagenes"

    return "otros"


def obtener_destino_disponible(destino):
    """Evita sobrescribir un archivo si ya existe uno con el mismo nombre."""
    if not destino.exists():
        return destino

    contador = 1
    while True:
        nuevo_destino = destino.with_name(
            f"{destino.stem}_{contador}{destino.suffix}"
        )
        if not nuevo_destino.exists():
            return nuevo_destino
        contador += 1


def procesar_archivos():
    """Clasifica y mueve los archivos de input hacia output."""
    INPUT_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)

    filas_reporte = []

    archivos = [archivo for archivo in INPUT_DIR.iterdir() if archivo.is_file()]

    if not archivos:
        print("No hay archivos para procesar dentro de la carpeta input.")
        logging.warning("No se encontraron archivos en input.")
        return

    for archivo in archivos:
        try:
            categoria = clasificar_archivo(archivo)
            carpeta_destino = OUTPUT_DIR / categoria
            carpeta_destino.mkdir(exist_ok=True)

            destino = obtener_destino_disponible(carpeta_destino / archivo.name)
            shutil.move(str(archivo), str(destino))

            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            filas_reporte.append(
                {
                    "fecha": fecha,
                    "archivo_original": archivo.name,
                    "categoria": categoria,
                    "ubicacion_final": str(destino),
                    "estado": "Procesado",
                }
            )

            logging.info(
                "Archivo procesado: %s | Categoría: %s | Destino: %s",
                archivo.name,
                categoria,
                destino,
            )

            print(f"✓ {archivo.name} → {categoria}")

        except Exception as error:
            logging.exception("Error al procesar %s", archivo.name)
            print(f"✗ Error al procesar {archivo.name}: {error}")

    generar_reporte(filas_reporte)


def generar_reporte(filas):
    """Crea el reporte CSV de la ejecución."""
    if not filas:
        return

    columnas = [
        "fecha",
        "archivo_original",
        "categoria",
        "ubicacion_final",
        "estado",
    ]

    with REPORT_FILE.open("w", newline="", encoding="utf-8-sig") as archivo_csv:
        escritor = csv.DictWriter(archivo_csv, fieldnames=columnas)
        escritor.writeheader()
        escritor.writerows(filas)

    logging.info("Reporte generado: %s", REPORT_FILE)
    print(f"\nReporte generado: {REPORT_FILE.name}")


if __name__ == "__main__":
    configurar_logs()

    print("FileAutomator iniciado...")
    procesar_archivos()
    print("Proceso finalizado.")