import unittest
import os
import pandas as pd
from pipeline import main  # Aus pipeline.py importieren

class TestDataPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Führt einmalig vor allen Tests die Pipeline aus.
        Wir nehmen an, dass pipeline.main() das CSV 'merged_dataset.csv' generiert.
        """
        # Falls schon eine alte CSV-Datei existiert, löschen wir sie.
        csv_file = "merged_dataset.csv"
        if os.path.isfile(csv_file):
            os.remove(csv_file)

        # Jetzt die Pipeline starten
        main()

    def test_csv_file_exists(self):
        """
        Prüft, ob die Pipeline ein 'merged_dataset.csv' erzeugt hat.
        """
        self.assertTrue(os.path.isfile('merged_dataset.csv'),
                        "CSV-Ausgabedatei 'merged_dataset.csv' wurde nicht erzeugt.")

    def test_csv_file_not_empty(self):
        """
        Prüft, ob die erzeugte CSV-Datei nicht leer ist.
        """
        file_size = os.path.getsize('merged_dataset.csv')
        self.assertGreater(file_size, 0, "Die CSV-Datei ist leer.")

    def test_csv_has_data(self):
        """
        Lädt die CSV in ein DataFrame und prüft, ob es mindestens eine Zeile gibt.
        """
        df = pd.read_csv('merged_dataset.csv')
        self.assertFalse(df.empty, "CSV-Datei enthält keine Zeilen.")
        self.assertGreater(len(df), 0, "CSV-Datei hat keine Datenzeilen.")

if __name__ == '__main__':
    unittest.main()