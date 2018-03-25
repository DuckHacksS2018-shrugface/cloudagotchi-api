import time

import connexion
from pymongo import MongoClient

client = MongoClient("mongodb+srv://admin:shrugface@petuserdata-vckb7.mongodb.net/test")
db = client.data

def get_data(petID):
    result = db.pet.find_one({'petID': petID})
    if result == None:
        return {'result': 'Pet not found'}, 404
    rDict = {}
    for key, val in result.items():
        rDict[key] = val
    rDict.pop('_id')
    return rDict, 200

def make_new(petID):
    args = connexion.request.args
    username = args.get('username')
    petname = args.get('petname')
    if db.pet.find_one({'petID': petID}) != None:
        return {'result': 'Pet with ID already exists'}, 409
    if db.user.find_one({'user': username}) == None:
        return {'result': 'That user does not exist'}, 400
    new_pet = {
        'petID': petID,
        'name': petname,
        'ownername': username,
        'hunger': 5,
        'happiness': 5,
        'discipline': 5,
        'cleanliness': 5,
        'sick': False,
        'age': 0,
        'weight': 5,
        'poo': 5,
        'last_interaction': time.time(),
        'last_meal': time.time(),
        'last_poo': None,
        'sleep_time': 0,
        'meals_used': 0
    }
    db.pet.insert_one(new_pet)
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
    foodData = db.food.find_one({'foodID': foodID})
    if foodData == None:
        return {'result': 'No such food'}, 404
    fillingLevel = foodData['filling']
    meal = foodData['meal']
    if meal:
        if db.pet.find_one({'petID': petID})['meals_used'] < 5:
            db.pet.update_one({'petID': petID}, {'$inc': {'meals_used': 1}})
            db.pet.update_one({'petID': petID}, {'$set': {'last_meal': time.time()}})
        else:
            return {'result': 'Your pet is full'}, 400
    curFilled = db.pet.find_one({'petID': petID})['hunger']
    newFilled = curFilled + fillingLevel
    if newFilled > 5:
        newFilled = 5
    db.pet.update_one({'petID': petID}, {'$set': {'hunger': newFilled}})
    db.pet.update_one({'petID': petID}, {'$set': {'last_interaction': time.time()}})
    return {'result': 'Pet fed', 'hunger': newFilled}, 200

def play(petID, gameID):
    result = db.pet.find_one({'petID': petID})
    if result['hunger'] < 1:
        return {'result': 'Your pet is too hungry to play'}, 400
    if result['happiness'] > 3:
        db.pet.update_one({'petID': petID}, {'$set': {'happiness': 5}})
    else:
        db.pet.update_one({'petID': petID}, {'$inc': {'happiness': 2}})
    db.pet.update_one({'petID': petID}, {'$inc': {'hunger': -1}})
    db.pet.update_one({'petID': petID}, {'$set': {'last_interaction': time.time()}})
    return {'result': 'Played with pet'}, 200

def clean(petID):
    if db.pet.find_one({'petID': petID})['poo'] == 0:
        return {'result': 'No poo to clean up'}, 400
    db.pet.update_one({'petID': petID}, {'$set': {'poo': 0, 'last_poo': None, 'last_interaction': time.time()}})
    return {'result': 'Cleaned up poo'}, 200

def wash(petID):
    if db.pet.find_one({'petID': petID})['cleanliness'] == 5:
        return {'result': "Your pet's already clean"}, 400
    db.pet.update_one({'petID': petID}, {'$set': {'cleanliness': 5, 'last_interaction': time.time()}})
    return {'result': 'Washed pet'}, 200

def scold(petID):
    result = db.pet.find_one({'petID': petID})
    curDis = result['discipline']
    curHap = result['happiness']
    curDis += 1
    curHap -= 1
    if curDis > 5:
        return {'result': 'Pet is already at max discipline'}, 400
    if curHap < 0:
        return {'result': 'Your pet is too unhappy to listen to you'}, 400
    db.pet.update_one({'petID': petID}, {'$set': {'discipline': curDis, 'happiness': curHap,
                                                  'last_interaction': time.time()}})
    return {'result': 'Disciplined pet'}, 200

def heal(petID):
    if not db.pet.find_one({'petID': petID})['sick']:
        return {'result': 'Your pet is not sick'}, 400
    db.pet.update_one({'petID': petID}, {'$set': {'sick': False, 'last_interaction': time.time()}})
    return {'result': 'Healed pet'}, 200
