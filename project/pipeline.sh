#!/bin/bash

# Navigate to the directory containing the Bash script
cd "$(dirname "$0")"

# Install the necessary Python packages
pip install pandas requests

# Run the Python script
python pipeline.py
