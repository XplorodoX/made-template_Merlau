#!/bin/bash

# Skriptname: run_main.sh

# Überprüfen, ob Python installiert ist
if ! command -v python3 &> /dev/null; then
    echo "Python ist nicht installiert. Bitte installiere Python, um dieses Skript auszuführen."
    exit 1
fi

# Überprüfen, ob main.py existiert
if [ ! -f "main.py" ]; then
    echo "Die Datei main.py wurde nicht gefunden. Stelle sicher, dass sie im aktuellen Verzeichnis liegt."
    exit 1
fi

# Ausführen von main.py
echo "Starte main.py..."
python3 main.py

# Erfolgsmeldung
if [ $? -eq 0 ]; then
    echo "main.py wurde erfolgreich ausgeführt."
else
    echo "Fehler beim Ausführen von main.py."
    exit 1
fi
