from flask import Flask, render_template, request, redirect, url_for
from todo_app.data import session_items

from todo_app.data.items import Payload
from todo_app.data.items import TrelloBoard
from todo_app.data.items import TrelloStatus
from todo_app.data.items import TrelloTask

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)



@app.route('/')
def index():
    #Get a board
    board = TrelloBoard.get_board('5fb59a498ec194253c614ac7')
    return render_template('index.html', items=board.get_tasks_on_a_board())
  
@app.route('/createNewToDoItems', methods=['POST'])
def create():
    #get the task item to add
    item  = request.form.get('Title')
    #Add the task item to ToDo List
    TrelloBoard.add_item(item)

    return redirect(url_for('index'))
 
@app.route('/complete_item', methods=['POST'])
def update_items():
 
    #Get the card details to update
    card_id = request.form.get('cardId')
    #Get a board
    board = TrelloBoard.get_board('5fb59a498ec194253c614ac7')
    board.complete_item(board,card_id)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
