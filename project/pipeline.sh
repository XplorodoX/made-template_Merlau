#!/bin/bash

# Create the required directory
mkdir -p project/data

# Install the necessary Python packages
pip install pandas requests

# Run the Python script
python pipeline.py
