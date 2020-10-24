from flask import Flask, render_template, request, redirect, url_for
from todo_app.data import session_items 

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)


#@app.route('/')
#def index():
#   return render_template('index.html',items=session_items.get_items())


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
       session_items.add_item(request.form.get('Title'))


    return render_template('index.html',items=session_items.get_items())

@app.route('/result', methods=['POST'])
def create():
    print("in Create function" + str(request.form.get('Title')))
    item  = request.form.get('Title')
    if item != '':
        session_items.add_item(item)
    return redirect(url_for('index'))
 


if __name__ == '__main__':
    app.run()
