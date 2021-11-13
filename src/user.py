import re
import os
from src.helper import  decode_jwt, \
     datetime_to_unix_time_stamp
from src.error import InputError
from src.channels import channels_list_v1
import urllib.request
from PIL import Image
from src.dm import dm_list_v1
import requests
from src import config
import time
from src.data_store import data_store
BASE_URL = "https://deplododo.alwaysdata.net/"

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
    db_store = data_store.get()
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
    db_store = data_store.get()

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

    data_store.set(db_store)
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

    db_store = data_store.get()
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
                
    data_store.set(db_store)
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
    db_store = data_store.get()
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
    
    data_store.set(db_store)
    return {}


def user_profile_uploadphoto_v1(u_id, img_url, x_start, y_start, x_end, y_end):
    '''
    Given a u_id, an http image_url, and dimensions x_start, y_start, x_end, y_end
    downloads an image, crops it and serves it/makes it accessible to the frontend
    
    Arguments:
        u_id (int) - u_id of user who is having their profile image changed
        img_url (str) - url of image being downloaded and cropped
        x_start and y_start (int) - togther define coordinates of upper left hand 
                                    corner of the cropped image
        x_end and y_end (int) - determines the height and width of the cropped image
    Exceptions:
        InputError
            - image_url does not refer to existing image
            - image_rl is not a jpg or jpeg
            - image dimensions determined by start and end are out of range
            - end values are less than or equal to start values
    
    Return Value:
        empty dictionary
    '''
    # Check if image url is valid
    response = requests.get(img_url)
    if response.status_code != 200:
        raise InputError(description="Error: Invalid Image url")

    # Check if image url is a jpg or jpeg
    r_image = re.compile(r".*\.(jpg|jpeg)$") 
    if not r_image.match(img_url):
        raise InputError(description="Error: Image not a JPG or JPEG")

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
    if x_end <= x_start or y_end <= y_start:
        raise InputError(description="Error: end value less than start value")
    
    # Crop image
    cropped = imageObject.crop((x_start, y_start, x_end, y_end))
    cropped.save(img_file_path)

    # Save served url of uploaded image
    profile_img_url = BASE_URL + "static/" + img_file
    db_store = data_store.get()
    for user in db_store["users"]:
        if user["u_id"] == u_id:
            user["profile_img_url"] = profile_img_url
        
    data_store.set(db_store)
    return {}


def user_stats_v1(token):
    '''
    '''
    db_store = data_store.get()
    
    auth_user_id = decode_jwt(token)['u_id']
    
    num_channels = len(db_store['channels'])
    num_dms = len(db_store['dms'])
    num_msgs = db_store['message_index']

    for user in db_store['users']:
        if user['u_id'] == auth_user_id:
            targer_user = user

    num_channels_joined = targer_user['channels_joined']
    num_dms_joined = targer_user['dms_joined']
    num_msgs_sent = targer_user['messages_sent']
    
    involved = num_channels_joined + num_dms_joined + num_msgs_sent
    _all = num_channels + num_dms + num_msgs

    involvement_rate = 0
    if _all == 0:
        involvement_rate = 0
    else:
        involvement_rate = involved/_all

    if involvement_rate > 1:
        involvement_rate = 1
        

    print('num_channels_joined: ',num_channels_joined)
    print('num_dms_joined: ',num_dms_joined)
    print('num_msgs_sent: ',num_msgs_sent)
    print('involved', involved)
    print('num_channels: ',num_channels)
    print('num_dms: ',num_dms)
    print('num_msgs: ',num_msgs)  
    print('_all: ', _all) 

    targer_user['user_stats']['involvement_rate'] = involvement_rate
    user_stats = targer_user['user_stats']
    data_store.set(db_store)

    return user_stats
        
                 
    # channels_joined': [{'num_channels_joined':0,'timestamp':timestamp}, 
    # {'num_channels_joined':1,'timestamp':timestamp},
    # {'num_channels_joined':2,'timestamp':timestamp},
    # {'num_channels_joined':3,'timestamp':timestamp},
    # ],
