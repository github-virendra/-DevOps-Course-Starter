from flask import Flask, render_template, request, redirect, url_for, session
#from todo_app.data import session_items, view_model
#from todo_app.data import view_model
from todo_app.data.view_model import ViewModel
from todo_app.flask_config import Config
from todo_app.data.trello_items import Item, Items, StatusList
import requests
from datetime import datetime
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())


    @app.route('/')
    def index():
        #items = session_items.get_items()
        items = Items().get_items
        item_view_model = ViewModel.view_model_with_sorted_items(items)
        return render_template('index.html', view_model = item_view_model)

    @app.route('/add_item', methods=['POST'])
    def create():
        item  = request.form.get('Title')
        #Add an item to To Do list
        # response = requests.get("https://api.trello.com/1/boards/5feb252a40ff2d09fa3a8eea/lists?key=acbb0995281e26011d961a4e89a5ddbf&token=f94c7ed49ec616120fb26fbd7aa8f40193b0b697f663aaa493250727ae61a9ca&fields=id,name,idBoard")
        #session["_DEFAULT_LISTS"] = response.json()
        status_id = StatusList().get_status_id("To Do")
        #session_items.add_item(item)
        Items().add_item(item,status_id)
        return redirect(url_for('index'))

    @app.route('/complete_item', methods=['POST'])
    def complete_item():
        #Get the card details to update
        task_id = request.form.get('taskId')

        #get the card on the board
        response = Item.get_task_on_the_board(task_id)
        # url = "https://api.trello.com/1/boards/5feb252a40ff2d09fa3a8eea/cards/" + task_id

        # query = {
        #             'key': 'acbb0995281e26011d961a4e89a5ddbf',
        #             'token': 'f94c7ed49ec616120fb26fbd7aa8f40193b0b697f663aaa493250727ae61a9ca',
        #              'fields': 'id,name,idBoard,idList,due'
        #     }


        # response = requests.request("GET", url, params=query).json()
        status_list = StatusList()
        status_id = response['idList']
        current_status = status_list.get_status_name(status_id)

        'updating task from Doing to Done update the completion date'
        if current_status == 'Doing':
            item = Item(response['id'],current_status,response['name'],datetime.now().strftime("%c"))
        else:
            item = Item(response['id'],current_status,response['name'],response['due'])
        
        next_status = status_list.get_next_status(status_id)
        item.complete_item(next_status)

        return redirect(url_for('index'))

    if __name__ == '__main__':
        app.run()

    return app