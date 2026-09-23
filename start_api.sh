#!/bin/bash
source venv/bin/activate
PYTHONPATH=. uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
