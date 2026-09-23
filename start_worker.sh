#!/bin/bash
source venv/bin/activate
PYTHONPATH=. arq src.worker.settings.WorkerSettings
