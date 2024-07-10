#!/bin/bash

# Ensure npm global bin is in PATH
export PATH=$PATH:/usr/local/bin

# Start the Flask API
nohup python /app/flask-api/src/app/app.py &

# Start the Gatsby frontend
nohup gatsby serve -H 0.0.0.0 -p 8000 &

# Wait for processes to keep the container running
wait
