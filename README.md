# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.tempalate` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

# Trello configuration
Trello is a web-based listmaking app popular among many dev teams because it provides
a lightweight way to track work.
Trello provides a REST API that this app uses to create, read and
update to-do items. In Trello, items or tasks are called cards and
they are grouped together as lists ('To Do', 'Done', etc.) under
boards.

You'll need to create a Trello account and a dedicated board to store the to-do items for your app. 
Setup the Trello board ID to be used in the .env file, set the TRELLO_BOARD_ID with the reference trello board to be used in the Todo app. 

Register to the website trello.com - https://trello.com/signup to create an account.

Generate an API key and token by following the https://trello.com/app-key

After creating a Trello account and generate the API key and token. Please ensure the key and token are kept safe and not shared. Set the T_KEY and T_TOKEN in the .env file with the corresponding key and token values.

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

Add new task in the Title. The tasks are added to To Do list. Use the update button to change the status of the task. The status of the Done task can also be reset to backlog using update status.


## Running the tests
## Unit tests and integrations tests
Once the all dependencies have been installed,start the tests in development mode within the poetry environment by running:
For running the integration test .env.tests file is used for basic configuration

```bash
$ poetry run pytest -s tests
```

## End to end tests using Selenium
Ensure the corresponding selenium webdriver is available in the root of the project. chromedriver.exe is used for end to end tests in this instance. 

For running the end to end tests:

```bash
$ poetry run pytest -s tests_e2e
```
## Running the app via Vagrant VM
To make vagrant automatically launch the app when you run vagrant up.Write a trigger to install your dependencies and launch the app after vagrant up, automating the steps.
In /vagrant
- Install dependecies : Poetry
- Launch flask's development server: poetry run flask run
If this step fails it may be because poetry, running inside the VM, has automatically detected the host system virtual environment (located in the .venv directory) and is trying to use it instead of creating its own! Unfortunately there's no way to exclude the host virtual environment from the directory sharing using VirtualBox. 
If you're having this issue, delete .venv and edit your poetry.toml file to set the virtuals.in-project option to false.
This tells poetry to create virtual environment files in a central location, outside your code directory. This side-steps the issue, and allows the host machine and VM to run their own independent virtual environments.

Do port forwarding i.e redirect traffic from port 5000 on the host machine to port 5000 on the VM. This will let you access the app running in vagrant via your web browser. Add the below config in Vagrant file
config.vm.network "forwarded_port", guest: 5000, host: 5000

Run the command as a background process so that it doesn't make vagrant up hang.
nohup poerty run flask run --host=0.0.0.0 > logs.txt 2>&1 &

With these changes in place, re-launch your VM and check you can access your
site by opening http://localhost:5000.

## Running the app in a Docker
Install Docker
Dockerfile contains the container configuration.

To build docker image use the below commands :
For Development :
docker build --target development --tag todo-app:dev .
For Production :
docker build --target production --tag todo-app:prod .

To run the docker container
Development:
docker run --env-file ./.env -p 5000:5000 --mount type=bind,source="$(pwd)"/todo_app,target=/app/todo_app/ todo-app:dev
Production:
docker run --env-file ./.env -p 5000:5000  todo-app:prod

List Docker continer : docker container list
To stop the container : docker stop <container name>
Remove the container : docker rm <container name>
