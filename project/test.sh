#!/usr/bin/env bash
# tests.sh

# Bei Fehler (z.B. Befehl schlägt fehl) wird das Skript abgebrochen
set -e  

echo "Starte Testläufe..."

# Kleiner Beispiel-Test: Prüfen, ob Python installiert ist
if command -v python &> /dev/null; then
  echo "Python ist installiert. Führe hier deine echten Tests aus..."
  # Beispiel: pytest aufrufen (auskommentiert, bis du echte Tests hast)
  # pytest
else
  echo "Python ist nicht installiert. Tests werden übersprungen."
  # Oder ggf. Fehler provozieren: exit 1
fi

echo "Alle Tests (Beispiel) erfolgreich durchgelaufen!"