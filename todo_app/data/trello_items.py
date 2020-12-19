from flask import session, current_app as app
import requests
from todo_app.data.items import payload, trello_board, trello_list, trello_card


class t_items:
    def __init__(self):
        self.cards_On_A_Board = []
        self.status_list = []
        self.board = trello_board('5fb59a498ec194253c614ac7','S95R-M2')

    def getLists_On_A_Board(self):
        self.board.getBoardId()
        print("In getLists_On_A_Board()")
        url= 'https://api.trello.com/1/boards/' + self.board.getBoardId() + '/lists'
        print(url)
        listData = (requests.get(url, params=payload().getPayLoad())).json()
        print("In getLists_On_A_Board() - Made a request")
      
        for listDict in listData:
            print(listDict['id'])
            print(listDict['name'])
            self.status_list.append(trello_list(listDict['id'], listDict['name']))
        
        for status in self.status_list:
            print("Status Name: ", status.getStatusName())
            print("Status id: ", status.getStatusId())

    def get_the_status_Id_of_card(self, cardId):
        
        url = 'https://api.trello.com/1/cards/'+ cardId + '/list'
        print(url)

        #get the list the card is on
        queryString = {"fields":"id"}
        listData = (requests.get(url, params=payload(queryString).getPayLoad())).json()

        print(listData)
        return listData['id']

    def get_next_status_of_the_card(self,listId):
        self.getLists_On_A_Board()

        #get the first status in the status list
        statusId_at_start = self.status_list[0].getStatusId()
        list_len = len(self.status_list)

        #There is only one list
        if(list_len == 1):
            return None

        for status in self.status_list:
            position = self.status_list.index(status)

            if status.getStatusId() == listId:
                print('Current Status :' + status.getStatusName())
                print('Current Position :' + str(position))

                #if it is the last status in the list
                if(position + 1) == list_len:
                    print('Position :' + str(position))
                    print('Reached End of the status list, assinging back ToDo')
                    return statusId_at_start
                else:
                    print ('The next Status in the list is : ' + self.status_list[position + 1].getStatusName())
                    return self.status_list[position + 1].getStatusId()
                


    def get_items(self):
        """
        Fetches all saved items from the session.

        Returns:
            list: The list of saved items.
        """

        #get a board
        data = payload()
        queryString = {'cards':'all', 'card_fields':'idBoard,idList,name,desc'}
        data.addQuery(queryString)

        #Get lists on a board
        r = requests.get('https://api.trello.com/1/boards/5fb59a498ec194253c614ac7/lists', params=data.getPayLoad())
    
        listDict = r.json()

        #board = trello_board('5fb59a498ec194253c614ac7','S95R-M2')
    
        for listOfTasks in listDict:
            taskList = trello_list(listOfTasks['id'], listOfTasks['name'])
            self.status_list.append({'statusId' : taskList.listId, 'statusName' : taskList.listName})
        
            for card in listOfTasks['cards']:
                cardItem = trello_card(card['id'],card['name'],taskList.listName)
                taskList.items.append(cardItem)
    
            self.board.lists.append(taskList)
  
        return self.board

    def add_item(self,title):
        """
        Adds a new item with the specified title to the session.

        Args:
            title: The title of the item.

        Returns:
            item: The saved item.
        """
        key = app.config.get("T_KEY")
        #print("Trello Key " + key)

        token = app.config.get("T_TOKEN")
        #print("Trello Token : " + token)

        payload = {'key':key, 'token' : token,  'name' : title,'idList' : '5fb59a498ec194253c614aca'}
        item = requests.post('https://api.trello.com/1/cards', params=payload)
    
        return item

    def complete_item(self,id):
        key = app.config.get("T_KEY")
        print("Trello Key " + key)

        token = app.config.get("T_TOKEN")
        print("Trello Token : " + token)

        print("Card Id: ", id)
        # print("Staus to be updated to:", nextStatus)

        #Get the List the card is in
        listId = self.get_the_status_Id_of_card(id)

        for status in self.status_list:
            if status['id'] == listId:
                print("The Card belongs to List:", status['name'])

        #get next status of the card
        idList = self.get_next_status_of_the_card(listId)

        print("Next Status Id :", idList)

        for status in self.status_list:
            if status.getStatusId() == idList:
                print("Next Status Name :", status.getStatusName())
                print("Changing Card Status to :", status.getStatusName())

        if idList == None:
            print("Invalid Request...")

        
        payload = {'key':key, 'token' : token, 'idList' : idList}
        url = 'https://api.trello.com/1/cards/' + id
        print(url)
        item = requests.put(url, params=payload)

        return item
#===============
        

def get_items():
    """
    Fetches all saved items from the session.

    Returns:
        list: The list of saved items.
    """
    # key = app.config.get("T_KEY")

    # token = app.config.get("T_TOKEN")
    
    #dataload = {'key':key, 'token' : token, 'cards':'all', 'card_fields':'idBoard,idList,name,desc'}

    data = payload()
    queryString = {'cards':'all', 'card_fields':'idBoard,idList,name,desc'}
    data.addQuery(queryString)
    
    r = requests.get('https://api.trello.com/1/boards/5fb59a498ec194253c614ac7/lists', params=data.getPayLoad())
    
    listDict = r.json()

    board = trello_board('5fb59a498ec194253c614ac7','S95R-M2')
    
    for listOfTasks in listDict:
        taskList = trello_list(listOfTasks['id'], listOfTasks['name'])

        
        for card in listOfTasks['cards']:
            cardItem = trello_card(card['id'],card['name'],taskList.listName)
            taskList.items.append(cardItem)
    
        board.lists.append(taskList)
  
    return board

    # board = {'boardid' : '5fb59a498ec194253c614ac7',
    #          'boardname':'S95R-M2'}
    # board['taskList']=[]
    # for listOfTasks in listDict:
    #     createList={}
    #     createList['id'] = listOfTasks['id']
    #     createList['name'] = listOfTasks['name']

    #     createList['cards'] = []

    #     for card in listOfTasks['cards']:
    #         listCard = {}
    #         listCard['id'] = card['id']
    #         listCard['name'] = card['name']
    #         listCard['status'] = createList['name']

    #         createList['cards'].append(listCard)

    #     board['taskList'].append(createList)
  
    # return board




def get_item(id):
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    items = get_items()
    return next((item for item in items if item['id'] == int(id)), None)


def add_item(title):
    """
    Adds a new item with the specified title to the session.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.
    """
    key = app.config.get("T_KEY")
   #print("Trello Key " + key)

    token = app.config.get("T_TOKEN")
    #print("Trello Token : " + token)

    payload = {'key':key, 'token' : token,  'name' : title,'idList' : '5fb59a498ec194253c614aca'}
    item = requests.post('https://api.trello.com/1/cards', params=payload)
    
    return item


def save_item(item):
    """
    Updates an existing item in the session. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.
    """
    existing_items = get_items()
    updated_items = [item if item['id'] == existing_item['id'] else existing_item for existing_item in existing_items]

    session['items'] = updated_items

    return item

def complete_item(id):
    key = app.config.get("T_KEY")
    print("Trello Key " + key)

    token = app.config.get("T_TOKEN")
    print("Trello Token : " + token)

    print("Card Id: ", id)
    payload = {'key':key, 'token' : token, 'idList' : '5fb59a498ec194253c614ace'}
    url = 'https://api.trello.com/1/cards/' + id
    print(url)
    item = requests.put(url, params=payload)

    return item