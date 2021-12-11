from flask import Flask, render_template, request, redirect, url_for, session
from todo_app.data.view_model import ViewModel
from todo_app.flask_config import Config
from todo_app.data.mongo_items import Item, Items, StatusList
from datetime import datetime, timezone
import os



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    @app.route('/')
    def index():
        items = Items().get_items
        item_view_model = ViewModel.view_model_with_sorted_items(items)
        return render_template('index.html', view_model = item_view_model)

    @app.route('/add_item', methods=['POST'])
    def create():
        item  = request.form.get('Title')
        #Add an item to To Do list
        status_id = StatusList().get_status_id("To Do")
        Items().add_item(item,status_id)
        return redirect(url_for('index'))

    @app.route('/complete_item', methods=['POST'])
    def complete_item():
        #Get the card details to update
        task_id = request.form.get('taskId')
   
        #get the card on the board
        response = Item.get_task_on_the_board(task_id)

        status_list = StatusList()
        status_id = response['idList']
        current_status = status_list.get_status_name(status_id)

        'updating task from Doing to Done update the completion date'
        if current_status == 'Doing':
            item = Item(response['id'],current_status,response['name'],datetime.now(timezone.utc).isoformat().replace("+00:00","Z"))
        else:
            item = Item(response['id'],current_status,response['name'],response['due'])
        
        next_status = status_list.get_next_status(status_id)
        item.complete_item(next_status)

        return redirect(url_for('index'))
    return app

if __name__ == '__main__':
    app = create_app()
    app.run()

