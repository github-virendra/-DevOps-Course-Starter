import os


class Config:
    def __init__(self):
        """Base configuration variables."""
        self.M_KEY = os.environ.get('M_KEY')
        
        self.M_TOKEN = os.environ.get('M_TOKEN')
        
        self.MONGO_BOARD_ID=os.environ.get('MONGO_BOARD_ID')