from src.helper import check_valid_token, get_data, save_database_updates
from src.helper import decode_jwt
from src.error import InputError, AccessError

def admin_user_remove_v1(token, u_id):
    '''
    Removes a user from all channels and dms,
    changing all messages sent to "Removed user",
    user is not listed in users all, but can be found
    through user profile
    
    Arguments:
        token - an encrypted value containing u_id and session_id of a global owner
        u_id  - the u_id of the user to be removed

    Exceptions:
        AccessError - token is invalid
        AccessError - token's u_id is not that of a global owner
        InputError  - u_id does not refer to a valid user
        InputError  - u_id is that of the last global owner
    
    Return Value:
        None
    '''
    
    # Check if token is valid
    check_valid_token(token)
    
    # Get data
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
    
    return {}


def admin_userpermission_change_v1(token, u_id, permission_id):
    '''
    Changes the permisisons of the given u_id to those of the given
    permission_id
    
    Arguments:
        token         - an encrypted value containing u_id and session_id of a global owner
        u_id          - the u_id of the user whose permissions will be changed
        permission_id - new permission of u_id

    Exceptions:
        AccessError - token is invalid
        AccessError - token's u_id is not that of a global owner
        InputError  - u_id does not refer to a valid user
        InputError  - last global owner is being changed to member
        InputError  - permission_id is not valid
    
    Return Value:
        None
    '''
    # Check if token is valid
    check_valid_token(token)
    
    # Get data
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

    return {}