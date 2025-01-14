import os
import unittest
import pandas as pd
from pipeline import main

class TestOutputFiles(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Run the main function to execute the data pipeline.
        """
        main()

    def setUp(self):
        """
        Define the base directory relative to the current script's location
        for use in all tests.
        """
        self.base_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

    def test_output_files_exist(self):
        """
        Test to check if the expected output files exist after running the main script.
        """
        # List of expected output files
        expected_files = [
            "temperature_large_graph.pdf",
            "co2_emissions_large_graph.pdf",
            "temperature_vs_emissions.pdf",
            "temperature_trendlines.pdf",
            "df_combined.csv",
            "yearly_summarysouth.csv",
            "yearly_summarynorden.csv",
        ]

        # Verify existence of each file in the data directory
        for file in expected_files:
            file_path = os.path.join(self.base_directory, file)
            with self.subTest(file=file):
                self.assertTrue(os.path.exists(file_path), f"File {file_path} does not exist.")

    def test_csv_file_content(self):
        """
        Test to ensure that the CSV files contain data and are not empty.
        """
        # List of expected CSV output files
        csv_files = [
            "df_combined.csv",
            "yearly_summarysouth.csv",
            "yearly_summarynorden.csv",
        ]

        # Verify that each CSV file is not empty
        for file in csv_files:
            file_path = os.path.join(self.base_directory, file)
            with self.subTest(file=file):
                self.assertTrue(os.path.exists(file_path), f"CSV file {file_path} does not exist.")
                df = pd.read_csv(file_path)
                self.assertFalse(df.empty, f"CSV file {file_path} is empty.")
                self.assertGreater(len(df), 0, f"CSV file {file_path} has no data rows.")

if __name__ == "__main__":
    unittest.main()
