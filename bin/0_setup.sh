#!/bin/bash

APP_DIR='../'

# TODO(zf) Make venv off BUILDID
echo "Creating VirtualEnv"
virtualenv -p python3 venv
source ./venv/bin/activate

pip install -r "${APP_DIR}/requirements.txt"



