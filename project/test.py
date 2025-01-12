import unittest
import os
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
        
        for file in self.output_files:
            if os.path.exists(file):
                os.remove(file)

    def tearDown(self):
        """
        Cleans up the test environment after each test.
        Removes generated files to keep the environment clean.
        """
        for file in self.output_files:
            if os.path.exists(file):
                os.remove(file)

    def test_run_pipeline_and_check_outputs(self):
        """
        Tests whether the pipeline executes correctly:
        - Verifies that all expected output files are created
        - Checks that the files are not empty
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

if __name__ == '__main__':
    unittest.main()