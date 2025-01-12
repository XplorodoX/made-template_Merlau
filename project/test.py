import unittest
import os
import pandas as pd
from pipeline import main

class TestDataPipeline(unittest.TestCase):
    def setUp(self):
        """
        Prepares the test environment before each test.
        Ensures no previous output files exist for clean testing.
        """
        self.output_files = [
            "temperature_large_graph.png",
            "co2_emissions_large_graph.png",
            "temperature_vs_emissions.png",
            "temperature_trendlines.png"
        ]
        self.csv_file = "filtered_combined_temperature_emissions.csv"
        
        for file in self.output_files:
            if os.path.exists(file):
                os.remove(file)
        
        if os.path.exists(self.csv_file):
            os.remove(self.csv_file)

    def tearDown(self):
        """
        Cleans up the test environment after each test.
        Removes generated files to keep the environment clean.
        """
        for file in self.output_files:
            if os.path.exists(file):
                os.remove(file)

        if os.path.exists(self.csv_file):
            os.remove(self.csv_file)

    def test_run_pipeline_and_check_outputs(self):
        """
        Tests whether the pipeline executes correctly:
        - Verifies that all expected output files are created
        - Checks that the CSV file contains valid data
        """
        # Run the main pipeline function
        try:
            main()
            print("Pipeline executed successfully.")
        except Exception as e:
            self.fail(f"Pipeline execution failed: {e}")

        # Verify that the output files are created
        for file in self.output_files:
            self.assertTrue(
                os.path.isfile(file),
                f"Expected output file '{file}' was not created."
            )

            # Verify that the files are not empty
            self.assertGreater(
                os.path.getsize(file),
                0,
                f"The file '{file}' is empty."
            )

        # Verify the CSV file was created
        self.assertTrue(
            os.path.isfile(self.csv_file),
            f"The file '{self.csv_file}' was not created."
        )

        # Verify that the CSV file is not empty and contains valid data
        try:
            df = pd.read_csv(self.csv_file)
        except Exception as e:
            self.fail(f"Failed to load the CSV file: {e}")

        self.assertFalse(
            df.empty,
            "The CSV file contains no rows."
        )
        self.assertGreater(
            len(df),
            0,
            "The CSV file contains no data rows."
        )

        # Validate expected columns in the CSV file
        expected_columns = ["Entity", "Code", "Month", "Year", "Temperature", "emissions_total", "Region"]
        for column in expected_columns:
            self.assertIn(
                column, df.columns,
                f"Expected column '{column}' is missing in the CSV file."
            )

        # Additional validation: Check for non-null data
        self.assertFalse(
            df.isnull().any().any(),
            "The CSV file contains missing values."
        )

if __name__ == '__main__':
    unittest.main()