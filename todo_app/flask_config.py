import os


class Config:
    def __init__(self):
        """Base configuration variables."""
        #self.SECRET_KEY = os.environ.get('SECRET_KEY')

        self.T_KEY = os.environ.get('T_KEY')
        
        self.T_TOKEN = os.environ.get('T_TOKEN')
        
        self.TRELLO_BOARD_ID=os.environ.get('TRELLO_BOARD_ID')
        
    