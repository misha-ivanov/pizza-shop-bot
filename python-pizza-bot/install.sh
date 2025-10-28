#!/usr/bin/env bash

python3 -m venv .venv
source .venv/bin/activate
pip intsall -r requirements.txt
deactivate