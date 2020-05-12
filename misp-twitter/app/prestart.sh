#! /usr/bin/env bash

echo "Running inside /app/prestart.sh, you could add migrations to this file, e.g.:"
echo "Starting worker..."
python /app/worker.py &
gunicorn --bind 0.0.0.0:5000 wsgi:app