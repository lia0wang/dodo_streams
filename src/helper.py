import jwt
import json
import os
from src.data_store import data_store
from src.error import InputError, AccessError

SECRET = "DODO"
SESSION_ID = 0

def create_jwt(handle_string, session_id):
    '''
    Creates token given a handle string and session_id
    Arguments: 
        - handle_string: user's handle string (string)
        - session_id: user's session_id (string)
    Returns:
        - jwt encoded string
    '''
    payload = {
        "handle_string": handle_string,
        "session_id": session_id
    }
    return jwt.encode(payload, SECRET, algorithm = 'HS256')

def decode_jwt(encoded_jwt):
    '''
    Decode token given encoded token.
    Arguments: 
        - encoded_jwt: encoded token (string)
        - session_id: user's session_id (string)
    Returns:
        - dictionary containing 'handle_string' and 'session_id'
    '''
    return jwt.decode(encoded_jwt, SECRET, algorithms=['HS256'])

def create_session_id():
    """
    creates a new session ID

    Returns:
        - SESSION_ID (int)
    """
    global SESSION_ID 
    SESSION_ID  += 1
    return SESSION_ID

# Only saves updates to users and channels
# Might need to be updated later
def save_data_store_updates():
    '''
    Saves updates to data_store. 
    Saves it to json file database
    '''
    store = data_store.get()
    if is_database_exist() == True:
        with open("database.json") as file:
            data = json.load(file)
        file.close()
        # Update 'already existing' users information 
        for updated_user in store['users']:
            for index, user in enumerate(data['users']):
                if user['u_id'] == updated_user['u_id'] and user != updated_user:
                    data['users'][index] = updated_user
        # Append new users
        for user in store['users']:
            if user not in data['users']:
                data['users'].append(user)

        # Update 'already existing' channels information
        for updated_chann in store['channels']:
            for index, chann in enumerate(data['channels']):
                if chann['channel_id'] == updated_chann['channel_id'] and chann != updated_chann:
                    data['channels'][index] = updated_chann
        # Append new channels
        for channel in store['channels']:
            if channel not in data['channels']:
                data['channels'].append(channel)

        with open('database.json', 'w') as file:
            json.dump(data, file)
        file.close()
    else:
        with open('database.json', 'w') as file:
            json.dump(store, file)
        file.close()


def save_database_updates(updated_database):
    '''
    Saves updates to database.
    Saves it to json database.
    Arguments:
        updated_database (dictionary)
    '''
    with open('database.json', 'w') as file:
        json.dump(updated_database, file)
    file.close()

def get_data():
    '''
    Retrieves data from json file database
    Returns:
        dictionary in a smilar manner to datastore.get
    '''
    # Check if database exists
    if os.path.isfile("database.json"):
        filesize = os.path.getsize("database.json")
        if filesize == 0:
            return {}
        with open('database.json') as file:
            data = json.load(file)
        file.close()
        return data
    else:
        return{}


def create_handle(name_first, name_last, data):

    '''
    Generate handle
    Arguments:
        name_first (string)
        name_last (string)
        data (dictionary) - database
    Return:
        handle_str (string)
    '''
    handle_str = name_first.lower() + name_last.lower()
    handle_str = ''.join(char for char in handle_str if char.isalnum())
    handle_rep_num = -1
    if len(handle_str) > 20:
        handle_str = handle_str[0:20]
    if len(data['users']) != 0:
        for user in data['users']:
            if user['handle_str'][0:len(handle_str)] == handle_str:
                handle_rep_num += 1
        if handle_rep_num != -1:
            handle_str = handle_str + str(handle_rep_num)
    return handle_str

def create_permission_id(data):
    if len(data['users']) == 0:
        permission_id = 1
    else:
        permission_id = 2
    return permission_id

def seek_target_channel_and_errors(data, auth_user_id, channel_id):
    # Check if auth_user_id refers to existing user
    is_valid_user = False
    for user in data['users']:
        if user['u_id'] == auth_user_id:
            is_valid_user = True
    if is_valid_user == False:
        raise AccessError("Error: Invalid user id")
    
    # Check if channel_id refers to valid channel
    # Find and save target channel if it exists
    is_valid_channel = False
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            target_channel = channel
            is_valid_channel = True
    if is_valid_channel == False:
        raise InputError("Error: Invalid channel id")

    # Check if authorised user is a member of the target channel
    # Search list of members in the target channel
    is_member = False
    for member in target_channel['all_members']:
        if member['u_id'] == auth_user_id:
            is_member = True
    if is_member == False:
        raise AccessError("Error: Authorised user is not a member")

    return target_channel

def is_database_exist():
    if os.path.isfile("database.json"):
        if os.path.getsize("database.json") != 0:
            return True
        else:
            return False
    else:
        return False

