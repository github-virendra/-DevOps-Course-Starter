from todo_app.data.view_model import ViewModel
from datetime import datetime


def test_just_the_todo_items():
    # Arrange
    items = [
        { 'id': 1, 'status': 'Doing', 'title': 'List saved todo items' },
        { 'id': 2, 'status': 'To Do', 'title': 'Allow new items to be added' }
    ]
    view_model = ViewModel(items)

    # Act
    todo_items = view_model.todo

    # Assert
    for item in todo_items:
        assert item['status'] == "To Do"

def test_just_the_doing_items():
    # Arrange
    items = [
        { 'id': 1, 'status': 'Doing', 'title': 'List saved todo items' },
        { 'id': 2, 'status': 'To Do', 'title': 'Allow new items to be added' }
    ]
    view_model = ViewModel(items)

    # Act
    doing_items = view_model.doing

    # Assert
    for item in doing_items:
        assert item['status'] == "Doing"

def test_just_the_done_items():
    # Arrange
    items = [
        { 'id': 1, 'status': 'Doing', 'title': 'List saved todo items' },
        { 'id': 2, 'status': 'To Do', 'title': 'Allow new items to be added' },
        { 'id': 3, 'status': 'Done', 'title': 'Allow items to be updated','complete_date' :'Mon Dec 21 11:46:31 2020' }
    ]
    view_model = ViewModel.view_model_with_sorted_items(items, datetime(2020, 12, 21))

    # Act
    don_items = view_model.done

    # Assert
    for item in don_items:
        assert item['status'] == "Done"


def test_show_all_done_items():
    # Arrange
    items = [
        { 'id': 1, 'status': 'Doing', 'title': 'List saved todo items' },
        { 'id': 2, 'status': 'To Do', 'title': 'Allow new items to be added'},
        { 'id': 3, 'status': 'Done', 'title': 'Task 1','complete_date' :'Mon Dec 21 11:46:31 2020'},
        { 'id': 4, 'status': 'Done', 'title': 'Task 2','complete_date' :'Mon Dec 21 11:46:31 2020'},
        { 'id': 5, 'status': 'Done', 'title': 'Task 3','complete_date' :'Mon Dec 21 11:46:31 2020'},
        { 'id': 6, 'status': 'Done', 'title': 'Task 4','complete_date' :'Mon Dec 20 11:46:31 2020'}

    ]
    view_model = ViewModel.view_model_with_sorted_items(items, datetime(2020, 12, 21))
    

    # Act
    show_all_done_items = view_model.show_all_done
    count_all_done_items = len(show_all_done_items)

    # Assert
    assert  count_all_done_items == 4

def test_show_recent_done_items():
    # Arrange
    items = [
        { 'id': 1, 'status': 'Doing', 'title': 'List saved todo items'},
        { 'id': 2, 'status': 'To Do', 'title': 'Allow new items to be added'},
        { 'id': 3, 'status': 'Done', 'title': 'Task 1','complete_date' :'Mon Dec 21 11:46:31 2020'},
        { 'id': 4, 'status': 'Done', 'title': 'Task 2','complete_date' :'Mon Dec 21 11:56:31 2020'},
        { 'id': 5, 'status': 'Done', 'title': 'Task 3','complete_date' :'Mon Dec 21 12:46:31 2020'},
        { 'id': 6, 'status': 'Done', 'title': 'Task 4','complete_date' :'Mon Dec 21 9:46:31 2020'},
        { 'id': 7, 'status': 'Done', 'title': 'Task 5','complete_date' :'Mon Dec 21 14:46:31 2020'},
        { 'id': 8, 'status': 'Done', 'title': 'Task 6','complete_date' :'Mon Dec 21 15:46:31 2020'},
        { 'id': 9, 'status': 'Done', 'title': 'Task 7','complete_date' :'Mon Dec 21 10:10:31 2020'},
        { 'id': 10, 'status': 'Done', 'title': 'Task 8','complete_date' :'Mon Dec 20 11:46:31 2020'}

    ]
    view_model = ViewModel.view_model_with_sorted_items(items, datetime(2020, 12, 21))
    id_of_recent_items=[3,4,5,6,7,8,9]
    
    # Act
    recent_done_items = view_model.recent_done_items
    
    # Assert
    for item in recent_done_items:
        assert item['id'] in id_of_recent_items

    
def test_show_older_done_items():
    # Arrange
    items = [
        { 'id': 1, 'status': 'Doing', 'title': 'List saved todo items'},
        { 'id': 2, 'status': 'To Do', 'title': 'Allow new items to be added'},
        { 'id': 3, 'status': 'Done', 'title': 'Task 1','complete_date' :'Mon Dec 21 11:46:31 2020'},
        { 'id': 4, 'status': 'Done', 'title': 'Task 2','complete_date' :'Mon Dec 21 11:56:31 2020'},
        { 'id': 5, 'status': 'Done', 'title': 'Task 3','complete_date' :'Mon Dec 21 12:46:31 2020'},
        { 'id': 6, 'status': 'Done', 'title': 'Task 4','complete_date' :'Mon Dec 21 9:46:31 2020'},
        { 'id': 7, 'status': 'Done', 'title': 'Task 5','complete_date' :'Mon Dec 21 14:46:31 2020'},
        { 'id': 8, 'status': 'Done', 'title': 'Task 6','complete_date' :'Mon Dec 21 15:46:31 2020'},
        { 'id': 9, 'status': 'Done', 'title': 'Task 7','complete_date' :'Mon Dec 21 10:10:31 2020'},
        { 'id': 10, 'status': 'Done', 'title': 'Task 8','complete_date' :'Mon Dec 20 11:46:31 2020'}

    ]
    view_model = ViewModel.view_model_with_sorted_items(items,datetime(2020, 12, 21))
    id_of_old_items=[10]
    
    # Act
    older_done_items = view_model.older_done_items
    
    # Assert
    for item in older_done_items:
        assert item['id'] in id_of_old_items

def test_show_all_done_and_older_done_items():
    # Arrange
    items = [
        { 'id': 1, 'status': 'Doing', 'title': 'List saved todo items'},
        { 'id': 2, 'status': 'To Do', 'title': 'Allow new items to be added'},
        { 'id': 3, 'status': 'Done', 'title': 'Task 1','complete_date' :'Mon Dec 21 11:46:31 2020'},
        { 'id': 4, 'status': 'Done', 'title': 'Task 8','complete_date' :'Mon Dec 20 11:46:31 2020'}

    ]
    view_model = ViewModel.view_model_with_sorted_items(items,datetime(2020, 12, 21))
        
    # Act
    show_all_done_items = view_model.show_all_done
    count_all_done_items = len(show_all_done_items)
    older_done_items = view_model.older_done_items
    count_older_done_items = len(older_done_items)
    
    # Assert
    assert  count_all_done_items == 2 
    assert  count_older_done_items == 0