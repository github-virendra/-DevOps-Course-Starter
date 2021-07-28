FROM python:3.9.2-slim-buster as base
WORKDIR /app
COPY pyproject.toml .
COPY poetry.lock .
COPY entrypoint.sh .
RUN ["pip", "install", "poetry"]
#RUN poetry install
EXPOSE 5000

FROM base as production
ENV FLASK_ENV=production
COPY ./todo_app/ /app/todo_app
RUN poetry config virtualenvs.create false --local && poetry install --no-dev
#ENTRYPOINT [ "poetry", "run","gunicorn","--bind", "0.0.0.0:$PORT","todo_app.wsgi:app" ]
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT /app/entrypoint.sh

FROM base as development
RUN poetry install
ENTRYPOINT ["poetry", "run", "flask", "run","--host", "0.0.0.0"]

FROM base as test
RUN apt-get update && apt-get install curl -y
RUN apt-get update && apt-get install wget -y

#Install chrome
RUN ls -lrt /etc/apt
RUN apt-get update && apt-get install -y gnupg2
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
RUN apt-get update && apt-get install google-chrome-stable -y

RUN poetry install
ENV PYTHONPATH /app:$PATH
ENTRYPOINT ["poetry", "run", "pytest"]

