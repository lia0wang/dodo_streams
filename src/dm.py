from src.error import AccessError, InputError
from src.helper import get_data, save_database_updates, is_database_exist
from src.data_store import data_store

def dm_create_v1(auth_user_id, u_ids):
    ''' 
    Creates a dm contains the creator and users,
    the creator becomes the owner of the dm,
    dm name should be generated based on the users in the dm,
    name -> an alphabetically-sorted, comma-and-space-separated list of user handles,
    name -> 'ahandle1, bhandle2, chandle3'.
    Assumption:
        The creator of the dm cant be in the users list.
    Arguments:
        auth_user_id (int)  - The ID of the valid auth user.
        u_ids (dict) - The IDs of the users the DM is directed to 
    Exceptions:
        InputError - when the u_id in u_ids does not refer to a valid user
    Return Value:
        Return a dictionary containing the dm id 
    '''

    # Fetch data
    if is_database_exist():
        store = get_data()
    else:
        store = data_store.get()

    # Check if the auth_user_id is valid
    valid = False
    for user in store['users']:
        if user['u_id'] == auth_user_id:
            valid = True
    if not valid:
        raise InputError(description="Invalid authorized user ID!")

    # Check if the u_ids are valid
    for u_id in u_ids:
        valid = False
        for user in store['users']:
            if user['u_id'] == u_id:
                valid = True
        if not valid:
            raise InputError(description="Invalid user ID!")

    # The creator of the dm cant be in the users list
    for u_id in u_ids:
        if u_id == auth_user_id:
            raise AccessError(description="The authorized user cannot be in the invited users list!")

    # Generate dm_id
    dm_id = len(store['dms']) + 1

    # Generate dm_name based on the list of dm members
    member_ids = [auth_user_id] + u_ids
    dm_name = []
    for member_id in member_ids:
        for user in store['users']:
            if user['u_id'] == member_id:
                dm_name.append(user['handle_str'])
    dm_name.sort()
    dm_name = ', '.join(dm_name)
    
    # Create a new dm
    dm = {
        'dm_id': dm_id,
        'dm_name': dm_name,
        'auth_user_id': auth_user_id,
        'u_ids': member_ids,
        'messages': []
    }

    # Append the created channel to channels database
    store['dms'].append(dm)
    if is_database_exist:
        save_database_updates(store)
    else:
        data_store.set(store)
    
    return {
        'dm_id': dm_id,
        'dm_name': dm_name
    }

def dm_details_v1(auth_user_id, dm_id):
    # Fetch data
    store = data_store.get()
    if is_database_exist():
        store = get_data()
    # Check if auth_user_id refers to existing user
    is_valid_user = False
    for user in store['users']:
        if user['u_id'] == auth_user_id:
            is_valid_user = True
    if is_valid_user == False:
        raise AccessError(description="Error: Invalid user id")
    
    # Check if dm_id refers to valid dm
    # Find and save target dm if it exists
    is_valid_dm = False
    for dm in store['dms']:
        if dm['dm_id'] == dm_id:
            target_dm = dm
            is_valid_dm = True
    if is_valid_dm == False:
        raise InputError(description="Error: Invalid channel id")
    # Check if authorised user is a member of the target dm
    # Search list of members in the target dm
    is_member = False
    for u_id in target_dm['u_ids']:
        if u_id == auth_user_id:
            is_member = True
    if is_member == False:
        raise AccessError(description="Error: Authorised user is not a member")
    
    # Generate list of members 
    members = []
    for member in target_dm['u_ids']:
        for user in store['users']:
            if user['u_id'] == member:
                member_details = {
                        'u_id': user['u_id'],
                        'email': user['email'],
                        'name_first': user['name_first'],
                        'name_last': user['name_last'],
                        'handle_str': user['handle_str'],
                }
                members.append(member_details)
    # Return details
    return {
        'name': target_dm['dm_name'],
        'members': members
    }