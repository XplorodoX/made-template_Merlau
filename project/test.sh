#!/usr/bin/env bash
# test.sh
#
# Bash-Skript, das dein Python-Testskript ausführt.

set -e  # Script sofort beenden, wenn ein Befehl einen Fehler zurückgibt

echo "Starte Tests..."

# Optional: Prüfen, ob Python installiert ist
if ! command -v python3 &>/dev/null; then
  echo "Fehler: python3 ist nicht installiert!"
  exit 1
fi

# Dein Python-Testskript ausführen
python3 ./project/test.py

echo "Alle Tests erfolgreich abgeschlossen!"