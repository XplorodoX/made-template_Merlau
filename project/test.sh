#!/usr/bin/env bash
# test.sh

set -e 

echo "Starte Tests..."

if ! command -v python3 &>/dev/null; then
  echo "Fehler: python3 ist nicht installiert!"
  exit 1
fi

python3 ./project/test.py

echo "Alle Tests erfolgreich abgeschlossen!"