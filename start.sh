#!/bin/bash

# Ensure npm global bin is in PATH
export PATH=$PATH:/usr/local/bin

# Print the current working directory to verify
pwd

# Start the Flask API
nohup python /app/flask-api/src/app/app.py &

# Change working directory to the Gatsby project
cd /app/front-end

# Print the current working directory to verify
pwd

# Start the Gatsby frontend
nohup gatsby serve -H 0.0.0.0 -p 8000 &

# Change working directory back to /app
cd /app

# Print the current working directory to verify
pwd

# Wait for processes to keep the container running
wait
