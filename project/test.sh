#!/usr/bin/env bash
# tests.sh

# Brich ab, wenn ein Befehl fehlschlägt
set -e

echo "Starte Systemtest für die Datenpipeline..."

# 1) Alte Ausgabedateien entfernen (falls vorhanden)
OUTPUT_FILE="filtered_combined_temperature_emissions.csv"
if [ -f "$OUTPUT_FILE" ]; then
    echo "Entferne vorhandenes Ausgabefile: $OUTPUT_FILE"
    rm "$OUTPUT_FILE"
fi

# 2) Datenpipeline ausführen
echo "Führe Datenpipeline aus..."
python3 pipeline.py input_data.csv "$OUTPUT_FILE"

# 3) Prüfe, ob das Ausgabefile erzeugt wurde
if [ -f "$OUTPUT_FILE" ]; then
    echo "✓ Ausgabedatei $OUTPUT_FILE wurde erzeugt."
else
    echo "✗ Fehler: Ausgabedatei $OUTPUT_FILE fehlt!"
    exit 1
fi

# 4) Optional: Weitere Validierung
FILE_SIZE=$(wc -c <"$OUTPUT_FILE")
if [ "$FILE_SIZE" -gt 0 ]; then
    echo "✓ $OUTPUT_FILE ist nicht leer ($FILE_SIZE Bytes)."
else
    echo "✗ Fehler: $OUTPUT_FILE ist leer."
    exit 1
fi

echo "Systemtest erfolgreich abgeschlossen!"