#!/bin/bash

function create_venv {
  if [ ! -d ".venv" ]; then
    python3.9 -m venv .venv
  fi
  source .venv/bin/activate
  echo "Virtual environment activated!"
}

create_venv

python -m pip install --upgrade pip
pip install -r requirements.txt