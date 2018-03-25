import connexion
from pymongo import MongoClient

client = MongoClient("mongodb+srv://admin:shrugface@petuserdata-vckb7.mongodb.net/test")
db = client.data

def get_data(petID):
    result = db.pet.find_one({'petID': petID})
    return {'result': result['name']}, 200

def make_new(petID):
    db.pet.insert_one({'petID': petID, 'name': 'testName'})
    return {'result': 'make a pet'}, 501

def delete(petID):
    db.pet.delete_one({'petID': petID})
    return {'result': 'kill a pet'}, 501

def feed(petID, foodID):
    return {'result': 'feed pet'}, 501

def play(petID, gameID):
    return {'result': 'play with pet'}, 501

def clean(petID):
    return {'result': 'clean up poo'}, 501

def wash(petID):
    return {'result': 'wash pet'}, 501

def scold(petID):
    return {'result': 'discipline pet'}, 501

def heal(petID):
    return {'result': 'heal pet'}, 501
