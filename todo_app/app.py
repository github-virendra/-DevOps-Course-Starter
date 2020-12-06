from flask import Flask, render_template, request, redirect, url_for
from todo_app.data import session_items, trello_items 


from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)




@app.route('/')
def index():
    #return render_template('index.html', items=session_items.get_items())
    data=trello_items.get_items()
    return render_template('index.html', items=data)

@app.route('/createNewToDoItems', methods=['POST'])
def create():
    item  = request.form.get('Title')
    print(item)
    trello_items.add_item(item)
    return redirect(url_for('index'))
 
@app.route('/complete_item', methods=['POST'])
def update_items():
    print("In Update Items")
    data = request.form.get('cardId')
    print(data)
    trello_items.complete_item(data)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
