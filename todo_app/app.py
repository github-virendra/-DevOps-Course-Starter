from flask import Flask, render_template, request, redirect, url_for
#from todo_app.data import session_items

from todo_app.data.items import Payload
from todo_app.data.items import TrelloBoard
from todo_app.data.items import TrelloStatus
from todo_app.data.items import TrelloTask

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())



@app.route('/')
def index():
    #Get a board
    board_id = app.config.get('TRELLO_BOARD_ID')
    board = TrelloBoard.get_board(board_id)
    board.get_items()
    return render_template('index.html', items=board.get_tasks_on_a_board())
  
@app.route('/createNewToDoItems', methods=['POST'])
def create():
    #get the task item to add
    new_task  = request.form.get('Title')
    board_id = app.config.get('TRELLO_BOARD_ID')
    board = TrelloBoard.get_board(board_id)
    todo_status = board.get_status(name = 'To Do')
    todo_status.create_task(new_task)

    return redirect(url_for('index'))
 
@app.route('/complete_item', methods=['POST'])
def update_items():
 
    #Get the card details to update
    task_id = request.form.get('taskId')
    #Get a board
    board_id = app.config.get('TRELLO_BOARD_ID')
    board = TrelloBoard.get_board(board_id)
  
    task = board.get_task(task_id)
    #Get the List the card is in
    status_id = task.get_task_status_id()
    status_name = task.get_status()
    #get next status of the card
    next_status_id = board.get_next_status_of_the_task(status_id)
    task.update_task_status(next_status_id)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
