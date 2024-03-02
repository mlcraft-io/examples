#!/bin/bash

function create_venv {
  if [ ! -d ".venv" ]; then
    python3.9 -m venv .benchmarks_venv
  fi
  source .benchmarks_venv/bin/activate
  echo "Virtual environment activated!"
}

create_venv

python -m pip install --upgrade pip
pip install -r requirements.txt