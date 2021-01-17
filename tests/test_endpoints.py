from dotenv import find_dotenv, load_dotenv
import requests

import pytest
import os

@pytest.fixture
def client():
    print("In client fixture")
    file_path = find_dotenv('.env.test')
    print(file_path)
    load_dotenv(file_path, override=True)
    print(os.environ.get('SECRET_KEY'))
    print(os.environ.get('FLASK_ENV'))

    from todo_app import app    
    # Create the new app
    test_app = app.create_app()

    #use the app to create test client that can be used in our tests
    with test_app.test_client() as client:
        yield client

class MockResponse:
    def __init__(self,*args, **kwargs):
        print('In MockResponse __init__')
        self.method_ = args[0]
        self.url_ = args[1]
        for kwarg in kwargs.values():
            self.params_ = kwarg
        
        print(self.method_, self.url_, self.params_)

    
    def json(self):
        if self.url_.find('cards') > 0:
            print('In json cards')
            return [
                {
                    "id": "5feb2bda1dcba5309a368592",
                    "name": "Task A",
                    "idBoard": "5feb252a40ff2d09fa3a8eea",
                    "idList": "5feb25447bb43e82547a17f1",
                    "due": None
                },
                {
                    "id": "5feb3b4554ad726db1f82e20",
                    "name": "Task D",
                    "idBoard": "5feb252a40ff2d09fa3a8eea",
                    "idList": "5feb2558a39bc5366ab8df8e",
                    "due": "2020-12-30T16:04:00.000Z"
                }
            ]

        if self.url_.find('lists') > 0:
            print('In json lists')
            return [
                        {
                            "id": "5feb25447bb43e82547a17f1",
                            "name": "To Do",
                            "idBoard": "5feb252a40ff2d09fa3a8eea"
                        },
                        {
                            "id": "5feb2553117c378500b8dd3c",
                            "name": "Doing",
                            "idBoard": "5feb252a40ff2d09fa3a8eea"
                        },
                        {
                            "id": "5feb2558a39bc5366ab8df8e",
                            "name": "Done",
                            "idBoard": "5feb252a40ff2d09fa3a8eea"
                        }
                ]
def test_index_page(monkeypatch, client):
    def mock_get_requests(*args, **kwargs):
        print('In mock_get_requests')
        return MockResponse(*args, **kwargs)

    monkeypatch.setattr(requests,"request", mock_get_requests)      
    print("In test index page")
    response = client.get('/')
    assert b'Task A' in response.data
