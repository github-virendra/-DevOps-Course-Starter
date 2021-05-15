FROM python:3.9.2-slim-buster as base
WORKDIR /app
COPY pyproject.toml .
COPY poetry.lock .
RUN ["pip", "install", "poetry"]
#RUN poetry install
EXPOSE 5000

FROM base as production
ENV FLASK_ENV=production
COPY ./todo_app/ /app/todo_app
RUN poetry install --no-dev
ENTRYPOINT [ "poetry", "run","gunicorn","--bind", "0.0.0.0:5000","todo_app.wsgi:app" ]

FROM base as development
RUN poetry install
ENTRYPOINT ["poetry", "run", "flask", "run","--host", "0.0.0.0"]
