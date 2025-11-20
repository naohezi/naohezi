#!/bin/bash

# Wait for network to be ready
sleep 10

# Navigate to project directory
cd /opt/dashboard

# Activate virtual environment
source venv/bin/activate

# Start uvicorn server
venv/bin/uvicorn dev:app --reload --port 8000 --host 0.0.0.0
