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
    
    def get_id(self):
        return self.task_id

    def get_task_status_id(self):
        print("In get_task_status_id, task_id :" + self.task_id)
        fields = "id"
        status_ = (TrelloApi.get_card_status(self.task_id, fields)).json()
        return status_['id']

    def get_status(self):
        fields = "name"
        status_ = (TrelloApi.get_card_status(self.task_id, fields)).json()
        self.task_status = status_['name']
        return status_['name']

    def update_task_status(self, status_id_to_update_to):
        TrelloApi.update_cardstatus(self.task_id, status_id_to_update_to).json()

 

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

    def create_task(self, title)->TrelloTask:
        response = (TrelloApi.add_task_to_list(title, self.status_id)).json()
        task = TrelloTask(response['id'],response['name'],self.get_status_name())
        self.add_task(task)
     
    def add_task(self, task:TrelloTask):
        self.get_tasks().append(TrelloTask(task.task_id, task.task_title, task.task_status))
        return task



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
    
    def add_lists(self, value):
        self.list_.append(value)

    def get_board_id(self):
        return self.board_id

    def get_items(self):

        query_string = {'cards':'all', 'card_fields':'idBoard,idList,name,desc'}
        status_dict = (TrelloApi.get_lists_on_a_Board(self.get_board_id(), query_string)).json()
        
        for status in status_dict:
            task_list = TrelloStatus(status['id'], status['name'])
        
            for task in status['cards']:
                task_ = TrelloTask(task['id'],task['name'],task_list.status)
                task_list.add_task(task_)
    
            self.add_lists(task_list)
     
    def get_status(self, **listArgs)-> TrelloStatus:
        status_dict = (TrelloApi.get_lists_on_a_Board(self.get_board_id())).json()
        for status in status_dict:
            task_list = TrelloStatus(status['id'], status['name'])
            for key, value in listArgs.items():
                if key == 'id':
                    if status['id'] == value:
                        self.add_lists(task_list)
                        return task_list
                if key == 'name':
                    if status['name'] == value:
                        self.add_lists(task_list)
                        return task_list

    def get_the_status_list(self,query_string='id'):
        """
        returns list of Status by name or by id
        querystring can be 'name' or 'id'
        default is 'id'
        """
        status_list_by_name = list()
        status_list_by_id = list()

        status_dict = TrelloApi.get_lists_on_a_Board(self.board_id).json()
        for status in status_dict:
            self.add_lists(TrelloStatus(status['id'], status['name']))
            status_list_by_id.append(status['id'])
            status_list_by_name.append(status['name'])

        if query_string == 'name':
            return status_list_by_name
        else:
            return status_list_by_id

    def get_next_status_of_the_task(self, status_id)->TrelloStatus:
        status_list_by_id = self.get_the_status_list()
        status_list_by_name = self.get_the_status_list('name')
        position = status_list_by_id.index(status_id)

        list_len = len(status_list_by_id)

        #if it is the last status in the list
        if(position + 1) == list_len:
            return status_list_by_id[0]
        else:
            return status_list_by_id[position + 1]

    def get_tasks_on_a_board(self):
        status_list = self.get_board_lists()
        board_tasks=[]
        for status_ in status_list:
            for task in status_.get_tasks():
                board_tasks.append(task)

        return board_tasks

    def get_task(self, task_id):
        item = TrelloApi.get_card_on_a_Board(self.board_id, task_id).json()
        status = self.get_status(id = item['idList'])
        task = TrelloTask(item['id'], item['name'],status.get_status_name())
        return task
  

    @classmethod
    def get_board(cls, id):
        #Get a board
        response = (TrelloApi.get_TrelloBoard(id)).json()
        board_id, board_name = response.values()       
        board =  TrelloBoard(board_id, board_name)
        return board

    
class TrelloApi():
    url_base = 'https://api.trello.com/1'

    @classmethod
    def get_TrelloBoard(cls, resource):
        url_ = TrelloApi.url_base + '/boards/' + resource

        query_parameters = {'fields':'name'}
        data = Payload(query_parameters)
        #Get a board
        response = requests.get(url_ , params=data.get_pay_load())
        return response
    
    @classmethod    
    def get_lists_on_a_Board(cls,board_id,query_parameters={}):
        url_ = TrelloApi.url_base + '/boards/' + board_id + '/lists'
        data = Payload(query_parameters)
        response = requests.get(url_, params=data.get_pay_load())
        return response

    @classmethod
    def get_card_on_a_Board(cls, board_id, task_id):
        url_ = TrelloApi.url_base + '/boards/' + board_id + '/cards/' + task_id
        query_parameters = {'fields':'id,name,idList'}
        data = Payload(query_parameters)
        response = requests.get(url_, params=data.get_pay_load())
        return response

    @classmethod
    def get_card_status(cls,card_id, fields=''):
        url_ = TrelloApi.url_base + '/cards/' + card_id + '/list'
        #get the list the card is on            
        query_parameters = {"fields":fields}
        response = requests.get(url_, params=Payload(query_parameters).get_pay_load())
        return response

    @classmethod
    def add_task_to_list(cls,title, status_id):
        url_ = TrelloApi.url_base + '/cards'
        query_parameters = {'name' : title,'idList' : status_id}
        data = Payload(query_parameters)
        response = requests.post(url_, params=data.get_pay_load())
        return response

    @classmethod
    def update_cardstatus(cls, id, status_id_to_update_to):
        url_ = TrelloApi.url_base + '/cards/' + id
        query_parameters = {'idList' : status_id_to_update_to}
        item = requests.put(url_, params=Payload(query_parameters).get_pay_load())
        return item

class Payload(object):
    """
    blue print for Trello API arguments
    """

    def __init__(self, query_string={}):
        self.apiArguments = {'key' : app.config.get("T_KEY"), 'token': app.config.get("T_TOKEN")}  
        self.add_query(query_string)
    
    def add_query(self, query_string):
        for key, value in query_string.items():
            self.apiArguments[key] = value


    def get_pay_load(self):
        return self.apiArguments
