import os
import pytest
from threading import Thread
from todo_app.data.trello_items import Board
from dotenv import find_dotenv, load_dotenv


file_path = find_dotenv('.env')
print(file_path)
load_dotenv(file_path, override=True)
print(os.environ.get('SECRET_KEY'))
print(os.environ.get('FLASK_ENV'))

from todo_app import app 


from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="module")
def driver():
    #print('in Driver')
    with Chrome() as driver:
        yield driver

@pytest.fixture(scope='module')
def test_app():
    print('Starting test_app')
           
    # construct the new application
    application = app.create_app()

    with application.app_context():
         # Create the new board & update the board id environment variable
        board = Board('Test Board 1')

        os.environ['TRELLO_BOARD_ID'] = board.board_id
        print('Board id: ' + board.board_id,': Board name: ',board.board_name )
        os.environ['TRELLO_BOARD_NAME'] = board.board_name

        # start the app in its own thread.
        thread = Thread(target=lambda: application.run(use_reloader=False))
        thread.daemon = True
        thread.start()

        yield app

    
        # Tear Down
        thread.join(1)
        
        board.delete_board()

def test_task_journey(driver, test_app):
    print('In test_task_journey: Testing Index page')
    driver.get('http://localhost:5000/')

    assert driver.title == 'To-Do App'

def test_add_task_journey(driver, test_app):
    print('In test_add_task_journey : Add a task')
    driver.get('http://localhost:5000/')
    #assert driver.title == 'To-Do App'
    elem = driver.find_element_by_name("Title")
    elem.send_keys("Task A")
    elem.send_keys(Keys.RETURN)

    task_rows = len(driver.find_elements_by_xpath('/html/body/div/div[2]/div/ul/table[1]/tbody/tr'))
    task_columns = len(driver.find_elements_by_xpath('/html/body/div/div[2]/div/ul/table[1]/tbody/tr[1]/th'))
    print('Fetched data from To Do table :')
    #print(task_rows)
    #print(task_columns)
    task=[]
    for row in range(2,task_rows+1):
        for col in range(1,task_columns+1):
            value = driver.find_element_by_xpath('/html/body/div/div[2]/div/ul/table[1]/tbody/tr['+str(row)+']/td['+str(col)+']').text
            print(value, end='    ')
            task.append(value)
        print()

    id,status,title = task
    print('id :', id, 'Status :', status, 'Title :' , title)
    assert status == 'To Do'
    assert title == 'Task A' 

def test_doing_task_journey(driver, test_app):
    print('In test_doing_task_journey: start Doing the task')
    driver.get('http://localhost:5000/')

    task_rows = len(driver.find_elements_by_xpath('/html/body/div/div[2]/div/ul/table[1]/tbody/tr'))
    task_columns = len(driver.find_elements_by_xpath('/html/body/div/div[2]/div/ul/table[1]/tbody/tr[2]/td'))
    print('Fetched data from To Do table :')
    # print(task_rows)
    # print(task_columns)
    task=[]
    for row in range(2,task_rows+1):
        for col in range(1,task_columns+1):
            value = driver.find_element_by_xpath('/html/body/div/div[2]/div/ul/table[1]/tbody/tr['+str(row)+']/td['+str(col)+']').text
            print(value, end='    ')
            task.append(value)
        print()

    id,status,title,form = task
    print('Status :', status, 'Title :' , title)
    
    print("Id of the task : ", id )

    #fetch the form element
    form_ele = driver.find_element_by_xpath('/html/body/div/div[2]/div/ul/table[1]/tbody/tr['+'2'+']/td['+'4'+']')
    submit_button = form_ele.find_element(By.NAME,'taskId')
    submit_button.click()
    print('Clicked submit button')
    print('Moving task from To Do to Doing')

    task_rows = len(driver.find_elements_by_xpath('/html/body/div/div[2]/div/ul/table[2]/tbody/tr'))
    task_columns = len(driver.find_elements_by_xpath('/html/body/div/div[2]/div/ul/table[2]/tbody/tr[1]/th'))
    print('Fetched data from Doing table :')
    # print(task_rows)
    # print(task_columns)
    task=[]
    for row in range(2,task_rows+1):
        for col in range(1,task_columns+1):
            value = driver.find_element_by_xpath('/html/body/div/div[2]/div/ul/table[2]/tbody/tr['+str(row)+']/td['+str(col)+']').text
            print(value, end='    ')
            task.append(value)
        print()

    id,status,title = task

    print('Status :', status, 'Title :' , title)
    assert status == 'Doing'
    assert title == 'Task A' 


def test_done_task_journey(driver, test_app):
    print('In test_done_task_journey : Moving task to Done')
    driver.get('http://localhost:5000/')


    task_rows = len(driver.find_elements_by_xpath('/html/body/div/div[2]/div/ul/table[2]/tbody/tr'))
    task_columns = len(driver.find_elements_by_xpath('/html/body/div/div[2]/div/ul/table[2]/tbody/tr[2]/td'))
    print('Fetched data from Doing table :')
    # print(task_rows)
    # print(task_columns)
    task=[]
    for row in range(2,task_rows+1):
        for col in range(1,task_columns+1):
            value = driver.find_element_by_xpath('/html/body/div/div[2]/div/ul/table[2]/tbody/tr['+str(row)+']/td['+str(col)+']').text
            print(value, end='    ')
            task.append(value)
        print()

    id,status,title,form = task
    print('Status :', status, 'Title :' , title)
    
    print("Id of the task : ", id )
    #get the form element
    form_ele = driver.find_element_by_xpath('/html/body/div/div[2]/div/ul/table[2]/tbody/tr['+'2'+']/td['+'4'+']')
    submit_button = form_ele.find_element(By.NAME,'taskId')
    submit_button.click()
    print('Clicked submit button')
    print('Moving task from Doing to Done')


    task_rows = len(driver.find_elements_by_xpath('/html/body/div/div[2]/div/ul/table[3]/tbody/tr'))
    task_columns = len(driver.find_elements_by_xpath('/html/body/div/div[2]/div/ul/table[3]/tbody/tr[1]/th'))
    #print('Fetched data from Done table :')
    # print(task_rows)
    # print(task_columns)
    task=[]
    for row in range(2,task_rows+1):
        for col in range(1,task_columns+1):
            value = driver.find_element_by_xpath('/html/body/div/div[2]/div/ul/table[3]/tbody/tr['+str(row)+']/td['+str(col)+']').text
            print(value, end='    ')
            task.append(value)
        print()

    id,status,title = task

    print('Status :', status, 'Title :' , title)
    assert status == 'Done'
    assert title == 'Task A' 


def test_reset_task_journey(driver, test_app):
    print('In test_reset_task_journey : Restting the task back to ToDo')
    driver.get('http://localhost:5000/')
    #assert driver.title == 'To-Do App'
   

    task_rows = len(driver.find_elements_by_xpath('/html/body/div/div[2]/div/ul/table[3]/tbody/tr'))
    task_columns = len(driver.find_elements_by_xpath('/html/body/div/div[2]/div/ul/table[3]/tbody/tr[2]/td'))
    print('Fetched data from Done table :')
    # print(task_rows)
    # print(task_columns)
    task=[]
    for row in range(2,task_rows+1):
        for col in range(1,task_columns+1):
            value = driver.find_element_by_xpath('/html/body/div/div[2]/div/ul/table[3]/tbody/tr['+str(row)+']/td['+str(col)+']').text
            print(value, end='    ')
            task.append(value)
        print()

    id,status,title,form = task
    print('Status :', status, 'Title :' , title)
    
    print("Id of the task : ", id )
    form_ele = driver.find_element_by_xpath('/html/body/div/div[2]/div/ul/table[3]/tbody/tr['+'2'+']/td['+'4'+']')
    submit_button = form_ele.find_element(By.NAME,'taskId')
    submit_button.click()
    print('Clicked submit button')
    print('Reset task, moving from Done back to To Do')

    task_rows = len(driver.find_elements_by_xpath('/html/body/div/div[2]/div/ul/table[1]/tbody/tr'))
    task_columns = len(driver.find_elements_by_xpath('/html/body/div/div[2]/div/ul/table[1]/tbody/tr[1]/th'))
    #print('Fetched data from To Do table :')
    print(task_rows)
    print(task_columns)
    task=[]
    for row in range(2,task_rows+1):
        for col in range(1,task_columns+1):
            value = driver.find_element_by_xpath('/html/body/div/div[2]/div/ul/table[1]/tbody/tr['+str(row)+']/td['+str(col)+']').text
            print(value, end='    ')
            task.append(value)
        print()

    id,status,title = task

    print('Status :', status, 'Title :' , title)
    assert status == 'To Do'
    assert title == 'Task A' 