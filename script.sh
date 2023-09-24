#!/bin/bash

# Define the target directory and log file path
TARGET_DIR="/mnt/c/Users/jayku/PersonalProject/node-app/pythoncode/target"
LOG_FILE="/mnt/c/Users/jayku/PersonalProject/node-app/pythoncode/logfile.log"

touch $LOG_FILE

# Change to the target directory
cd "$TARGET_DIR" || exit 1

# Run Git commands
git add .
git commit -m "Automated commit on $(date)"
COMMIT_HASH=$(git rev-parse HEAD)

# Log the operation in the specified log file, including the commit hash
echo "Git commit performed on $(date) with commit hash: $COMMIT_HASH" >> "$LOG_FILE"