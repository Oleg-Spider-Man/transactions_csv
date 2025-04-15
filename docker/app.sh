#!/bin/sh


gunicorn src.api.api_main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
