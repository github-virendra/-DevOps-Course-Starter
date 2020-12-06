from flask import session, current_app as app
import requests





_DEFAULT_ITEMS = [
    { 'id': 1, 'status': 'Not Started', 'title': 'List saved todo items' },
    { 'id': 2, 'status': 'Not Started', 'title': 'Allow new items to be added' }
]




def get_items():
    """
    Fetches all saved items from the session.

    Returns:
        list: The list of saved items.
    """
    key = app.config.get("T_KEY")

    token = app.config.get("T_TOKEN")
    
    payload = {'key':key, 'token' : token, 'cards':'all', 'card_fields':'idBoard,idList,name,desc'}
    r = requests.get('https://api.trello.com/1/boards/5fb59a498ec194253c614ac7/lists', params=payload)
    
    listDict = r.json()
    board = {'boardid' : '5fb59a498ec194253c614ac7',
             'boardname':'S95R-M2'}
    board['taskList']=[]
    for listOfTasks in listDict:
        createList={}
        createList['id'] = listOfTasks['id']
        createList['name'] = listOfTasks['name']

        createList['cards'] = []

        for card in listOfTasks['cards']:
            listCard = {}
            listCard['id'] = card['id']
            listCard['name'] = card['name']
            listCard['status'] = createList['name']

            createList['cards'].append(listCard)

        board['taskList'].append(createList)
  
    return board




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