]import os
from src.data_store import data_store
from src.error import AccessError, InputError
from src.helper import get_data, seek_target_channel_and_errors, is_database_exist

def channel_invite_v1(auth_user_id, channel_id, u_id):
    '''
    Let an authorised user with ID auth_user_id to invite a user with ID u_id to j
    oin a channel with ID channel_id. Once invited, the user is added to the channel immediately.
    In both public and private channels, all members are able to invite users.
    
    Arguments:
        auth_user_id (int)
        channel_id (int)
        u_id (int)
        
    Exceptions:
        InputError - occurs if channel_id does not refer to existing channel
        InputError - occurs if u_id does not refer to existing user
        InputError - occurs if u_id is already a member of the channel
        AccessError - occurs if auth_user_id does not refer to member of the valid channel
        
    Return Value:
        N/A
    '''
    store = data_store.get()
    valid_user1 = False
    valid_user2 = False
    valid_channel = False
    is_member = False
    new_member = {} 
    # Check if auth_user_id is valid
    for user in store['users']:
        if user['u_id'] == auth_user_id:
            valid_user1 = True
    # Check if u_id is valid
    for user in store['users']:
        if user['u_id'] == u_id:
            valid_user2 = True
            new_member = {
                'u_id': u_id,
                'email': user['email'],
                'name_first': user['name_first'],
                'name_last': user['name_last'],
                'handle_str': user['handle_str'],
                'permission_id': user['permission_id']
            } 
    # auth_user_id is invalid         
    if valid_user1 == False:
        raise InputError("Authorised u_id does not refer to a valid user")
    # u_id is valid
    if valid_user2 == False:
        raise InputError("u_id does not refer to a valid user")
    
    # Check channel_id is valid
    for chan in store['channels']:
        if chan['channel_id'] == channel_id:
            valid_channel = True
            target_channel = chan
            for user in chan["all_members"]:
                if user['u_id'] == auth_user_id:
                    is_member = True # Check if authorised user is a member of the channel
                    break
            for user in chan["all_members"]:
                if user['u_id'] == new_member['u_id']: # Duplicated user
                    raise InputError("The user is already a member of the channel")
                
    if valid_channel == False:
        raise InputError("channel_id does not refer to a valid channel")
   
    if is_member == False:
        raise AccessError("Authorised user is not a member of the channel")
   
    # Add user to the channel after checking all conditions
    target_channel['all_members'].append(new_member)
    data_store.set(store)
    return {
    }
    
def channel_details_v1(auth_user_id, channel_id):
    '''
    A channel and authorised user is given. If the authorised user is a member
    of the channel then details about the channel are provided. These details include the
    channel's name, its members, owners and 'public-or-private' status.
    
    Arguments:
        auth_user_id (int) - ID of the authorised user
        channel_id (int) - ID of the channel whose details will be provided
        
    Exceptions:
        AccessError - occurs if auth_user_id does not refer to existing user
        InputError - occurs if channel_id does not refer to existing channel
        AccessError - occurs if auth_user_id does not refer to member of the valid channel
        
    Return Value:
        Returns dictionary if auth_user_id and channel_id, together, are valid
        Dictionary includes:
            - name (string)
            - is_public (boolean)
            - owner_members (list of dictionaries)
                Each dictionary contains:
                    u_id (int)
                    email (string)
                    name_first (string)
                    name_last (string)
                    handle_str (string)
            - all_members (list of dictionaries)
                Each dictionary contains:
                    u_id (int)
                    email (string)
                    name_first (string)
                    name_last (string)
                    handle_str (string)
    '''
    # Fetch data
    store = data_store.get()

    if is_database_exist() == True:
        db_store = get_data()
        target_channel = seek_target_channel_and_errors(db_store, auth_user_id, channel_id)
    else:
        target_channel = seek_target_channel_and_errors(store, auth_user_id, channel_id)

    # Generate list of owner members and members 
    # 'permission_id' and 'password' are excluded from member details
    owner_members = []
    all_members = []

    for owner_member in target_channel['owner_members']:
        owner_member_details = {
                'u_id': owner_member['u_id'],
                'email': owner_member['email'],
                'name_first': owner_member['name_first'],
                'name_last': owner_member['name_last'],
                'handle_str': owner_member['handle_str'],
        }
        owner_members.append(owner_member_details)
    
    for member in target_channel['all_members']:
        member_details = {
                'u_id': member['u_id'],
                'email': member['email'],
                'name_first': member['name_first'],
                'name_last': member['name_last'],
                'handle_str': member['handle_str'],
        }
        all_members.append(member_details)

    # Return details
    return {
        'name': target_channel['name'],
        'is_public': target_channel['is_public'],
        'owner_members': owner_members,
        'all_members': all_members
    }

def channel_messages_v1(auth_user_id, channel_id, start):
    """
    Checks validty of authorised users and see if they are a member of
    a valid channel_id. Then returns 'end' which is the 'start + 50th message',
    the return data behaviour is pagination. Note: in first iteration,
    it will return an empty message list, and end is undeclared, this function
    is limited in iteration 1.
    Arguments:
        auth_user_id (int) - The ID of the authorised valid user
        channel_id (int)   - The ID of the channel where the user will join in
        start (int) - the starting index of messages which the user specifies 
    Exceptions:
        InputError  - Channel_id is invalid
        InputError - start is greater than the total number of messages in the 
                    channel
        AccessError - channel_id is valid and the authorised user is not a 
                        member of the channe;
    Return Value:
        Returns start on condition that start <= total messages
        Returns end 
        Returns messages 
    """
        
    store = data_store.get()
    # Check if the channel_id is valid
    valid_channel = False
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            valid_channel = True
            target_channel = channel
    if valid_channel == False:
        raise InputError("Invalid channel ID!")

    # Check if authorised user is a member of the target channel
    # Search list of members in the target channel
    is_member = False
    for member in target_channel['all_members']:
        if member['u_id'] == auth_user_id:
            is_member = True
    if is_member == False:
        raise AccessError("Error: Authorised user is not a member")

    total_messages = 0
    if start > total_messages:
        raise InputError("Error: Start must be lower than total_messages")

    return {
        'messages': [ ],
        'start': start,
        'end': -1,
    }



def channel_join_v1(auth_user_id, channel_id):
    """
    Add authorised users to the channel with given channel_id
    Arguments:
        auth_user_id (int) - The ID of the authorised valid user
        channel_id (int)   - The ID of the channel where the user will join in
    Exceptions:
        InputError  - Channel_id is invalid
                    - If the user is already a member of the channel
        AccessError - Channel_id refers to a channel that is private
                      and the authorised user is not already a channel member
                      and is not a global owner
    Return Value:
        Return an empty dictionary
    """

    # Fetch data
    store = data_store.get()

    # Check if the auth_user_id is valid
    valid = False
    for user in store['users']:
        if user['u_id'] == auth_user_id:
            new_member = {
                'u_id': auth_user_id,
                'email': user['email'],
                'name_first': user['name_first'],
                'name_last': user['name_last'],
                'handle_str': user['handle_str'],
                'permission_id': user['permission_id']
            } # Catch the new_member without password
            valid = True
    if not valid:
        raise AccessError("Invalid user ID!")

    # Check if the channel_id is valid
    valid = False
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            valid = True
            target_channel = channel # Catch the channel where the new_member is gonna join
    if not valid:
        raise InputError("Invalid channel ID!")

    # A user can't join a channel where he is alreday a member.
    for old_member in target_channel['all_members']:
        if old_member['u_id'] == new_member['u_id']:
            raise InputError("Sorry, you can't join the same channel agian.")

    # If the channel is private and the useer is not a member nor a global owner.
    if not target_channel['is_public'] and new_member['permission_id'] != 1:
        raise AccessError("Sorry, you can't join the private channel.")

    # Append the new member to the target channel
    target_channel['all_members'].append(new_member)
    data_store.set(store)

    return {
    }
