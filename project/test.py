import unittest
import os
import pandas as pd
from pipeline import main 

class TestDataPipeline(unittest.TestCase):
    def setUp(self):
        """
        Prepares the test environment before each test.
        Deletes the CSV file if it exists to ensure clean tests.
        """
        self.csv_file = "filtered_combined_temperature_emissions.csv"
        if os.path.exists(self.csv_file):
            os.remove(self.csv_file)

    def tearDown(self):
        """
        Cleans up the test environment after each test.
        Removes any generated files to keep the environment clean.
        """
        if os.path.exists(self.csv_file):
            os.remove(self.csv_file)

    def test_run_pipeline_and_check_csv(self):
        """
        Tests whether the script executes the pipeline correctly:
        - Verifies that the CSV file is created
        - Checks that the file is not empty
        - Validates the file contains proper data
        """
        # Print the current working directory
        print(f"Current working directory: {os.getcwd()}")

        # Run the script
        try:
            main()
            print("The main() function executed successfully.")
        except Exception as e:
            self.fail(f"Pipeline execution failed: {e}")

        # Print the directory contents after running the script
        print(f"Directory contents after running main(): {os.listdir(os.getcwd())}")

        # Verify that the CSV file was created
        self.assertTrue(
            os.path.isfile(self.csv_file),
            f"The file {self.csv_file} was not created."
        )

        # Verify that the file is not empty
        self.assertGreater(
            os.path.getsize(self.csv_file),
            0,
            f"The file {self.csv_file} is empty."
        )

        # Load the file as a Pandas DataFrame and validate its contents
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

        # Additional validation: Check if expected columns exist
        expected_columns = ["Entity", "Code", "Month", "Year", "Temperature", "emissions_total"] 
        for column in expected_columns:
            self.assertIn(
                column, df.columns,
                f"Expected column '{column}' is missing in the CSV file."
            )

if __name__ == '__main__':
    unittest.main()