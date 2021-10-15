import jwt
import json
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
    Saves data to json file
    '''
    store = data_store.get()
    with open('database.json', 'w') as fp:
        json.dump(store, fp)

def get_data():
    '''
    Retrieves data from json database
    Returns:
        dictionary with data similar to data_store.get
    '''
    with open('database.json') as fp:
        return json.load(fp)
