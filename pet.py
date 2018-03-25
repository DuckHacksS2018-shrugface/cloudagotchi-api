import connexion
from pymongo import MongoClient

client = MongoClient("mongodb+srv://admin:shrugface@petuserdata-vckb7.mongodb.net/test")
db = client.data

def get_data(petID):
    result = db.pet.find_one({'petID': petID})
    if result == None:
        return {'result': 'Pet not found'}, 404
    return {'result': result['name']}, 200

def make_new(petID):
    args = connexion.request.args
    username = args.get('username')
    if db.pet.find_one({'petID': petID}) != None:
        return {'result': 'Pet with ID already exists'}, 409
    if db.user.find_one({'user': username}) == None:
        return {'result': 'That user does not exist'}, 400
    db.pet.insert_one({'petID': petID, 'name': 'testName', 'ownername': username})
    petslist = db.user.find_one({'user': username})['pets']
    petslist.append(petID)
    db.user.update_one({'user': username}, {'$set': {'pets': petslist}})
    return {'result': 'made a pet', 'id': petID}, 200

def delete(petID):
    args = connexion.request.args
    username = args.get('username')
    uresult = db.user.find_one({'user': username})
    if uresult == None:
        return {'result': 'That user does not exist'}, 400
    petslist = uresult['pets']
    if not petID in petslist:
        return {'result': 'That user does not own that pet'}, 404
    petslist.remove(petID)
    db.user.update_one({'user': username}, {'$set': {'pets': petslist}})
    result = db.pet.delete_one({'petID': petID})
    if result.deleted_count == 1:
        return {'result': 'Killed pet'}, 200
    return {'result': 'Could not delete pet'}, 500

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
