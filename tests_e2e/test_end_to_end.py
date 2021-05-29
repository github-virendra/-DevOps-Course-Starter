import os
import pytest
from threading import Thread
from todo_app.data.trello_items import Board
from dotenv import find_dotenv, load_dotenv
from todo_app import app 
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


file_path = find_dotenv('.env')
print('env File path : ' + file_path + '\n')
load_dotenv(file_path, override=True)

@pytest.fixture(scope="module")
def driver():
    opts = Options()
    opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    ##with Chrome('/app/chromedriver', options=opts) as driver:
    #with Chrome('/usr/local/bin/chromedriver', options=opts) as driver:
    with Chrome(ChromeDriverManager().install(), options=opts) as driver:
    #with Chrome() as driver:
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
        print('Board id: ' + board.board_id + '\n')
 
        # start the app in its own thread.
        thread = Thread(target=lambda: application.run(use_reloader=False))
        thread.daemon = True
        thread.start()

        yield app
    
        # Tear Down
        thread.join(1)
        board.delete_board()

def test_task_journey(driver, test_app):
    print('Test_task_journey: Testing Index page\n')
    driver.get('http://localhost:5000/')

    assert driver.title == 'To-Do App'

def test_add_task_journey(driver, test_app):
    print('\nTest_add_task_journey : Add a task')
    driver.get('http://localhost:5000/')

    elem = driver.find_element_by_name("Title")
    elem.send_keys("Task A")
    elem.send_keys(Keys.RETURN)

    id = driver.find_element_by_xpath('//table[1]/tbody/tr['+str(2)+']/td['+str(1)+']').text
    status = driver.find_element_by_xpath('//table[1]/tbody/tr['+str(2)+']/td['+str(2)+']').text
    title = driver.find_element_by_xpath('//table[1]/tbody/tr['+str(2)+']/td['+str(3)+']').text

    print('id :', id, 'Status :', status, 'Title :' , title)
    assert status == 'To Do'
    assert title == 'Task A' 

def test_doing_task_journey(driver, test_app):
    print('\nTest_doing_task_journey: start Doing the task')
    driver.get('http://localhost:5000/')

    #fetch the form element
    form_ele = driver.find_element_by_xpath('//table[1]/tbody/tr['+'2'+']/td['+'4'+']')
    submit_button = form_ele.find_element(By.NAME,'taskId')
    submit_button.click()
    print('Clicked submit button')
    print('Moving task from To Do to Doing')

    status = driver.find_element_by_xpath('//table[2]/tbody/tr['+str(2)+']/td['+str(2)+']').text
    title = driver.find_element_by_xpath('//table[2]/tbody/tr['+str(2)+']/td['+str(3)+']').text
  
    print('Status :', status, 'Title :' , title)
    assert status == 'Doing'
    assert title == 'Task A' 


def test_done_task_journey(driver, test_app):
    print('\nTest_done_task_journey : Moving task to Done')
    driver.get('http://localhost:5000/')

    #get the form element
    form_ele = driver.find_element_by_xpath('//table[2]/tbody/tr['+'2'+']/td['+'4'+']')
    submit_button = form_ele.find_element(By.NAME,'taskId')
    submit_button.click()
    print('Clicked submit button')
    print('Moving task from Doing to Done')

    status = driver.find_element_by_xpath('//table[3]/tbody/tr['+str(2)+']/td['+str(2)+']').text
    title = driver.find_element_by_xpath('//table[3]/tbody/tr['+str(2)+']/td['+str(3)+']').text

    print('Status :', status, 'Title :' , title)
    assert status == 'Done'
    assert title == 'Task A' 


def test_reset_task_journey(driver, test_app):
    print('\nTest_reset_task_journey : Restting the task back to ToDo')
    driver.get('http://localhost:5000/')

    form_ele = driver.find_element_by_xpath('//table[3]/tbody/tr['+'2'+']/td['+'4'+']')
    submit_button = form_ele.find_element(By.NAME,'taskId')
    submit_button.click()
    print('Clicked submit button')
    print('Reset task, moving from Done back to To Do')

    status = driver.find_element_by_xpath('//table[1]/tbody/tr['+str(2)+']/td['+str(2)+']').text
    title = driver.find_element_by_xpath('//table[1]/tbody/tr['+str(2)+']/td['+str(3)+']').text

    print('Status :', status, 'Title :' , title)
    assert status == 'To Do'
    assert title == 'Task A' 