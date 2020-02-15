#!/bin/bash

set -ex

if [ -z $(pip3 freeze | grep virtualenv) ]; then
    pip3 install virtualenv
fi

if [ ! -d "venv" ]; then
  virtualenv -p python3 venv
fi

source venv/bin/activate

pip3 install -r requirements.txt

python3 main.py
