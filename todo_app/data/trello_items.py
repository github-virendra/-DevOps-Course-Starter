from flask import current_app as app
import requests
from datetime import datetime 
import os


class Board:
    def __init__(self, name):

        url = "https://api.trello.com/1/boards/"

        query = {
                    'key' : app.config.get("T_KEY"),
                    'token': app.config.get("T_TOKEN"),
                    'name': name
            }

        response = requests.request("POST", url, params=query).json()
        self.board_id_ = response['id']
        os.environ['TRELLO_BOARD_ID'] = self.board_id_
    
    @property
    def board_id(self):
        return self.board_id_



    def delete_board(self):
        url = "https://api.trello.com/1/boards/" + self.board_id

        print(url)
        query = {
                    'key' : app.config.get("T_KEY"),
                    'token': app.config.get("T_TOKEN"),
             }
        print('\nDeleting Board :' , self.board_id)
        response = requests.request("DELETE", url, params=query).json()
        if response['_value'] == None:
            print("Board Deleted")
            return True 


class StatusList:
    def __init__(self):

        board_id = os.environ.get('TRELLO_BOARD_ID')
        url = "https://api.trello.com/1/boards/" + board_id + "/lists"

        query = {
                    'key' : app.config.get("T_KEY"),
                    'token': app.config.get("T_TOKEN"),
                    'fields' : 'id,name,idBoard'
             }

        response = requests.request("GET", url, params=query).json()
        self.statuses_ = response

    
    def get_status_id(self, name):
        for status in self.statuses_:
            if status["name"] == name:
                return status['id']
    
    def get_status_name(self, id):
        for status in self.statuses_:
            if status["id"] == id:
                return status['name']
    
    def get_next_status(self, current_status_id):
        no_of_elements = len(self.statuses_)
        for status in self.statuses_:
            if status['id'] == current_status_id:
                pos = self.statuses_.index(status)
                #if it is not end of the status list return next status else the first status
                if pos < no_of_elements - 1:
                    return self.statuses_[pos + 1]
                else:
                    return self.statuses_[0]

                

class Item:
    def __init__(self, id, state, title, date_complete=None):
        self.id = id
        self.status = state
        self.title = title
        self.complete_date = date_complete
    
    @property
    def get_item(self):
        return {'id' : self.id, 'status' : self.status, 'title' : self.title, 'complete_date' : self.complete_date}
    
    def complete_item(self, next_status):
        
        url = "https://api.trello.com/1/cards/" + self.id

       
        if next_status['name'] == "To Do":
            self.complete_date = ''

        query = {
                    'key' : app.config.get("T_KEY"),
                    'token': app.config.get("T_TOKEN"),
                    'due': self.complete_date,
                    'idList': next_status['id']
                }

        requests.request("PUT", url, params=query)

    @staticmethod
    def get_task_on_the_board(task_id): 
        
        board_id = os.environ.get('TRELLO_BOARD_ID')

        url = "https://api.trello.com/1/boards/" + board_id + "/cards/" + task_id

        query = {
                    'key' : app.config.get("T_KEY"),
                    'token': app.config.get("T_TOKEN"),
                    'fields': 'id,name,idBoard,idList,due'
            }

        response = requests.request("GET", url, params=query).json()

        return response

class Items:
    def __init__(self):
        board_id = os.environ.get('TRELLO_BOARD_ID')
    
        url = "https://api.trello.com/1/boards/" + board_id + "/cards"

        query = {
                'key' : app.config.get("T_KEY"),
                'token': app.config.get("T_TOKEN"),
                'fields' : 'id,name,idBoard,idList,due'
            }

        response = requests.request("GET", url, params=query)

        #get a list of items
        statusList = StatusList()

        self.items = []

        for task in response.json():
            date_str = ""
            if task['due'] != None:
                date_str = datetime.fromisoformat(task['due'] [:-1]).strftime("%c")
                item = Item(task['id'], 
                            statusList.get_status_name(task['idList']),
                            task['name'],
                            date_str)
                self.items.append(item.get_item)
            else:
                item = Item(task['id'], 
                            statusList.get_status_name(task['idList']),
                            task['name'],
                            date_str)
                self.items.append(item.get_item)


    
    @property
    def get_items(self):
        return [ item for item in self.items]

    
    def add_item(self, title, list_id):
        
        #Api call
        url = "https://api.trello.com/1/cards"
        query = {
                    'key' : app.config.get("T_KEY"),
                    'token': app.config.get("T_TOKEN"),
                    'idList': list_id,
                    'name' : title,
                    'desc' : title
            }
        
        response = requests.request("POST",url, params=query).json()
        item = Item(response['id'], "To Do", response['name'], response['due'])

        # Add the item to the list
        self.items.append(item)