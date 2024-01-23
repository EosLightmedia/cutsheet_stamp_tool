#!/bin/bash

# Activate the virtual environment
source /home/steveg/projects/cutsheet_stamp_tool/venv/bin/activate

# Change to your project directory
cd /home/steveg/projects/cutsheet_stamp_tool

# Start Gunicorn with your Flask app
/home/steveg/projects/cutsheet_stamp_tool/venv/bin/gunicorn --workers 3 --timeout 240 --bind unix:cutsheet_stamp_tool.sock app:app
