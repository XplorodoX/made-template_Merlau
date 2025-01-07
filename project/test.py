import unittest
import os
import subprocess
import pandas as pd

class TestDataPipeline(unittest.TestCase):
    def setUp(self):
        """
        Vor jedem Test einmal altes CSV löschen (falls vorhanden)
        """
        self.csv_file = "merged_dataset.csv"
        if os.path.exists(self.csv_file):
            os.remove(self.csv_file)

    def test_run_pipeline_and_check_csv(self):
        """
        Ruft main.py per subprocess auf, prüft, ob 'merged_dataset.csv' erzeugt wurde
        und ob sie nicht leer ist.
        """
        # 1) main.py ausführen (hier wird dein Skript ganz normal gestartet)
        subprocess.run(["python", "main.py"], check=True)

        # 2) Check: CSV erzeugt?
        self.assertTrue(
            os.path.isfile(self.csv_file),
            f"Die Datei {self.csv_file} wurde nicht erzeugt."
        )

        # 3) Check: Datei nicht leer?
        self.assertGreater(
            os.path.getsize(self.csv_file),
            0,
            f"Die Datei {self.csv_file} ist leer."
        )

        # 4) Optional: Laden als Pandas-DataFrame, um weitere Prüfungen zu machen
        df = pd.read_csv(self.csv_file)
        self.assertFalse(df.empty, "CSV-Datei enthält keine Zeilen.")
        self.assertGreater(len(df), 0, "CSV-Datei hat keine Datenzeilen.")

if __name__ == '__main__':
    unittest.main()