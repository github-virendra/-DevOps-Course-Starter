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
        status_ = (Url.get_card_status(self.task_id, fields)).json()
        return status_['id']

    def get_status(self):
        print("In get_status, task_id :" + self.task_id)
        fields = "name"
        status_ = (Url.get_card_status(self.task_id, fields)).json()
        self.task_status = status_['name']
        return status_['name']

    def update_task_status(self, status_id_to_update_to):
        Url.update_cardstatus(self.task_id, status_id_to_update_to).json()

 

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
        response = (Url.add_task_to_list(title, self.status_id)).json()
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
        status_dict = (Url.get_lists_on_a_Board(self.get_board_id(), query_string)).json()
        
        for status in status_dict:
            task_list = TrelloStatus(status['id'], status['name'])
        
            for task in status['cards']:
                task_ = TrelloTask(task['id'],task['name'],task_list.status)
                task_list.add_task(task_)
    
            self.add_lists(task_list)
     
    def get_status(self, **listArgs)-> TrelloStatus:
        status_dict = (Url.get_lists_on_a_Board(self.get_board_id())).json()
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

        status_dict = Url.get_lists_on_a_Board(self.board_id).json()
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

    def get_task(self, task_id):
        item = Url.get_card_on_a_Board(self.board_id, task_id).json()
        status = self.get_status(id = item['idList'])
        task = TrelloTask(item['id'], item['name'],status.get_status_name())
        return task
  

    @classmethod
    def get_board(cls, id):
        #Get a board
        response = (Url.get_TrelloBoard(id)).json()
        board_id, board_name = response.values()       
        board =  TrelloBoard(board_id, board_name)
        return board

    
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
    def get_lists_on_a_Board(cls,board_id,query_string={}):
        print("In get_lists_on_a_Board()")
        url_ = Url.url_base + '/boards/' + board_id + '/lists'
        print(url_)
        data = Payload(query_string)
        response = requests.get(url_, params=data.get_pay_load())
        return response

    @classmethod
    def get_card_on_a_Board(cls, board_id, task_id):
        print('In get_card_on_a_Board()')
        url_ = Url.url_base + '/boards/' + board_id + '/cards/' + task_id
        print(url_)
        query_string = {'fields':'id,name,idList'}
        data = Payload(query_string)
        response = requests.get(url_, params=data.get_pay_load())
        return response

    @classmethod
    def get_card_status(cls,card_id, fields=''):
        url_ = Url.url_base + '/cards/' + card_id + '/list'
        print(url_)
        #get the list the card is on            
        query_string = {"fields":fields}
        response = requests.get(url_, params=Payload(query_string).get_pay_load())
        return response

    @classmethod
    def add_task_to_list(cls,title, status_id):
        url_ = Url.url_base + '/cards'
        print("In add_task_to_list() status_id : " +  status_id)
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
