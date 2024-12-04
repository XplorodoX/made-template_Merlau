#!/bin/bash
set -e

# Run all tests
echo "Running system-level tests..."

# Execute the data pipeline
echo "Executing data pipeline..."
./pipeline.sh

cd "$(dirname "$0")"

# Validate output files
echo "Validating output..."
if [ -f ../data/cleaned_data.db ]; then
    echo "Test passed: Output file exists."
else
    echo "Test failed: Output file does not exist."
    exit 1
fi

echo "All tests passed!"