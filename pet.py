import connexion

def get_data(petID):
    return {'message': 'get pet data'}, 501

def make_new(petID):
    return {'message': 'make a pet'}, 501

def delete(petID):
    return {'message': 'kill a pet'}, 501

def feed(petID, foodID):
    return {'message': 'feed pet'}, 501

def play(petID, gameID):
    return {'message': 'play with pet'}, 501

def clean(petID):
    return {'message': 'clean up poo'}, 501

def wash(petID):
    return {'message': 'wash pet'}, 501

def scold(petID):
    return {'message': 'discipline pet'}, 501

def heal(petID):
    return {'message': 'heal pet'}, 501
