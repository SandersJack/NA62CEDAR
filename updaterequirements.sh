#!/bin/sh

source .venv/Scripts/activate
git checkout -b update/requirements
rm requirements.txt 
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Updated requirements.txt"
git push origin update/requirements
git branch -d update/requirements