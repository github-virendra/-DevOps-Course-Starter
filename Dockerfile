FROM python:3.9.2-slim-buster as base
WORKDIR /app
COPY pyproject.toml .
RUN ["pip", "install", "poetry"]
RUN poetry install
EXPOSE 5000

FROM base as production
ENV FLASK_ENV=production
COPY . /app/
ENTRYPOINT [ "poetry", "run","gunicorn","--bind", "0.0.0.0:5000","todo_app.wsgi:app" ]

FROM base as development
ENTRYPOINT ["poetry", "run", "flask", "run","--host", "0.0.0.0"]
