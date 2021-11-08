import re
import os
from src.helper import get_data, save_database_updates, decode_jwt
from src.error import InputError
from src.channels import channels_list_v1
from src.dm import dm_list_v1
import requests
import urllib.request
from PIL import Image
from src import config
import time
BASE_URL = config.url

def user_profile_v1(u_id):
    """
    For a valid user, returns information about their user_id, email, first name, 
    last name, and handle

    Arguments:
        u_id (int)       
        ...

    Exceptions:
        InputError - u_id does not refer to valid user

    Return Value:
        returns dictionary with user information with keys
        Each dictionary contains:
            u_id (int)
            email (string)
            name_first (string)
            name_last (string)
            handle_str (string)
    """
    is_valid_user = False
    db_store = get_data()
    for user in db_store['users']:
        if user['u_id'] == u_id:
            is_valid_user = True
    if is_valid_user == False:
        raise InputError(description="u_id does not refer to existing user")

    # find user in database
    for user in db_store['users']:
        if user['u_id'] == u_id:
            target_user = user
    # create dictionary to be returned
    user_return = {
        'u_id': target_user['u_id'],
        'email': target_user['email'],
        'name_first': target_user['name_first'],
        'name_last': target_user['name_last'],
        'handle_str': target_user['handle_str'], 
        'profile_img_url': target_user['profile_img_url']
    }
    return user_return

def user_profile_setname_v1(u_id, name_first, name_last):
    """
    Update the authorised user's first and last name

    Arguments:
        u_id (int)     
        name_first (string) 
        name_last (string) 
        ...

    Exceptions:
        InputError - length of name_first or name_last 
                    is not between 1 and 50 characters inclusive

    Return Value:
        empty dictionary
    """
    # fetch data
    db_store = get_data()

    # check name length errors
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError(description="Error: Invalid first name")
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError(description="Error: Invalid last name")

    # update user's names in users list
    for index, user in enumerate(db_store['users']):
        if user['u_id'] == u_id:
            db_store['users'][index]['name_first'] = name_first
            db_store['users'][index]['name_last'] = name_last
    # update user's 
    for index, chann in enumerate(db_store['channels']):
        for index2, owner_mem in enumerate(chann['owner_members']):
            if owner_mem['u_id'] == u_id:
                db_store['channels'][index]['owner_members'][index2]['name_first'] = name_first
                db_store['channels'][index]['owner_members'][index2]['name_last'] = name_last
        for index3, mem in enumerate(chann['all_members']):
            if mem['u_id'] == u_id:
                db_store['channels'][index]['all_members'][index3]['name_first'] = name_first
                db_store['channels'][index]['all_members'][index3]['name_last'] = name_last

    save_database_updates(db_store)
    return {}

def user_profile_setemail_v1(u_id, email):
    """
    Update the authorised user's email
    Arguments:
        u_id (int)   
        email (string)    
        ...

    Exceptions:
        InputError 
            - invalid email
            - email is already being used by another user

    Return Value:
        empty dictionary
    """
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    # Check for input errors
    if not re.fullmatch(regex, email):
        raise InputError(description="Error: Invalid email")

    db_store = get_data()
    for user in db_store['users']:
        if user['email'] == email:
            raise InputError(description="Error: email taken")

    for index, user in enumerate(db_store['users']):
        if user['u_id'] == u_id:
            db_store['users'][index]['email'] = email

    for index, chann in enumerate(db_store['channels']):
        for index2, owner_mem in enumerate(chann['owner_members']):
            if owner_mem['u_id'] ==u_id:
                db_store['channels'][index]['owner_members'][index2]['email'] = email
        for index3, mem in enumerate(chann['all_members']):
            if mem['u_id'] == u_id:
                db_store['channels'][index]['all_members'][index3]['email'] = email
                
    save_database_updates(db_store)
    return {}

def user_profile_sethandle_v1(u_id, handle_str):
    """
    Update the authorised user's handle/display name
    Arguments:
        u_id (int) 
        handle_str (string)      
        ...

    Exceptions:
        InputError 
            - length of handle_str is not between 3 and 20 characters inclusive
            - handle_str contains characters that are not alphanumeric
            - the handle is already used by another user

    Return Value:
        empty dictionary
    """
    if len(handle_str) < 3 or len(handle_str) > 20:
        raise InputError(description="Invalid handle")
    if not handle_str.isalnum():
        raise InputError(description="Invalid handle")
    db_store = get_data()
    for user in db_store['users']:
        if user['handle_str'] == handle_str:
            raise InputError(description="Invalid handle")

    for index, user in enumerate(db_store['users']):
        if user['u_id'] == u_id:
            db_store['users'][index]['handle_str'] = handle_str

    for index, chann in enumerate(db_store['channels']):
        for index2, owner_mem in enumerate(chann['owner_members']):
            if owner_mem['u_id'] == u_id:
                db_store['channels'][index]['owner_members'][index2]['handle_str'] = handle_str
        for index3, mem in enumerate(chann['all_members']):
            if mem['u_id'] == u_id:
                db_store['channels'][index]['all_members'][index3]['handle_str'] = handle_str
    
    save_database_updates(db_store)
    return {}

def users_all_v1():
    '''
    Returns all users
    
    Arguments:
        token - an encrypted value containing u_id and session_id of a user

    Exceptions:
        AccessError - token is invalid
    
    Return Value:
        Returns a list of user dictionaries with their associated details.
        Each dictionary contains:
            u_id (int)
            email (string)
            name_first (string)
            name_last (string)
            handle_str (string)
    '''
    # Fetching data
    store = get_data()
       
    # Create list and add users to the list
    users = []
    for user in store['users']:
        if len(user['email']) != 0:
            new_user = user
            del new_user['password']
            del new_user['session_list']
            users.append(new_user)
    return {"users": users}

def user_profile_uploadphoto_v1(u_id, img_url, x_start, y_start, x_end, y_end):

    # Check if image url is valid
    response = requests.get(img_url)
    if response.status_code != 200:
        raise InputError(description="Error: Invalid Image url")

    # Check if image url is a jpg or jpeg
    r_image = re.compile(r".*\.(jpg|jpeg)$") 
    if not r_image.match(img_url):
        raise InputError(description="Error: Image not a JPG")

    # Create image filename and path string
    imgfile_list = os.listdir("src/static/")
    img_file = "profile_img" + str(len(imgfile_list)) + ".jpg"
    img_file_path = "src/static/" + img_file

    # Download image
    urllib.request.urlretrieve(img_url, img_file_path)
    imageObject = Image.open(img_file_path)
    width, height = imageObject.size

    # Check if dimensions are valid
    if x_end not in range(width + 1) or y_end not in range(height + 1):
        raise InputError(description="Error: Image dimensions out of range")
    if x_start not in range(width + 1) or y_start not in range(height + 1):
        raise InputError(description="Error: Image dimensions out of range")
    if x_end < x_start or y_end < y_start:
        raise InputError(description="Error: end value less than start value")
    
    # Crop image
    cropped = imageObject.crop((x_start, y_start, x_end, y_end))
    cropped.save(img_file_path)

    # Save url of uploaded image
    profile_img_url = BASE_URL + "static/" + img_file
    db_store = get_data()
    for user in db_store["users"]:
        if user["u_id"] == u_id:
            user["profile_img_url"] = profile_img_url
        
    save_database_updates(db_store)
    return {}

def user_stats_v1(token):
    db_store = get_data()
    auth_user_id = decode_jwt(token)['u_id']
    channel_list = channels_list_v1(auth_user_id)
    dm_list = dm_list_v1(token)
    timestamp = datetime_to_unix_time_stamp()
    num_channels = 0
    num_channels_joined = 0
    num_dms = 0
    num_dms_joined = 0
    num_msgs = 0
    num_msgs_sent = 0
    for joined_channel in channel_list:
        num_channels_joined += 1
        for channel in db_store['channels']:
            if channel['channel_id'] == joined_channel['channel_id']:
                for message in channel['messages']:
                    if message['u_id'] == auth_user_id:
                        num_msgs_sent += 1
                        
    for joined_dm in dm_list:
        num_dms_joined += 1
        for dm in db_store['dms']:
             if dm['dm_id'] == joined_dm['dm_id']:
                 for message in dm['messages']:
                     if message['u_id'] == auth_user_id:
                         num_msgs_sent +=1
                         
    for channel in db_store['channels']:
        num_channels += 1
        for message in channel['messages']:
            num_msgs += 1
    for dm in db_store['dms']:
        num_dms += 1
        for message in dm['messages']:
            num_msgs += 1
            
    involved = num_channels_joined + num_dms_joined + num_msgs_sent
    _all = num_channels + num_dms + num_msgs
    '''
    involvement_rate = 0
    if _all == 0:
        involvement_rate = 0
    else:
        involvement_rate = involved/_all
    '''
    involvement_rate = involved/_all
    user_stats = {
        'channels_joined': {num_channels_joined,timestamp},
        'dms_joined': {num_dms_joined,timestamp},
        'messages_sent': {num_msgs_sent,timestamp},
        'involvement_rate': {involvement_rate,timestamp}
        }
    
    return user_stats
        
                 
    
