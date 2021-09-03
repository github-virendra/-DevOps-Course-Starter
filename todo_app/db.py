from pymongo import MongoClient, response
from pymongo.errors import ConnectionFailure
from bson.objectid import ObjectId
import sys
import os
from flask import current_app as app

from requests.models import Response

class DBMongo:
    def __init__(self):

        try:
            url = "mongodb+srv://" + str(os.environ['M_KEY']) + ":" + str(os.environ["M_TOKEN"]) + "@virendra-mongodb-cluste.280hx.mongodb.net/Virendra-MongoDB-Cluster0?retryWrites=true&w=majority"
            self.client = MongoClient(url)
            self.db = self.client['TodoDB']
            print("Connected to MongoDB successfully")
            
        except ConnectionFailure as e:
            sys.stderr.write("Could not connect to MongoDB: %s" % e)
            sys.exit(1)

    def get_db(self):
        return self.db

    def create_board(self,name):
        board = {
                    "name" : name,
                    "desc" : name,
                    "_id" : str(ObjectId()),
                    "status" : [
		                        {
		                            "_id": str(ObjectId()),
                                    "name":"To Do",
                                    "cards":[
                                                {
                                                }
                                            ]
		                        },
		                        {
		                            "_id": str(ObjectId()),
                                    "name": "Doing",
                                    "cards":[
                                                {
                                                }
                                            ]
		                        },
		                        {
		                            "_id": str(ObjectId()),
                                    "name": "Done",
                                    "cards": [
                                                {
                                                }
                                            ]
		                        }
	                        ]
                }
        result = self.get_db().Board.insert_one(board)
        print("Created Board :" + str(result.inserted_id))
        return str(result.inserted_id)

    def delete_board(self, board_id):
        result = self.get_db().Board.delete_one({'_id':board_id})
        print("DBMongo Deleted Board :" + str(result.deleted_count))
        return result.deleted_count > 0


    def get_cards_on_a_board(self,board_id = os.environ.get('MONGO_BOARD_ID')):
        cards_on_a_board=[]        
        for board in self.db.Board.find({'_id' : board_id}):
            idBoard=board['_id']
            for status in board['status']:
                idList=status['_id']
                for card in status['cards']:
                    if (len(card) > 0):
                        id = card['_id']
                        name = card['name']
                        due = card['due']
                        item = {"id": id, "name": name ,"idBoard": idBoard, "idList":idList,"due":due}
                        cards_on_a_board.append(item)
                            
        return cards_on_a_board

    def get_lists_on_a_board(self,board_id = os.environ.get('MONGO_BOARD_ID')):
        status_on_a_board=[]
        for board in self.db.Board.find({'_id' : board_id}):
            idBoard=board['_id']
            for status in board['status']:
                id=status['_id']
                name = status['name']
                status= {"id": id, "name": name ,"idBoard": idBoard}
                status_on_a_board.append(status)
        return status_on_a_board

    def add_a_card_to_ToDoList(self,title, list_id):
        cardid = str(ObjectId())
        newCard =   { 
                        "_id" : cardid,
                       "name": title,
                        "due": None
                    }
        board_id = os.environ.get('MONGO_BOARD_ID')
        self.get_db().Board.update_one({'_id':board_id,'status._id':list_id},
                                      {"$push":{'status.$.cards':newCard}})

    def get_a_card_on_a_board(self,board_id,task_id):
        cards = self.get_db().Board.aggregate([
                            { "$match" : { "_id" : board_id} },
                            { "$unwind" : "$status" },
                            { "$unwind" : "$status.cards" },
                            { "$match" : { "status.cards._id" : task_id }},
                            {"$project": {"_id":1, "status._id":1, "status.cards._id":1, "status.cards.name":1, "status.cards.due":1}}
                        ])
        result = {}
        for card in cards:
            id = card['status']['cards']['_id']
            name = card['status']['cards']['name']
            idBoard = card['status']['_id']
            idList = card['status']['_id']
            due = card['status']['cards']['due']
            result = {'id':id, 'name':name, 'idBoard':idBoard, 'idList':idList, 'due': due}
        
        return result

    def complete_item(self,board_id, task):
        self.get_db().Board.update_one(
            {'_id':board_id, 'status._id' : task['status_id']},
            {'$pull': {'status.$.cards': {'_id':task['_id']}}})

        task_to_move={'_id': task['_id'], 'name': task['name'], 'due': task['due']}

        self.get_db().Board.update_one(
            {'_id':board_id, 'status._id' : task['next_status_listId']},
            {'$push': {'status.$.cards': task_to_move}})
            



 
