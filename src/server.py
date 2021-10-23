import sys
import signal
import re
from json import dump, dumps
from flask import Flask, request
from flask_cors import CORS
from src.channel import channel_addowner_v1, channel_invite_v1, channel_join_v1, channel_details_v1, channel_removeowner_v1, channel_messages_v1
from src.channel import channel_leave_v1
from src.user import user_profile_v1, user_profile_setname_v1, user_profile_setemail_v1
from src.user import user_profile_sethandle_v1, users_all_v1
from src.channels import channels_create_v1
from src.dm import dm_create_v1, dm_details_v1, dm_messages_v1
from src.message import message_send_v1, message_senddm_v1
from src.error import InputError, AccessError
from src import config
from src.auth import auth_register_v1, auth_login_v1
from src.channels import channels_list_v1, channels_listall_v1
from src.data_store import data_store
from src.helper import check_valid_token, get_data, save_data_store_updates, create_session_id
from src.helper import is_database_exist, save_database_updates, create_jwt, decode_jwt, hash_encrypt
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

    # Register user
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
    
    auth_login = auth_login_v1(email, password)
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

@APP.route("/channels/list/v2", methods=['GET'])
def channel_list():
    # Retrieve token
    token = request.args.get('token')
    
    # Check token and decode
    check_valid_token(token)
    decoded_token = decode_jwt(token)
    auth_user_id = decoded_token['u_id']
    
    # Pass parameters
    channels = channels_list_v1(auth_user_id)
    return dumps(channels)

@APP.route("/channels/listall/v2", methods=['GET'])
def channel_listall():
    # Retrieve token
    token = request.args.get('token')
    
    # Check token and decode
    check_valid_token(token)
    decoded_token = decode_jwt(token)
    auth_user_id = decoded_token['u_id']
    
    # Pass parameters
    channels = channels_listall_v1(auth_user_id)
    return dumps(channels)

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

@APP.route("/channel/leave/v2", methods=['POST'])
def channel_leave():
    # Retrieve token
    request_data = request.get_json()
    token = request_data['token']
    check_valid_token(token)

    # Decode token, retrieve parameters
    decode_token = decode_jwt(token)
    channel_id = request_data['channel_id']

    # Pass parameters
    channel_leave_v1(decode_token['u_id'], channel_id)
    save_data_store_updates()
    
    return dumps({})

@APP.route("/channel/invite/v2", methods=['POST'])
def channel_invite():
    # Retrieve token
    request_data = request.get_json()
    token = request_data['token']
    check_valid_token(token)

    # Decode token, retrieve parameters
    decode_token = decode_jwt(token)
    channel_id = request_data['channel_id']
    u_id = request_data['u_id']

    # Pass parameters
    channel_invite_v1(decode_token['u_id'], channel_id, u_id)
    save_data_store_updates()
    
    return dumps({})

@APP.route("/channel/addowner/v1", methods=['POST'])
def channel_addowner():
    # Retrieve token
    request_data = request.get_json()
    token = request_data['token']
    check_valid_token(token)
    
    # Decode token, retrieve parameters
    decode_token = decode_jwt(token)
    channel_id = request_data['channel_id']
    u_id = request_data['u_id']

    # Pass parameters
    channel_addowner_v1(decode_token['u_id'], channel_id, u_id)
    save_data_store_updates()
    return dumps({})

@APP.route("/channel/removeowner/v1", methods=['POST'])
def channel_removeowner():
    # Retrieve token
    request_data = request.get_json()
    token = request_data['token']
    check_valid_token(token)
    
    # Decode token, retrieve parameters
    decode_token = decode_jwt(token)
    channel_id = request_data['channel_id']
    u_id = request_data['u_id']

    # Pass parameters
    channel_removeowner_v1(decode_token['u_id'], channel_id, u_id)
    save_data_store_updates()
    return dumps({})

@APP.route("/channel/details/v2", methods=['GET'])
def details():
    request_data = request.get_json()
    check_valid_token(request_data['token'])
    decoded_jwt = decode_jwt(request_data['token'])
    details = channel_details_v1(decoded_jwt['u_id'], request_data['channel_id'])
    return dumps(details)
    
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

@APP.route("/dm/leave/v1", methods=['POST'])
def dm_leave():

    # Retrieve token
    request_data = request.get_json()
    token = request_data['token']
    check_valid_token(token)

    # Decode token, retrieve parameters
    decode_token = decode_jwt(token)
    target_u_id = decode_token['u_id']
    target_dm_id = request_data['dm_id']

    store = get_data()

    # Check if auth_user_id refers to existing user
    is_valid_user = False
    for user in store['users']:
        if user['u_id'] == target_u_id:
            is_valid_user = True
    if is_valid_user == False:
        raise AccessError(description="Error: Invalid user id")
    
    # Check if dm_id refers to valid dm
    # Find and save target dm if it exists
    is_valid_dm = False
    for dm in store['dms']:
        if dm['dm_id'] == target_dm_id:
            target_dm = dm
            is_valid_dm = True
    if is_valid_dm == False:
        raise InputError(description="Error: Invalid dm id")
    # Check if authorised user is a member of the target dm
    # Search list of members in the target dm
    is_member = False
    for u_id in target_dm['u_ids']:
        if u_id == target_u_id:
            is_member = True
    if is_member == False:
        raise AccessError(description="Error: Authorised user is not a member")

    target_dm['u_ids'].remove(target_u_id)
    
    save_database_updates(store)
    return dumps({}) 
@APP.route("/dm/list/v1", methods=['GET'])
def dm_list():
    # retrieve token
    token = request.args.get('token')
    
    # Checking and decoding token
    check_valid_token(token)
    decoded_jwt = decode_jwt(token)
    u_id = decoded_jwt['u_id']
    
    # Getting dm data and making dms list
    store = get_data()
    dms = []
    
    # Traversing through dms, appending those that
    # have u_id as a member
    for dm in store['dms']:
        if u_id in dm['u_ids']:
            new_dm = dm
            del new_dm['auth_user_id']
            del new_dm['u_ids']
            del new_dm['messages']
            dms.append(new_dm)
    return dumps(dms)


@APP.route("/dm/details/v1", methods=['GET'])
def dm_details():
    # retrieve token
    request_data = request.get_json()
    check_valid_token(request_data['token'])
    decoded_jwt = decode_jwt(request_data['token'])
    auth_user_id = decoded_jwt['u_id']
    details = dm_details_v1(auth_user_id, request_data['dm_id'])
    return dumps(details)

@APP.route("/message/send/v1", methods=['POST'])
def message_send():
    request_data = request.get_json()
    # Retrieve token
    token = request_data['token']
    check_valid_token(token)

    # Retrieve channel id
    channel_id = request_data['channel_id']
    # Retrieve message
    message = request_data['message']
    # Pass parameters
    new_message = message_send_v1(token,channel_id,message)
    return dumps(new_message)

@APP.route("/message/remove/v1", methods=['DELETE'])
def message_remove():
    return dumps({})

@APP.route("/message/senddm/v1", methods=['POST'])
def message_senddm():
    request_data = request.get_json()
    # Retrieve token
    token = request_data['token']
    check_valid_token(token)

    # Retrieve channel id
    dm_id = request_data['dm_id']
    # Retrieve message
    message = request_data['message']
    # Pass parameters
    new_dm = message_senddm_v1(token,dm_id,message)
    return dumps(new_dm)

@APP.route("/dm/messages/v1", methods=['GET'])
def dm_messages_v2():
    request_data = request.get_json()
    # Retrieve token
    token = request_data['token']
    check_valid_token(token)

    decoded_jwt = decode_jwt(request_data['token'])
    auth_user_id = decoded_jwt['u_id']

    dm_id = request_data['dm_id']
    start = request_data['start']

    messages = dm_messages_v1(auth_user_id, dm_id, start)
    return dumps(messages)

@APP.route("/channel/messages/v2", methods=['GET'])
def channel_messages_v2():
    request_data = request.get_json()
    # Retrieve token
    token = request_data['token']
    check_valid_token(token)

    decoded_jwt = decode_jwt(request_data['token'])
    auth_user_id = decoded_jwt['u_id']

    channel_id = request_data['channel_id']
    start = request_data['start']

    messages = channel_messages_v1(auth_user_id, channel_id, start)
    return dumps(messages)
    
@APP.route("/user/profile/v1", methods=['GET'])
def profile():
    request_data = request.get_json()
    # check if token is valid
    check_valid_token(request_data['token'])
    user_return = user_profile_v1(request_data['u_id'])

    return dumps(user_return)

@APP.route("/user/profile/setname/v1", methods=['PUT'])
def setname():
    request_data = request.get_json()
    # check if token is valid
    check_valid_token(request_data['token'])
    name_first = request_data['name_first']
    name_last = request_data['name_last']
    decoded_jwt = decode_jwt(request_data['token'])
    user_profile_setname_v1(decoded_jwt['u_id'], name_first, name_last)

    return dumps({})

@APP.route("/user/profile/setemail/v1", methods=['PUT'])
def set_email():
    request_data = request.get_json()
    # check if token is valid
    check_valid_token(request_data['token'])
    email = request_data['email']
    decoded_jwt = decode_jwt(request_data['token'])
    user_profile_setemail_v1(decoded_jwt['u_id'], email)

    return dumps({})

@APP.route("/user/profile/sethandle/v1", methods=['PUT'])
def set_handle():
    request_data = request.get_json()
    # check if token is valid
    check_valid_token(request_data['token'])
    handle_str = request_data['handle_str']
    decoded_jwt = decode_jwt(request_data['token'])
    user_profile_sethandle_v1(decoded_jwt['u_id'], handle_str)

    return dumps({})

@APP.route("/users/all/v1", methods=['GET'])
def list_users():
    # Retrieve token
    token = request.args.get('token')
    # token = data['token']
    
    # Check if token is valid token
    check_valid_token(token)
    decoded_token = decode_jwt(token)
    
    users = users_all_v1()
    return dumps(users)

@APP.route("/admin/user/remove/v1", methods=["DELETE"])
def remove_user():
    #Retrieve token
    data = request.get_json()
    token = data['token']
    
    # Check if token is valid
    check_valid_token(token)
    
    # Get data
    u_id = data['u_id']
    decoded_token = decode_jwt(token)
    auth_user_id = decoded_token['u_id']
    store = get_data()
    
    valid_u_id = False
    valid_auth = False
    multiple_global_owners = False
    
    # Checking for errors
    for user in store['users']:
        if user['u_id'] == u_id:
            valid_u_id = True
            
        if user['u_id'] == auth_user_id and user['permission_id'] == 1:
            valid_auth = True
        elif user['permission_id'] == 1:
            multiple_global_owners = True
    
    # Returning error messages in case of errors
    if not valid_u_id:
        raise InputError(description="u_id does not refer to a valid user")

    if not valid_auth:
        raise AccessError(description="Authorised user is not a global owner")
    
    if auth_user_id == u_id and not multiple_global_owners:
        raise InputError(description="There must be at least one global owner")

    # Remove user from user list
    for user in store['users']:
        if user['u_id'] == u_id:
            user['name_first'] = "Removed"
            user['name_last'] = "user"
            user['email'] = ""
            user['password'] = ""
            user['handle_str'] = ""
            user['permission_id'] = 2
    
    # Remove user from channels and change messages' content to "Removed user"
    for channel in store['channels']:
        user_in_channel = False
        for member in channel['owner_members']:
            if member['u_id'] == u_id:
                channel['owner_members'].remove(member)
        
        for member in channel['all_members']:
            if member['u_id'] == u_id:
                channel['all_members'].remove(member)
                user_in_channel = True
        if user_in_channel:
            for message in channel['messages']:
                if message['u_id'] == u_id:
                    message['message'] = "Removed user"
    
    # Remove user from dms and change messages' content to "Removed user"
    for dm in store['dms']:
        user_in_dm = False
        if dm['auth_user_id'] == u_id:
            dm['auth_user_id'] = ""
        
        for member in dm['u_ids']:
            if member == u_id:
                dm['u_ids'].remove(member)
                user_in_dm = True
        if user_in_dm:
            for message in dm['messages']:
                if message['u_id'] == u_id:
                    message['message'] = "Removed user"
    
    save_database_updates(store)
    
    return dumps({})

@APP.route("/admin/userpermission/change/v1", methods=['POST'])
def change_permission():
    # Retrieve token
    data = request.get_json()
    token = data['token']
    
    # Check if token is valid
    check_valid_token(token)
    
    # Get data
    u_id = data['u_id']
    permission_id = data['permission_id']
    decoded_token = decode_jwt(token)
    auth_user_id = decoded_token['u_id']
    store = get_data()
    
    valid_u_id = False
    valid_auth = False
    multiple_global_owners = False
    
    # Checking for errors
    if permission_id == 1 or permission_id == 2:
        for user in store['users']:
            if user['u_id'] == u_id:
                valid_u_id = True
            
            if user['u_id'] == auth_user_id and user['permission_id'] == 1:
                valid_auth = True
            elif user['permission_id'] == 1:
                multiple_global_owners = True
    else:
        raise InputError(description="permission_id is invalid")
    
    # Returning error messages in case of errors
    if not valid_u_id:
        raise InputError(description="u_id does not refer to a valid user")

    if not valid_auth:
        raise AccessError(description="Authorised user is not a global owner")
    
    if permission_id == 2 and auth_user_id == u_id and not multiple_global_owners:
        raise InputError(description="There must be at least one global owner")
    
    # Changing user's permissions in users list
    for user in store['users']:
        if user['u_id'] == u_id:
            user['permission_id'] = permission_id
    
    # Changing user's permissions in channel members list
    for channel in store['channels']:
        for member in channel['owner_members']:
            if member['u_id'] == u_id:
                member['permission_id'] = permission_id
        
        for member in channel['all_members']:
            if member['u_id'] == u_id:
                member['permission_id'] = permission_id

    save_database_updates(store)
    
    return dumps({})

#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
