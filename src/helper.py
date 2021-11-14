import jwt
import json
import os
import string
import random
import hashlib
from src.data_store import data_store
from requests.api import get
from src.error import InputError, AccessError
from datetime import date, timezone, datetime
import time
import re
SECRET = "DODO"
SESSION_ID = 0

def chan_check_tag(sender, message, target_channel):
    chan_id = target_channel['channel_id']
    dm_id = -1
    chan_name = target_channel['name']
    #notif_type = 'tagged'
    preview_msg = message[0:20]

    pattern = r'(@[a-z]{1,20}[0-9]*)|(@[a-z]{1,20})'

    result = re.findall(pattern, message) 
    # returns a list of tags without the @
    tags1 = [tup[0].replace("@","") for tup in result]

    tags = unique_list(tags1)

    for tag in tags:
        for user in target_channel['all_members']:
            # checks the tag gotten is an existing user handle string 
            if tag == user['handle_str']:
                notified_u_id = user['u_id']
                store_log_notif(notified_u_id, chan_id, dm_id, sender,\
                    chan_name, preview_msg)
                break               

    return {
    }

def dm_check_tag(sender, message, target_dm):
    chan_id = -1
    dm_id = target_dm['dm_id']
    chan_name = target_dm['dm_name']
    #notif_type = 'tagged'
    preview_msg = message[0:20]

    pattern = r'(@[a-z]{1,20}[0-9]*)|(@[a-z]{1,20})'

    result = re.findall(pattern, message) 
    # returns a list of tags without the @
    tags1 = [tup[0].replace("@","") for tup in result]

    tags = unique_list(tags1)

    store = data_store.get()
    for tag in tags:
        for user in store['users']:
            # checks the tag gotten is an existing user handle string 
            if tag == user['handle_str']:
                notified_u_id = user['u_id']
                store_log_notif(notified_u_id, chan_id, dm_id, sender,\
                    chan_name, preview_msg)
                break               

    return {
    }


def unique_list(l):
    unique_list = []
    [unique_list.append(x) for x in l if x not in unique_list]
    return unique_list


def store_log_notif(notified_u_id, channel_id, dm_id, handle_str, dmchan_name, notif_type):
    store = data_store.get()
    # create a log history for the notfication
    notif_log = {
        'u_id': notified_u_id,
        'channel_id': channel_id,
        'dm_id': dm_id,
        'handle_str': handle_str['handle_str'],
        'channel/dm_name': dmchan_name,
        'notif_type': notif_type
    }
    store['log_history'].append(notif_log)
    data_store.set(store)


def create_jwt(u_id, session_id):
    '''
    Creates token given a handle string and session_id
    Arguments: 
        - u_id: user's u_id (int)
        - session_id: user's session_id (int)
    Returns:
        - jwt encoded string
    '''
    payload = {
        "u_id": u_id,
        "session_id": session_id
    }
    return jwt.encode(payload, SECRET, algorithm = 'HS256')

def create_password_reset_jwt(u_id, reset_code):
    '''
    Creates token given a handle string and session_id
    Arguments: 
        - u_id: user's u_id (int)
        - reset_code: reset_code (str)
    Returns:
        - jwt encoded string
    '''
    payload = {
        "u_id": u_id,
        "reset_code": reset_code
    }
    return jwt.encode(payload, SECRET, algorithm = 'HS256')

def decode_jwt(encoded_jwt):
    '''
    Decode token given encoded token.
    Arguments: 
        - encoded_jwt: encoded token (string)
    Returns:
        - dictionary containing 'u_id' and 'session_id'
    '''
    return jwt.decode(encoded_jwt, SECRET, algorithms= ['HS256'])

def create_session_id():
    """
    creates a new session ID

    Returns:
        - SESSION_ID (int)
    """
    global SESSION_ID 
    SESSION_ID  += 1
    return SESSION_ID


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


def check_valid_token(token):
    db_store = data_store.get()
    try:
        decoded_jwt = decode_jwt(token)
    except Exception as error:
        raise AccessError(description="Invalid Token") from error

    u_id = decoded_jwt['u_id']
    session_id = decoded_jwt['session_id']

    for user in db_store['users']:
        if user['u_id'] == u_id:
            if session_id not in user['session_list']:
                raise AccessError(description="Invalid Token")


def hash_encrypt(password_str):
    """encrypts password string 

    Args:
        password_str (string)

    Returns:
        The hexidigest value of the encoded string
    """
    return hashlib.sha256(password_str.encode()).hexdigest()

def datetime_to_unix_time_stamp():
    timestamp = int(time.time())
    return timestamp

def create_reset_code():
    """creates password reset code
    Returns:
        Random 6 character alphanumeric string
    """
    db_store = data_store.get()
    characters = string.ascii_letters + string.digits
    reset_code = (''.join(random.choice(characters) for i in range(6))).upper()
    if len(db_store) != 0:
        for reset_token in db_store['reset_tokens']:
            decoded = decode_jwt(reset_token)
            # Ensure reset_code is not the same as any other active ones
            while decoded['reset_code'] == reset_code:
                reset_code = (''.join(random.choice(characters) for i in range(6))).upper()
    return reset_code

def search_channel_messages(u_id, channel, query_str):
    '''
    Given u_id, channel and query_str, returns list of messages with that query_str
    '''
    is_member = False
    messages = []
    for member in channel["all_members"]:
        if member["u_id"] == u_id:
            is_member = True
    if is_member:
        for message in channel["messages"]:
            if message["u_id"] == u_id and query_str.lower() in message["message"].lower():
                target_message = message
                del target_message['channel_id']
                messages.append(target_message)
    return messages

def search_dm_messages(u_id, dm, query_str):
    '''
    Given u_id, dm and query_str, returns list of messages with that query_str
    '''
    messages = []
    if u_id in dm["u_ids"]:
        for message in dm["messages"]:
            if message["u_id"] == u_id and query_str.lower() in message["message"].lower():
                target_message = message
                del target_message['dm_id']
                messages.append(target_message)
    return messages


def seek_target_dm_and_errors(data, auth_user_id, dm_id):
   # Check if auth_user_id refers to existing user
    is_valid_user = False
    for user in data['users']:
        if user['u_id'] == auth_user_id:
            is_valid_user = True
    if is_valid_user == False:
        raise AccessError("Error: Invalid user id")
    
    # Check if channel_id refers to valid channel
    # Find and save target channel if it exists
    is_valid_dm = False
    for dm in data['dms']:
        if dm['dm_id'] == dm_id:
            target_dm = dm
            is_valid_dm = True
    if is_valid_dm == False:
        raise InputError("Error: Invalid dm id")

    # Check if authorised user is a member of the target channel
    # Search list of members in the target channel
    is_member = False
    for member_id in target_dm['u_ids']:
        if member_id == auth_user_id:
            is_member = True
    if is_member == False:
        raise AccessError("Error: Authorised user is not a member")

    return target_dm