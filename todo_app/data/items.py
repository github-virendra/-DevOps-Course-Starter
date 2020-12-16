from flask import session, current_app as app
import requests

class TrelloTask(object):
    """
    blue print for trello tasks
    """
    def __init__(self,id, title, status):
        self.task_id = id
        self.task_title = title
        self.task_status = status

class TrelloStatus(object):
    """
    blue print for trello list
    """

    def __init__(self, id, name):
        self.status_id = id
        self.status = name
        self.items:TrelloTask = []

    def get_status_name(self):
        return self.status

    def get_status_id(self):
        return self.status_id

    def get_tasks(self):
        return self.items


class TrelloBoard(object):
    """
    blue print for trello board
    """

    def __init__(self, id, name):
        self.board_id = id
        self.board_name = name
        self.list_:TrelloStatus = []

    def get_board_lists(self):
        return self.list_
    
    def set_board_lists(self, value):
        self.list_.append(value)

    def get_board_id(self):
        return self.board_id
    
    def get_a_list_on_a_board(self, **listArgs)-> TrelloStatus:
        for status in self.list_:
            print("In get_a_list_on_a_Board")
            for key, value in listArgs.items():
                if key == 'id':
                    if status.get_status_id() == value:
                        return status
                if key == 'name':
                    if status.get_status_name() == value:
                        return status

    def get_status_id(self, name):
        for status in self.list_:
            print("In get_status_id")
            if status.get_status_name() == name:
                return status.get_status_id()

    def get_status_name(self, id):
        for status in self.list_:
            print("In get_status_name")
            if status.get_status_id() == id:
                return status.get_status_name()
    
    def get_the_status_list(self,query_string='id'):
        """
        returns list of Status by name or by id
        querystring can be 'name' or 'id'
        default is 'id'
        """
        status_list_by_name = list()
        status_list_by_id = list()

        for status in self.list_:
            status_list_by_name.append(status.get_status_name())
            status_list_by_id.append(status.get_status_id())
        if query_string == 'name':
            return status_list_by_name
        else:
            return status_list_by_id

    def get_next_status_of_the_card(self, status_id)->TrelloStatus:
        status_list_by_id = self.get_the_status_list()
        status_list_by_name = self.get_the_status_list('name')
        position = status_list_by_id.index(status_id)

        list_len = len(status_list_by_id)

        print('Current Position :' + str(position))
        print('Current Id :' + status_list_by_id[position])
        print('Current Status :' + status_list_by_name[position])

        #if it is the last status in the list
        if(position + 1) == list_len:
            print('Position :' + str(position))
            print('Reached End of the status list, assinging back ToDo')
            return status_list_by_id[0]
        else:
            print ('The next Status in the list is : ' + status_list_by_name[position + 1])
            return status_list_by_id[position + 1]

    def get_tasks_on_a_board(self):
        status_list = self.get_board_lists()
        board_tasks=[]
        for status_ in status_list:
            for task in status_.get_tasks():
                board_tasks.append(task)

        return board_tasks


    

    @classmethod
    def get_board(cls, id):
        #Get a board
        board_id, board_name = (TrelloBoard.get_trello_board(id)).values()       
        board =  TrelloBoard(board_id, board_name)
        # Get items
        TrelloBoard.get_items(board)
        return board

    @classmethod
    def get_items(cls, board):

        board_id = board.get_board_id()
        status_dict = (Url.get_lists_on_a_Board(board_id)).json()
        
        for status in status_dict:
            task_list = TrelloStatus(status['id'], status['name'])
        
            for task in status['cards']:
                task_ = TrelloTask(task['id'],task['name'],task_list.status)
                task_list.items.append(task_)
    
            board.list_.append(task_list)
 
        return board
    
    @classmethod
    def complete_item(cls, board, card_id):
        #Get the List the card is in
        status_id = TrelloBoard.get_the_status_id_of_card(card_id)
        status = board.get_a_list_on_a_board(id=status_id)

        print("The Card belongs to List:", status.get_status_name())
        #get next status of the card
        next_status_id = board.get_next_status_of_the_card(status_id)
        next_status = board.get_a_list_on_a_board(id=next_status_id)
        print("Next Status Name :", next_status.get_status_name())
        TrelloBoard.update_card_status(card_id, next_status_id)

    @staticmethod
    def update_card_status(id, status_id_to_update_to):
        item = (Url.update_cardstatus(id, status_id_to_update_to)).json()
        return item

    @staticmethod
    def get_the_status_id_of_card(card_id):
        print("In get_the_status_id_of_card, card_id :" + str(card_id))
        status_ = (Url.get_card_status(card_id)).json()

        print(status_)
        return status_['id']

    @staticmethod
    def add_item(title):
        board = TrelloBoard.get_board('5fb59a498ec194253c614ac7')
        status_id = board.get_status_id('To Do')
        task = (Url.add_item_to_ToDo_list(title, status_id)).json()
        return task

    @staticmethod
    def get_trello_board(id):
        response = (Url.get_TrelloBoard(id)).json()
        return response
      
    @staticmethod
    def get_statuses_on_a_board(board):
        print("In getLists_On_A_Board() - Made a request")
        status_list = (Url.get_lists_on_a_Board(board.get_board_id())).json()
      
        for status in status_list:
            print(status['id'])
            print(status['name'])
            board.set_board_lists(TrelloStatus(status['id'], status['name']))
        
        for status in board.get_board_lists():
            print("Status Name: ", status.get_status_name())
            print("Status id: ", status.get_status_id())
    
class Url():
    url_base = 'https://api.trello.com/1'

    @classmethod
    def get_TrelloBoard(cls, resource):
        url_ = Url.url_base + '/boards/' + resource

        print("In Url: getTrelloBoard")
        print("URL String :" + url_)
        query_string = {'fields':'name'}
        data = Payload(query_string)
        #Get a board
        response = requests.get(url_ , params=data.get_pay_load())
        return response
    
    @classmethod    
    def get_lists_on_a_Board(cls,board_id):
        print("In get_lists_on_a_Board()")
        url_ = Url.url_base + '/boards/' + board_id + '/lists'
        print(url_)
        query_string = {'cards':'all', 'card_fields':'idBoard,idList,name,desc'}
        data = Payload(query_string)
        response = requests.get(url_, params=data.get_pay_load())
        return response


    @classmethod
    def get_card_status(cls,card_id):
        url_ = Url.url_base + '/cards/' + card_id + '/list'
        print(url_)
        #get the list the card is on
        query_string = {"fields":"id"}
        response = requests.get(url_, params=Payload(query_string).get_pay_load())
        return response

    @classmethod
    def add_item_to_ToDo_list(cls,title, status_id):
        url_ = Url.url_base + '/cards'
        print("In add_item_to_ToDo_list() status_id : " +  status_id)
        print(url_)
        query_string = {'name' : title,'idList' : status_id}
        data = Payload(query_string)
        response = requests.post(url_, params=data.get_pay_load())
        return response

    @classmethod
    def update_cardstatus(cls, id, status_id_to_update_to):
        url_ = Url.url_base + '/cards/' + id
        print(url_)
        query_string = {'idList' : status_id_to_update_to}
        item = requests.put(url_, params=Payload(query_string).get_pay_load())
        return item

class Payload(object):
    """
    blue print for Trello API arguments
    """

    def __init__(self, query_string={}):
        self.key = app.config.get("T_KEY")
        self.token = app.config.get("T_TOKEN")
        self.apiArguments = {'key' : self.key, 'token': self.token} 
        self.add_query(query_string)
    
    def add_query(self, query_string):
        for key, value in query_string.items():
            self.apiArguments[key] = value


    def get_pay_load(self):
        print("Payload: " + str(self.apiArguments))
        return self.apiArguments
