import jwt
import json
import os
from src.data_store import data_store

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
        - jwt encoded string
    '''
    return jwt.decode(encoded_jwt, SECRET, algorithms=['HS256'])

def create_session_id():
    """
    creates a new session ID

    Returns:
        SESSION_ID (int)
    """
    global SESSION_ID 
    SESSION_ID  += 1
    return SESSION_ID

def save_data():
    '''
    Saves data to json file database
    '''
    store = data_store.get()
    filesize = os.path.getsize("database.json")
    # Store data_store if json file is empty
    if filesize == 0:
        with open('database.json', 'w') as file:
            json.dump(store, file)
        file.close()
    # Append new data from data_store if not empty
    else:
        with open("database.json") as file:
            data = json.load(file)
        file.close()
        for user in store['users']:
            data['users'].append(user)
        for channel in store['channels']:
            data['channels'].append(channel)
        with open('database.json', 'w') as file:
            json.dump(data, file)
        file.close()

def get_data():
    '''
    Retrieves data from json file database
    Returns:
        dictionary in a smilar manner to datastore.get
    '''
    with open('database.json') as file:
        data = json.load(file)
    file.close()
    return data


