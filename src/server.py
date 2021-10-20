import sys
import signal
from json import dump, dumps
from flask import Flask, request
from flask_cors import CORS
from src.channel import channel_join_v1
from src.channels import channels_create_v1
from src.dm import dm_create_v1
from src.error import InputError
from src import config
from src.auth import auth_register_v1, auth_login_v1
from src.data_store import data_store
from src.helper import check_valid_token, get_data, save_data_store_updates, save_database_updates, create_jwt, decode_jwt, create_session_id
from src.other import clear_v1

def quit_gracefully(*args):
    '''For coverage'''
    exit(0)

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

#### NO NEED TO MODIFY ABOVE THIS POINT, EXCEPT IMPORTS

@APP.route("/clear/v1", methods=['DELETE'])
def clear():
    clear_v1()
    #open('database.json', 'w').close()
    return dumps({})

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

@APP.route("/auth/register/v2", methods=['POST'])
def register():
    # Retrieve Parameters
    request_data = request.get_json()
    email = request_data['email']
    password = request_data['password']
    name_first = request_data['name_first']
    name_last = request_data['name_last'] 

    # Register user and update database with changes to data_store
    register_return = auth_register_v1(email, password, name_first, name_last)
    save_data_store_updates()

    # Fetch data from database
    database_store = get_data()

    # Find u_id and create session_id to generate token
    session_id = create_session_id()
    for index, user in enumerate(database_store['users']):
        if user['u_id'] == register_return['auth_user_id']:
            u_id = user['u_id']
            # Update user information with sessions_list and session_id 
            database_store['users'][index]['session_list'] = [session_id]

    # Update direct changes to database
    save_database_updates(database_store)
    register_return['token'] = create_jwt(u_id, session_id)
    return dumps(register_return)

@APP.route("/auth/login/v2", methods=['POST'])
def login():
    request_data = request.get_json()
    email = request_data['email']
    password = request_data['password']
    
    auth_login = auth_login_v1(email,password)
    session_id = create_session_id()
    auth_login['token'] = create_jwt(auth_login['auth_user_id'], session_id)
    
    # Fetch data from database
    database_store = get_data()

    # Find u_id and create session_id to generate token
    for index, user in enumerate(database_store['users']):
        if user['u_id'] == auth_login['auth_user_id']:
            # Update user information with sessions_list and session_id 
            database_store['users'][index]['session_list'].append(session_id)
            save_database_updates(database_store)
    return dumps(auth_login)

@APP.route("/channels/create/v2", methods=['POST'])
def channels_create():
    # Retrieve token
    request_data = request.get_json()

    token = request_data['token']
    check_valid_token(token)
    # Decode token, retrieve parameters
    decode_token = decode_jwt(token)
    name = request_data['name']
    is_public = request_data['is_public']

    # Pass parameters
    channel = channels_create_v1(decode_token['u_id'], name, is_public)
    save_data_store_updates()

    return dumps(channel)

@APP.route("/auth/logout/v1", methods=['POST'])
def logout():
    request_data = request.get_json()
    check_valid_token(request_data['token'])
    decoded_token = decode_jwt(request_data['token'])
        
    # Fetch data from database
    db_store = get_data()
    # invalidates session id by removing it from session list 
    for index, user in enumerate(db_store['users']):
        if user['u_id'] == decoded_token['u_id']:
            session_id = decoded_token['session_id']
            db_store['users'][index]['session_list'].remove(session_id)
            save_database_updates(db_store)
    return dumps({})


@APP.route("/channel/join/v2", methods=['POST'])
def channel_join():
    # Retrieve token
    request_data = request.get_json()
    token = request_data['token']
    check_valid_token(token)

    # Decode token, retrieve parameters
    decode_token = decode_jwt(token)
    channel_id = request_data['channel_id']
    # Pass parameters
    channel_join_v1(decode_token['u_id'], channel_id)
    save_data_store_updates()
    
    return dumps({})

@APP.route("/dm/create/v1", methods=['POST'])
def dm_create():
    # Retrieve token
    request_data = request.get_json()
    token = request_data['token']
    check_valid_token(token)

    # Decode token, retrieve parameters
    decode_token = decode_jwt(token)
    u_ids = request_data['u_ids']

    # Pass parameters
    dm = dm_create_v1(decode_token['u_id'], u_ids)

    return dumps(dm)

#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
