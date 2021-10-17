import sys
import signal
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config
from src.auth import auth_register_v1, auth_login_v1
from src.channels import channels_list_v1, channels_listall_v1
from src.data_store import data_store
from src.helper import get_data, save_data_store_updates, save_database_updates, create_jwt, decode_jwt, create_session_id
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

    # Find handle string and create session_id to generate token
    session_id = create_session_id()
    for index, user in enumerate(database_store['users']):
        if user['u_id'] == register_return['auth_user_id']:
            handle_string = user['handle_str']
            # Append session_id to user's session_list
            database_store['users'][index]['session_list'] = [session_id]

    # Update direct changes to database
    save_database_updates(database_store)
    register_return['token'] = create_jwt(handle_string, session_id)
    return dumps(register_return)

@APP.route("/channels/list/v2", methods=['POST'])
def channel_list():
    # Retrieve and decode token
    data = request.get_json()
    token = data['token']
    auth_user_id = decode_jwt(token)
    channels = channels_list_v1(auth_user_id)
    return dumps(channels)

#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
