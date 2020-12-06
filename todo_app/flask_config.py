import os


class Config:
    """Base configuration variables."""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for Flask application. Did you follow the setup instructions?")

    T_KEY = os.environ.get('T_KEY')
    if not T_KEY:
        raise ValueError("No Trello T_KEY set for Flask application. Did you follow the setup instructions?")

    T_TOKEN = os.environ.get('T_TOKEN')
    if not T_TOKEN:
        raise ValueError("No Trello T_TOKEN set for Flask application. Did you follow the setup instructions?")
