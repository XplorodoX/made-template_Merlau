import unittest
import os
import pandas as pd
from main1 import main  # Importiere die main-Funktion aus deinem Skript

class TestDataPipeline(unittest.TestCase):
    def setUp(self):
        """
        Vor jedem Test wird die Testumgebung vorbereitet.
        Lösche die CSV-Datei, falls sie existiert, um saubere Tests sicherzustellen.
        """
        self.csv_file = "filtered_combined_temperature_emissions.csv"
        if os.path.exists(self.csv_file):
            os.remove(self.csv_file)

    def tearDown(self):
        """
        Nach jedem Test werden eventuelle erzeugte Dateien entfernt,
        um die Testumgebung sauber zu halten.
        """
        if os.path.exists(self.csv_file):
            os.remove(self.csv_file)

    def test_run_pipeline_and_check_csv(self):
        """
        Testet, ob das Skript die Pipeline korrekt ausführt:
        - CSV-Datei wird erstellt
        - Die Datei ist nicht leer
        - Die Datei enthält valide Daten
        """
        # Skript ausführen
        try:
            main()
        except Exception as e:
            self.fail(f"Die Ausführung der Pipeline ist fehlgeschlagen: {e}")

        # Überprüfen, ob die CSV-Datei erstellt wurde
        self.assertTrue(
            os.path.isfile(self.csv_file),
            f"Die Datei {self.csv_file} wurde nicht erzeugt."
        )

        # Überprüfen, ob die Datei nicht leer ist
        self.assertGreater(
            os.path.getsize(self.csv_file),
            0,
            f"Die Datei {self.csv_file} ist leer."
        )

        # Datei als Pandas-DataFrame laden und prüfen
        try:
            df = pd.read_csv(self.csv_file)
        except Exception as e:
            self.fail(f"Die CSV-Datei konnte nicht geladen werden: {e}")

        self.assertFalse(
            df.empty,
            "Die CSV-Datei enthält keine Zeilen."
        )
        self.assertGreater(
            len(df),
            0,
            "Die CSV-Datei enthält keine Datenzeilen."
        )

        # Zusätzliche Validierung: Prüfen, ob erwartete Spalten existieren
        expected_columns = ["column1", "column2"]  # Passe dies an deine tatsächlichen Spalten an
        for column in expected_columns:
            self.assertIn(
                column, df.columns,
                f"Erwartete Spalte '{column}' fehlt in der CSV-Datei."
            )

if __name__ == '__main__':
    unittest.main()