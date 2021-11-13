import sys
import signal
import re
import requests
import urllib.request
from json import dump, dumps
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from src import message
from src.channel import channel_addowner_v1, channel_invite_v1, channel_join_v1, channel_details_v1, channel_removeowner_v1, channel_messages_v1
from src.channel import channel_leave_v1
from src.user import user_profile_v1, user_profile_setname_v1, user_profile_setemail_v1, user_stats_v1
from src.user import user_profile_sethandle_v1, user_profile_uploadphoto_v1
from src.users import users_all_v1, users_stats_v1
from src.channels import channels_create_v1
from src.dm import dm_create_v1, dm_details_v1, dm_messages_v1, dm_list_v1, dm_remove_v1
from src.message import message_send_v1, message_edit_v1, message_remove_v1, message_senddm_v1, message_send_later_v1, message_share_v1
from src.message import message_send_later_dm_v1, message_pin_v1, message_unpin_v1, message_react_v1, message_unreact_v1
from src.standup import standup_send_v1, standup_active_v1, standup_start_v1
from src.search import search_v1
from src.error import InputError, AccessError
from src import config
from src.auth import auth_passwordreset_request_v1, auth_register_v1, auth_login_v1, auth_passwordreset_reset_v1
from src.channels import channels_list_v1, channels_listall_v1
from src.admin import admin_user_remove_v1, admin_userpermission_change_v1
from src.helper import check_valid_token, create_session_id
from src.helper import  create_jwt, decode_jwt
from src.other import clear_v1
from src.notifications import notifications_v1
from src import config
from src.data_store import data_store
BASE_URL = config.url

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
    return dumps({"data": "hello"})

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
    email = request_data.get('email')
    password = request_data.get('password')
    name_first = request_data.get('name_first')
    name_last = request_data.get('name_last')

    # Register user
    register_return = auth_register_v1(email, password, name_first, name_last)
    # Fetch data from database
    database_store = data_store.get()

    # Find u_id and create session_id to generate token
    session_id = create_session_id()
    for index, user in enumerate(database_store['users']):
        if user['u_id'] == register_return['auth_user_id']:
            u_id = user['u_id']
            # Update user information with sessions_list and session_id 
            database_store['users'][index]['session_list'] = [session_id]

    # Update direct changes to database
    data_store.set(database_store)
    register_return['token'] = create_jwt(u_id, session_id)
    return dumps(register_return)

@APP.route("/auth/login/v2", methods=['POST'])
def login():
    request_data = request.get_json()
    email = request_data.get('email')
    password = request_data.get('password')
    
    auth_login = auth_login_v1(email, password)
    session_id = create_session_id()
    auth_login['token'] = create_jwt(auth_login['auth_user_id'], session_id)
    
    # Fetch data from database
    database_store = data_store.get()

    # Find u_id and create session_id to generate token
    for index, user in enumerate(database_store['users']):
        if user['u_id'] == auth_login['auth_user_id']:
            # Update user information with sessions_list and session_id 
            database_store['users'][index]['session_list'].append(session_id)
            data_store.set(database_store)
    return dumps(auth_login)

@APP.route("/channels/create/v2", methods=['POST'])
def channels_create():
    # Retrieve token
    request_data = request.get_json()

    token = request_data.get('token')
    check_valid_token(token)
    # Decode token, retrieve parameters
    decode_token = decode_jwt(token)
    name = request_data.get('name')
    is_public = request_data.get('is_public')

    # Pass parameters
    channel = channels_create_v1(decode_token['u_id'], name, is_public)

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
    check_valid_token(request_data.get('token'))
    decoded_token = decode_jwt(request_data.get('token'))
        
    # Fetch data from database
    db_store = data_store.get()
    # invalidates session id by removing it from session list 
    for index, user in enumerate(db_store['users']):
        if user['u_id'] == decoded_token['u_id']:
            session_id = decoded_token['session_id']
            db_store['users'][index]['session_list'].remove(session_id)
            data_store.set(db_store)
    return dumps({})

@APP.route("/channel/join/v2", methods=['POST'])
def channel_join():
    # Retrieve token
    request_data = request.get_json()
    token = request_data.get('token')
    check_valid_token(token)

    # Decode token, retrieve parameters
    decode_token = decode_jwt(token)
    channel_id = request_data.get('channel_id')

    # Pass parameters
    channel_join_v1(decode_token['u_id'], channel_id)
    
    return dumps({})

@APP.route("/channel/leave/v1", methods=['POST'])
def channel_leave():
    # Retrieve token
    request_data = request.get_json()
    token = request_data.get('token')
    check_valid_token(token)

    # Decode token, retrieve parameters
    decode_token = decode_jwt(token)
    channel_id = request_data.get('channel_id')

    # Pass parameters
    channel_leave_v1(decode_token['u_id'], channel_id)

    return dumps({})

@APP.route("/channel/invite/v2", methods=['POST'])
def channel_invite():
    # Retrieve token
    request_data = request.get_json()
    token = request_data.get('token')
    check_valid_token(token)

    # Decode token, retrieve parameters
    decode_token = decode_jwt(token)
    channel_id = request_data.get('channel_id')
    u_id = request_data.get('u_id')

    # Pass parameters
    channel_invite_v1(decode_token['u_id'], channel_id, u_id)
    
    return dumps({})

@APP.route("/channel/addowner/v1", methods=['POST'])
def channel_addowner():
    # Retrieve token
    request_data = request.get_json()
    token = request_data.get('token')
    check_valid_token(token)
    
    # Decode token, retrieve parameters
    decode_token = decode_jwt(token)
    channel_id = request_data.get('channel_id')
    u_id = request_data.get('u_id')

    # Pass parameters
    channel_addowner_v1(decode_token['u_id'], channel_id, u_id)
    return dumps({})

@APP.route("/channel/removeowner/v1", methods=['POST'])
def channel_removeowner():
    # Retrieve token
    request_data = request.get_json()
    token = request_data.get('token')
    check_valid_token(token)
    
    # Decode token, retrieve parameters
    decode_token = decode_jwt(token)
    channel_id = request_data.get('channel_id')
    u_id = request_data.get('u_id')

    # Pass parameters
    channel_removeowner_v1(decode_token['u_id'], channel_id, u_id)
    return dumps({})

@APP.route("/channel/details/v2", methods=['GET'])
def details():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    check_valid_token(token)
    decoded_jwt = decode_jwt(token)
    details = channel_details_v1(decoded_jwt['u_id'], channel_id)
    return dumps(details)
    
@APP.route("/dm/create/v1", methods=['POST'])
def dm_create():
    # Retrieve token
    request_data = request.get_json()
    token = request_data.get('token')
    check_valid_token(token)

    # Decode token, retrieve parameters
    decode_token = decode_jwt(token)
    u_ids = request_data.get('u_ids')

    # Pass parameters
    dm = dm_create_v1(decode_token['u_id'], u_ids)

    return dumps(dm)

@APP.route("/dm/leave/v1", methods=['POST'])
def dm_leave():

    # Retrieve token
    request_data = request.get_json()
    token = request_data.get('token')
    check_valid_token(token)

    # Decode token, retrieve parameters
    decode_token = decode_jwt(token)
    target_u_id = decode_token['u_id']
    target_dm_id = request_data.get('dm_id')

    store = data_store.get()

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

    dms = dm_list_v1(token)
    
    return dumps(dms)


@APP.route("/dm/details/v1", methods=['GET'])
def dm_details():
    # retrieve token
    token = str(request.args.get('token'))
    dm_id = int(request.args.get('dm_id'))
    check_valid_token(token)
    decoded_jwt = decode_jwt(token)
    auth_user_id = decoded_jwt['u_id']
    details = dm_details_v1(auth_user_id, dm_id)
    return dumps(details)

@APP.route("/dm/remove/v1", methods=['DELETE'])
def dm_remove():
    # Retrieve token
    request_data = request.get_json()
    token = request_data.get('token')
    check_valid_token(token)

    # Retrieve parameters
    dm_id = request_data.get('dm_id')

    # Pass parameters
    return dumps(dm_remove_v1(token, dm_id))

@APP.route("/message/send/v1", methods=['POST'])
def message_send():
    request_data = request.get_json()
    # Retrieve token
    token = request_data.get('token')
    check_valid_token(token)

    # Retrieve channel id
    channel_id = request_data.get('channel_id')
    # Retrieve message
    message = request_data.get('message')
    # Pass parameters
    new_message = message_send_v1(token,channel_id,message)
    return dumps(new_message)

@APP.route("/message/sendlater/v1", methods=['POST'])
def message_sendlater():
    request_data = request.get_json()
    # Retrieve token
    token = request_data.get('token')
    check_valid_token(token)

    # Retrieve channel id
    channel_id = request_data.get('channel_id')
    # Retrieve message
    message = request_data.get('message')
    # Retrieve time sent
    time_sent = request_data.get('time_sent')
    # Pass parameters
    new_message = message_send_later_v1(token,channel_id,message, time_sent)
    return dumps(new_message)

@APP.route("/message/edit/v1", methods=['PUT'])
def message_edit():
    request_data = request.get_json()
    # Retrieve token
    token = request_data.get('token')
    check_valid_token(token)

    # Retrieve message id
    message_id = request_data.get('message_id')
    # Retrieve message
    message = request_data.get('message')
    # Pass parameters
    message_edit_v1(token,message_id,message)
    return({})

@APP.route("/message/remove/v1", methods=['DELETE'])
def message_remove():
    request_data = request.get_json()
    # Retrieve token
    token = request_data.get('token')
    check_valid_token(token)

    # Retrieve message id
    message_id = request_data.get('message_id')

    # Pass parameters
    return dumps(message_remove_v1(token,message_id))

@APP.route("/message/senddm/v1", methods=['POST'])
def message_senddm():
    request_data = request.get_json()
    # Retrieve token
    token = request_data.get('token')
    check_valid_token(token)

    # Retrieve channel id
    dm_id = request_data.get('dm_id')
    # Retrieve message
    message = request_data.get('message')
    # Pass parameters
    new_dm = message_senddm_v1(token,dm_id,message)
    return dumps(new_dm)

@APP.route("/message/sendlaterdm/v1", methods=['POST'])
def message_sendlaterdm():
    request_data = request.get_json()
    # Retrieve token
    token = request_data.get('token')
    check_valid_token(token)

    # Retrieve channel id
    dm_id = request_data.get('dm_id')
    # Retrieve message
    message = request_data.get('message')
    # Retrieve time sent
    time_sent = request_data.get('time_sent')
    # Pass parameters
    new_message = message_send_later_dm_v1(token, dm_id, message, time_sent)
    return dumps(new_message)

@APP.route("/message/pin/v1", methods=['POST'])
def message_pin():
    # Retrieve data
    data = request.get_json()

    # Retrieving and checking token
    token = data.get('token')
    check_valid_token(token)

    # Retrieving message id
    message_id = data.get('message_id')

    message_pin_v1(token, message_id)

    return dumps({})

@APP.route("/message/unpin/v1", methods=['POST'])
def message_unpin():
    # Retrieve data
    data = request.get_json()

    # Retrieving and checking token
    token = data.get('token')
    check_valid_token(token)

    # Retrieving message id
    message_id = data.get('message_id')

    message_unpin_v1(token, message_id)

    return dumps({})

@APP.route("/message/react/v1", methods=['POST'])
def message_react():
    # Retrieve data
    data = request.get_json()
    
    # Retrieving and checking token
    token = data.get('token')
    check_valid_token(token)
    
    # Retrieving rest of info
    message_id = data.get('message_id')
    react_id = data.get('react_id')
    
    message_react_v1(token, message_id, react_id)
    
    return dumps({})

@APP.route("/message/unreact/v1", methods=['POST'])
def message_unreact():
    # Retrieve data
    data = request.get_json()
    
    # Retrieving and checking token
    token = data.get('token')
    check_valid_token(token)
    
    # Retrieving rest of info
    message_id = data.get('message_id')
    react_id = data.get('react_id')
    
    message_unreact_v1(token, message_id, react_id)
    
    return dumps({})

@APP.route("/message/share/v1", methods=['POST'])
def message_share():
    # Retrieve data
    data = request.get_json()
    
    # Retrieving and checking token
    token = data.get('token')
    check_valid_token(token)
    
    # Retrieving rest of info
    og_message_id = data.get('og_message_id')
    message = data.get('message')
    channel_id = data.get('channel_id')
    dm_id = data.get('dm_id')
    
    message_share_v1(token, og_message_id, message, channel_id, dm_id)
    
    return dumps({})

@APP.route("/dm/messages/v1", methods=['GET'])
def dm_messages_v2():

    token = str(request.args.get('token'))
    dm_id = int(request.args.get('dm_id'))
    start = int(request.args.get('start'))

    # Retrieve token
    check_valid_token(token)

    decoded_jwt = decode_jwt(token)
    auth_user_id = decoded_jwt['u_id']

    messages = dm_messages_v1(auth_user_id, dm_id, start)
    return dumps(messages)

@APP.route("/channel/messages/v2", methods=['GET'])
def channel_messages_v2():
    token = str(request.args.get('token'))
    channel_id = int(request.args.get('channel_id'))
    start = int(request.args.get('start'))

    # Retrieve token
    check_valid_token(token)

    decoded_jwt = decode_jwt(token)
    auth_user_id = decoded_jwt['u_id']

    messages = channel_messages_v1(auth_user_id, channel_id, start)
    return dumps(messages)
    
@APP.route("/user/profile/v1", methods=['GET'])
def profile():
    token = request.args.get('token')
    u_id = int(request.args.get('u_id'))
    # check if token is valid
    check_valid_token(token)
    user_return = user_profile_v1(u_id)

    return dumps({"user": user_return})

@APP.route("/user/profile/setname/v1", methods=['PUT'])
def setname():
    request_data = request.get_json()
    # check if token is valid
    check_valid_token(request_data.get('token'))
    name_first = request_data.get('name_first')
    name_last = request_data.get('name_last')
    decoded_jwt = decode_jwt(request_data.get('token'))
    user_profile_setname_v1(decoded_jwt['u_id'], name_first, name_last)

    return dumps({})

@APP.route("/user/profile/setemail/v1", methods=['PUT'])
def set_email():
    request_data = request.get_json()
    # check if token is valid
    check_valid_token(request_data.get('token'))
    email = request_data.get('email')
    decoded_jwt = decode_jwt(request_data.get('token'))
    user_profile_setemail_v1(decoded_jwt['u_id'], email)

    return dumps({})

@APP.route("/user/profile/sethandle/v1", methods=['PUT'])
def set_handle():
    request_data = request.get_json()
    # check if token is valid
    check_valid_token(request_data.get('token'))
    handle_str = request_data.get('handle_str')
    decoded_jwt = decode_jwt(request_data.get('token'))
    user_profile_sethandle_v1(decoded_jwt['u_id'], handle_str)

    return dumps({})

@APP.route("/user/profile/uploadphoto/v1", methods=['POST'])
def uploadphoto():
    request_data = request.get_json()
    check_valid_token(request_data.get('token'))
    decoded_token = decode_jwt(request_data.get('token'))
    u_id = decoded_token["u_id"]
    img_url = request_data.get("img_url")
    x_start = request_data.get("x_start")
    y_start = request_data.get("y_start")
    x_end = request_data.get("x_end")
    y_end = request_data.get("y_end")
    user_profile_uploadphoto_v1(u_id, img_url, x_start, y_start, x_end, y_end)
    return dumps({})


@APP.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('src/static', path)


@APP.route("/users/all/v1", methods=['GET'])
def list_users():
    # Retrieve token
    token = request.args.get('token')
    
    # Check if token is valid token
    check_valid_token(token)
    
    users = users_all_v1()
    return dumps(users)

@APP.route("/user/stats/v1", methods=['GET'])
def user_stats():
    token = request.args.get('token')
    check_valid_token(token)
    stats = user_stats_v1(token)
    return dumps({'user_stats': stats})

@APP.route("/users/stats/v1", methods=['GET'])
def users_stats():
    token = request.args.get('token')
    check_valid_token(token)  
    stats = users_stats_v1(token)
    return dumps({'workspace_stats': stats})

@APP.route("/admin/user/remove/v1", methods=['DELETE'])
def remove_user():
    #Retrieve data
    data = request.get_json()
    token = data.get('token')
    u_id = data.get('u_id')
    
    admin_user_remove_v1(token, u_id)
    
    return dumps({})

@APP.route("/admin/userpermission/change/v1", methods=['POST'])
def change_permission():
    # Retrieve data
    data = request.get_json()
    token = data.get('token')
    u_id = data.get('u_id')
    permission_id = data.get('permission_id')

    admin_userpermission_change_v1(token, u_id, permission_id)
    
    return dumps({})

@APP.route("/auth/passwordreset/request/v1", methods=['POST'])
def reset_request():
    # Retrieve email
    request_data = request.get_json()
    email = request_data.get('email')
    auth_passwordreset_request_v1(email)
    return dumps({})

@APP.route("/auth/passwordreset/reset/v1", methods=['POST'])
def reset():
    # Retrieve reset code and new_password
    request_data = request.get_json()
    reset_code = request_data.get('reset_code')
    new_password = request_data.get('new_password')
    auth_passwordreset_reset_v1(reset_code, new_password)
    return dumps({})

@APP.route("/notifications/get/v1", methods=['GET'])
def notifications_get():
    # Retrieve token
    token = request.args.get('token')
    
    # Check token and decode
    check_valid_token(token)
    decoded_token = decode_jwt(token)
    auth_user_id = decoded_token['u_id']

    # Pass parameters
    notifications = notifications_v1(auth_user_id)
    return dumps({"notifications": notifications})

@APP.route("/standup/send/v1", methods=['POST'])
def standup_send():
    # Retrieve token
    request_data = request.get_json()
    token = request_data.get('token')
    check_valid_token(token)

    # Decode token, retrieve parameters
    decode_token = decode_jwt(token)
    channel_id = request_data.get('channel_id')
    message = request_data.get('message')
    
    standup_send_v1(decode_token['u_id'], channel_id, message)
    return dumps({})

@APP.route("/standup/active/v1", methods=["GET"])
def standup_active():
    # Retrieve token
    request_data = request.args
    token = request_data.get('token')
    check_valid_token(token)

    decode_token = decode_jwt(token)
    channel_id = request_data.get('channel_id')

    standup_stat = standup_active_v1(int(decode_token['u_id']), int(channel_id))

    return dumps(standup_stat)

@APP.route("/standup/start/v1", methods=["POST"])
def standup_start():
    # Retrieve token
    request_data = request.get_json()
    token = request_data['token']
    check_valid_token(token)

    # Decode token, retrieve parameters
    decode_token = decode_jwt(token)
    channel_id = request_data['channel_id']
    length = request_data['length']

    standup_stat = standup_start_v1(decode_token['u_id'], channel_id, length)

    return dumps(standup_stat)

@APP.route("/search/v1", methods=['GET'])
def search():
    token = request.args.get("token")
    query_str = request.args.get("query_str")
    check_valid_token(token)
    decoded_token = decode_jwt(token)
    messages = search_v1(decoded_token["u_id"], query_str)
    return dumps({"messages": messages})

#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
