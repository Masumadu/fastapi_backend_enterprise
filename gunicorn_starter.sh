#!/bin/sh

alembic upgrade head

gunicorn --worker-class uvicorn.workers.UvicornWorker --workers 4  --bind 0.0.0.0:5000 --error-logfile - --access-logfile -  app.asgi:app
