#!/bin/bash
FOLDER="env"

echo "CREATE ENVIRONMENT"
virtualenv $FOLDER

echo "INSTALL DEPENDENCIES"
env/bin/pip install -r requirements.txt

echo "CREATE ENVIRONMENT"

echo "LOGS -> k8s-install.log"
env/bin/python3 k8s_install.py

rm -r env