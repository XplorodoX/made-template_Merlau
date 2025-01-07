#!/usr/bin/env python3

import os
import subprocess

def run_pipeline_test():
    """
    Führt die Datenpipeline aus und überprüft, ob die erwartete Ausgabedatei existiert und nicht leer ist.
    Dabei lädt die Pipeline die Eingangsdaten von selbst herunter (kein lokales input_file notwendig).
    """
    print("Starte Systemtest für die Datenpipeline...")

    # Name der Ausgabedatei
    output_file = "filtered_combined_temperature_emissions.csv"

    # 1) Entferne ggf. alte Ausgabedateien
    if os.path.exists(output_file):
        print(f"Entferne vorhandenes Ausgabefile: {output_file}")
        os.remove(output_file)

    # 2) Pipeline starten (die Pipeline lädt die Daten selbst herunter)
    print("Führe Datenpipeline aus...")
    subprocess.run(["python3", "pipeline.py"], check=True)

    # 3) Überprüfe, ob das Ausgabefile vorhanden ist
    if not os.path.exists(output_file):
        raise FileNotFoundError(f"Fehler: {output_file} wurde nicht erstellt.")

    # 4) Größe überprüfen (ob die Datei nicht leer ist)
    file_size = os.path.getsize(output_file)
    if file_size == 0:
        raise ValueError(f"Fehler: {output_file} ist leer.")

    print(f"✓ {output_file} wurde erfolgreich erstellt und ist nicht leer.")
    print("Systemtest erfolgreich abgeschlossen!")

if __name__ == "__main__":
    run_pipeline_test()