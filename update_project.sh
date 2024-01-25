#!/bin/bash

# Define the project directory
PROJECT_DIR="/home/steveg/projects/cutsheet_stamp_tool"

# Navigate to the project directory
cd $PROJECT_DIR

# Pull the latest changes from the remote repository
git pull origin dig-ocean-droplet

# Set file permissions
# - Files should be rw-r--r-- (644)
# - Directories should be rwxr-xr-x (755)
# - Executable scripts (like start_app.sh) should be rwxr-xr-x (755)
find $PROJECT_DIR -type f -exec chmod 644 {} \;
find $PROJECT_DIR -type d -exec chmod 755 {} \;
chmod 755 $PROJECT_DIR/start_app.sh

# Optionally, rebuild the virtual environment and install dependencies
# Remove the existing virtual environment
rm -rf $PROJECT_DIR/venv

# Create a new virtual environment
python3 -m venv $PROJECT_DIR/venv

# Activate the virtual environment
source $PROJECT_DIR/venv/bin/activate

# Install Python dependencies
pip install -r $PROJECT_DIR/requirements.txt

# Deactivate the virtual environment
deactivate
