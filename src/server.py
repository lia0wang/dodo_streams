import sys
import signal
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config
from src.auth import auth_register_v1, auth_login_v1
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
    request_data = request.get_json()

    email = request_data['email']
    password = request_data['password']
    name_first = request_data['name_first']
    name_last = request_data['name_last'] 

    register_return = auth_register_v1(email, password, name_first, name_last)
    save_data_store_updates()
    store = data_store.get()
    for user in store['users']:
        if user['u_id'] == register_return['auth_user_id']:
            handle_string = user['handle_str']
    session_id = create_session_id()
    register_return['token'] = create_jwt(handle_string, session_id)

    return dumps(register_return)

#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
