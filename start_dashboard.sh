#!/bin/bash
source venv/bin/activate
PYTHONPATH=. streamlit run src/dashboard/app.py --server.port 8501
