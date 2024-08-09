#!/bin/bash

# Command to run (replace this with your command)
command_to_run="python _main.py"

# Timeout between runs (in seconds)
timeout=20

# While loop to continue running the command until the exit code is 0
while true; do
    # Run the command
    $command_to_run
    
    # Check the exit code
    exit_code=$?
    
    # If the exit code is 0, break out of the loop
    if [ $exit_code -eq 0 ]; then
        break
    fi
    
    # Add any necessary delay before running the command again (optional)
    sleep $timeout
done