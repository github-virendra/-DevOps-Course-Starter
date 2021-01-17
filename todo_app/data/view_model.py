 
from datetime import datetime 

class ViewModel:
    def __init__(self, items, date=datetime.now()):
        self.items_ = items
        self.today_ = date

    @property
    def items(self):
        return self.items_


    @property
    def todo(self):
        todo_items =  [item for item in self.items_ if item['status'] == 'To Do']
        return todo_items

    @property
    def doing(self):
        doing_items = [item for item in self.items_ if item['status'] == 'Doing']
        return doing_items

    @property
    def done(self):
        done_items = [item for item in self.items_ if item['status'] == 'Done']
        return done_items

    @property
    def show_all_done(self):
        done_items = self.done

        if len(done_items) < 5:
            self.items_=[]
            return done_items
        else:
             show_recent_done_items = self.recent_done_items
             return show_recent_done_items

    @property
    def recent_done_items(self):
        all_done_items = self.done
 
        recent_items = [item for item in all_done_items if datetime.strptime(item['complete_date'],"%c").date() == self.today_.date() or datetime.strptime(item['complete_date'],"%c").date() > self.today_.date()]

        older_items = [item for item in all_done_items if item not in recent_items]
        # print('In recent_done_items : items that are old')
        # print(older_items)
        self.items_ = older_items
        return recent_items

    @property
    def older_done_items(self):
        all_done_items = self.done

        #get the items with date differnce  greater than 0

        older_items = [item for item in all_done_items if (self.today_ - datetime.strptime(item['complete_date'],"%c")).total_seconds() > 0]

        # print('Older Items :')
        # print(older_items)
        return older_items

    @classmethod
    def view_model_with_sorted_items(cls,items, date=datetime.now()):
        sorted_list = [item for item in items if not item['status'] == 'Done']
        done_items = [item for item in items if item['status'] == 'Done']
        done_items.sort(key = lambda item: datetime.strptime(item['complete_date'],"%c"))
        for item in done_items:
            sorted_list.append(item)
        
        return cls(sorted_list,date)

        

        