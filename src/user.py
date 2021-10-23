import re
from src.helper import get_data, save_database_updates
from src.error import InputError


def user_profile_v1(u_id):
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
        'handle_str': target_user['handle_str']
    }
    return user_return

def user_profile_setname_v1(u_id, name_first, name_last):
  
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


def users_all_v1(auth_user_id):
    # Fetching data
    store = get_data()
    
    # Checking if the auth_user_id is correct
    valid = False
    for user in store['users']:
        if user['u_id'] == auth_user_id:
            valid = True
    
    if not valid:
        raise AccessError(description="Invalid Token")
    
    # Create list and add users to the list
    users = []
    for user in store['users']:
        if 5 < len(user['password']):
            new_user = user
            del new_user['password']
            del new_user['session_list']
            users.append(new_user)
    return users