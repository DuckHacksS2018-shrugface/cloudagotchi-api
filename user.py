import connexion
from pymongo import MongoClient

client = MongoClient("mongodb+srv://admin:shrugface@petuserdata-vckb7.mongodb.net/test")
db = client.data

def get_data(username):
    result = db.user.find_one({'user': username})
    if result != None:
        return {'result': result['pets']}, 200
    return {'result': 'User not found'}, 404

def make_new(username):
    if db.user.find_one({'user': username}) != None:
        return {'result': 'User with username already exists'}, 409
    db.user.insert_one({'user': username, 'pets': []})
    return {'result': 'Made user'}, 200

def delete(username):
    result = db.user.find_one_and_delete({'user': username})
    if result == None:
        return {'result': 'User not found'}, 404
    petslist = result['pets']
    for petid in petslist:
        db.pet.delete_one({'petID': petid})
    return {'result': 'Deleted user'}, 200
