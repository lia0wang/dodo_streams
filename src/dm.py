from src.error import AccessError, InputError
from src.helper import check_valid_token, decode_jwt, store_log_notif, datetime_to_unix_time_stamp
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
 
    store = data_store.get()

    # Check if the auth_user_id is valid
    valid = False
    for user in store['users']:
        if user['u_id'] == auth_user_id:
            auth_user = user
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

    # Get the current time stamp
    time_stamp = datetime_to_unix_time_stamp()

    # Generate dm_name based on the list of dm members
    member_ids = [auth_user_id] + u_ids
    dm_name = []
    for member_id in member_ids:
        for user in store['users']:
            if user['u_id'] == member_id:
                dm_name.append(user['handle_str'])
                # Update the user stats       
                num = user['dms_joined']
                new_dict = {'num_dms_joined':num+1,'time_stamp':time_stamp}
                user['user_stats']['dms_joined'].append(new_dict)
                user['dms_joined'] += 1 

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

    # Append the created dm to dms database
    store['dms'].append(dm)

    # Update the workspace stats     
    num_dms = len(store['dms'])
    new_ws_dict = {'num_dms_exist':num_dms,'time_stamp':time_stamp}
    store['workspace_stats']['dms_exist'].append(new_ws_dict)

    data_store.set(store)

    for u_id in u_ids:
        store_log_notif(u_id, -1, dm_id, auth_user,\
        dm_name, 'dm_create')   

    return {
        'dm_id': dm_id,
    }

def dm_details_v1(auth_user_id, dm_id):
    # Fetch data

    store = data_store.get()
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
        raise InputError(description="Error: Invalid dm id")
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

def dm_messages_v1(auth_user_id, dm_id, start):
    """
    Checks validty of authorised users and see if they are a member of
    a valid dm_id. Then returns 'end' which is the 'start + 50th message',
    the return data behaviour is pagination.
    Arguments:
        auth_user_id (int) - The ID of the authorised valid user
        dm_id (int)   - The ID of the dm where the user will join in
        start (int) - the starting index of messages which the user specifies 
    Exceptions:
        InputError  - dm_id is invalid
        InputError - start is greater than the total number of messages in the 
                    dm
        AccessError - dm_id is valid and the authorised user is not a 
                        member of the channe;
    Return Value:
        Returns start on condition that start <= total messages
        Returns end 
        Returns messages 
    """
        

    store = data_store.get()

    # Check if the dm_id is valid
    valid_dm = False
    for dm in store['dms']:
        if dm['dm_id'] == dm_id:
            valid_dm = True
            target_dm = dm
    if valid_dm == False:
        raise InputError(description="Invalid dm ID!")

    # Check if authorised user is a member of the target dm
    # Search list of members in the target dm
    is_member = False
    for u_id in target_dm['u_ids']:
        if u_id == auth_user_id:
            is_member = True
    if is_member == False:
        raise AccessError(description="Error: Authorised user is not a member")

    messages = target_dm['messages']
    total_messages = 0
    for message in messages:
        total_messages += 1

    messages.reverse()
    if start > total_messages:
        raise InputError(description="Error: Start must be lower than total_messages")
    if total_messages == 0:
        end = -1
        return {
            'messages': [],
            'start': start,
            'end': end,
        }
    else:
        segment_messages = []
        #index = start
        #for message in reversed(messages):
        # [start:] is slicing where i am limiting it from start to the end
        for index, message in enumerate(messages[start:], start):
            for react in message['reacts']:
                if auth_user_id in react['u_ids']:
                    react['is_this_user_reacted'] = True
            
            message_content = {
                    'message_id': message['message_id'],
                    'u_id': message['u_id'],
                    'message': message['message'],
                    'time_created': message['time_created'],
                    'dm_id': dm_id,
                    'is_pinned': message['is_pinned'],
                    'reacts': message['reacts'],
            } 
            index+=1
            segment_messages.append(message_content)
            if (index < start + 50) and (index != total_messages):                  
                end = index + 1
            elif index == total_messages:
                end = -1
            else:
                break

    return {
        'messages': segment_messages,
        'start': start,
        'end': end,
    }


def dm_list_v1(token):
    '''
    Returns a dictionary containing a list of dms the user is a member of
    
    Arguments:
        token - an encrypted value containing u_id and session_id of a user

    Exceptions:
        AccessError - token is invalid
        
    Return Value:
        Dictionary of list of dms (dm_id, dm_name)
    '''
    # Checking and decoding token
    check_valid_token(token)
    decoded_jwt = decode_jwt(token)
    u_id = decoded_jwt['u_id']
    
    # Getting dm data and making dms list
    store = data_store.get()
    dms = []
    
    # Traversing through dms, appending those that
    # have u_id as a member
    for dm in store['dms']:
        if u_id in dm['u_ids']:
            new_dm = {
                "dm_id": dm["dm_id"],
                "name": dm["dm_name"]
            }
            dms.append(new_dm)
    return {"dms": dms}

def dm_remove_v1(token, dm_id):
    '''
    Remove an existing DM, so all members are no longer in the DM.
    This can only be done by the original creator of the DM.
    Arguments:
        token - Used to identify the user
        dm_id - Used to identify the dm that has been sent 
    Exceptions:
        InputError - dm_id does not refer to a valid DM
        AccessError - dm_id is valid and the authorised user is not the original DM creator
    Return Value:
        N/A
    
    '''
    valid_dm = False
    auth_request = False
    db_store = data_store.get()
    auth_user_id = decode_jwt(token)['u_id']
    
    for dm in db_store['dms']:
        if dm['dm_id'] == dm_id:
            valid_dm = True
            #print('dm_creator',dm['auth_user_id'])
            #print('auth_user_id', auth_user_id)
            if dm['auth_user_id'] == auth_user_id:
                auth_request = True
    if valid_dm == False:
         raise InputError("Error: dm_id does not refer to a valid DM")
    if valid_dm == True and auth_request == False:
         raise AccessError("Error: dm_id is valid and the authorised user is not \
                           the original DM creator")
        
    for dm in db_store['dms']:
        if dm['dm_id'] == dm_id:
            db_store['dms'].remove(dm)
            
    # Get the current time stamp
    time_stamp = datetime_to_unix_time_stamp()
     
    for user in db_store['users']:
        if user['u_id'] == auth_user_id:
            num = user['dms_joined']
            new_dict = {'num_dms_joined':num-1,'time_stamp':time_stamp}
            user['user_stats']['dms_joined'].append(new_dict)
            user['dms_joined'] -= 1   

    data_store.set(db_store)
