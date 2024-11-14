#!/bin/bash

# Erstellen Sie das benötigte Verzeichnis
mkdir -p project/data

# Installieren Sie die erforderlichen Python-Pakete
pip install pandas requests

# Führen Sie das Python-Skript aus
python pipeline.py
