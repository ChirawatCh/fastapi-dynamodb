#!/bin/bash

# Run your Python import script
python data/import_csv.py

# Start the FastAPI application using uvicorn
uvicorn src.main:app --host 0.0.0.0 --port 80 --reload
