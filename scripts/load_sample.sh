#!/bin/bash
set -e

echo "Generating sample data for the Global Job Project"

# Check if Python environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Error: Python virtual environment not activated."
    echo "Please activate the virtual environment first with: source venv/bin/activate"
    exit 1
fi

# Run the Python script
python -m scripts.generate_sample_data

echo "Sample data generation complete!"
