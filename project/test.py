import os
import unittest
from pipeline import main

class TestOutputFiles(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Run the main function to execute the data pipeline
        main()

    def test_output_files_exist(self):
        """
        Test to check if the expected output files exist after running the main script.
        """
        # Define the base directory relative to the current script's location
        base_directory = os.path.dirname(os.path.abspath(__file__))

        # Define the list of expected output files
        expected_files = [
            "temperature_large_graph.png",
            "co2_emissions_large_graph.png",
            "temperature_vs_emissions.png",
            "temperature_trendlines.png",
            "df_combined.csv",
            "yearly_summarysouth.csv",
            "yearly_summarynorden.csv",
        ]

        # Iterate over the expected files and check if they exist in the base directory
        for file in expected_files:
            file_path = os.path.join(base_directory, file)
            self.assertTrue(os.path.exists(file_path), f"File {file_path} does not exist.")

if __name__ == "__main__":
    unittest.main()
