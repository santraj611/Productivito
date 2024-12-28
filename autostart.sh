#!/bin/bash

# Setting file path
Path="/codes/pythonforbg/Productivito"

# Going to the file path
cd $HOME/$Path

# Activating the env
echo "Activating The environment"
source bin/activate
echo "environment activated"

# Running the server in background
echo "Starting the main app"
python3 main.py &
