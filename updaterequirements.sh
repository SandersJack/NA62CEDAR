#!/bin/sh

source .venv/Scripts/activate
rm requirements.txt 
pip freeze > requirements.txt