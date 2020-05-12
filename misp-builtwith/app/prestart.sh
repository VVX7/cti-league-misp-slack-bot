#! /usr/bin/env bash

# Nothing to do here.
# This file starts the Redis work and the gunicorn http server.
echo "Running inside /app/prestart.sh, you could add migrations to this file, e.g.:"
echo "Starting worker..."
python -u /app/worker.py &
gunicorn --bind 0.0.0.0:5000 wsgi:app