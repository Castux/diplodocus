#!/bin/bash

sudo apt update
sudo apt install python3-venv python3-pip
python3 -m pip install -U discord.py

git submodule init
git submodule update

cd diplomacy
pip install -r requirements.txt
