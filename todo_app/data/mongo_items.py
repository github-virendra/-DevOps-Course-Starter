from flask import current_app as app
from datetime import datetime 
import os
from todo_app.db import DBMongo


class Board:
    def __init__(self, name):

        self.board_id_ = DBMongo().create_board(name)
        print('Creating Board :' + self.board_id_)
        os.environ['MONGO_BOARD_ID'] = self.board_id_
    
    @property
    def board_id(self):
        return self.board_id_



    def delete_board(self):
        print('\nDeleting Board :' , self.board_id)
        result = DBMongo().delete_board(self.board_id)
        if result == True:
            print("Board Deleted")
            return True 


class StatusList:
    def __init__(self):

        board_id = os.environ.get('MONGO_BOARD_ID')
        response = DBMongo().get_lists_on_a_board(board_id)
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
        
      
        if next_status['name'] == "To Do":
            self.complete_date = None

        board_id = os.environ.get('MONGO_BOARD_ID')
        list_id= next_status['id']
        status_id = StatusList().get_status_id(self.status)
        newtask = dict([('_id', self.id),('status_name',self.status), ('status_id', status_id), ('next_status_listId',list_id), ('name',self.title), ('due', self.complete_date,)])
        DBMongo().complete_item(board_id,newtask)

    @staticmethod
    def get_task_on_the_board(task_id): 
        
        board_id = os.environ.get('MONGO_BOARD_ID')
        result = DBMongo().get_a_card_on_a_board(board_id,task_id)

        return result

class Items:
    def __init__(self):
        board_id = os.environ.get('MONGO_BOARD_ID')

        result = DBMongo().get_cards_on_a_board(board_id)

        #get a list of items
        statusList = StatusList()

        self.items = []

        for task in result:
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
        DBMongo().add_a_card_to_ToDoList(title,list_id)
