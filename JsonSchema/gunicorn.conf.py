# gunicorn.conf.py
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'JsonSchema.settings')
bind = '0.0.0.0:8000'
workers = 1
worker_class = 'uvicorn.workers.UvicornWorker'
loglevel = 'info'
