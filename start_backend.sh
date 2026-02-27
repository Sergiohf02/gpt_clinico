#!/bin/bash

pip install -r /home/cdsw/backend/requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8080 --app-dir /home/cdsw/backend