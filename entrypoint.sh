#!/usr/bin/env bash
poetry run gunicorn --bind 0.0.0.0:$PORT todo_app.wsgi:app
