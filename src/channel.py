import os
from src.data_store import data_store
from src.error import AccessError, InputError
from src.helper import get_data, seek_target_channel_and_errors, is_database_exist, save_database_updates

def channel_invite_v1(auth_user_id, channel_id, u_id):
    '''
    Invites a user with ID u_id to join a channel with ID channel_id.
    Once invited, the user is added to the channel immediately.
    In both public and private channels, all members are able to invite users.
    
    Arguments:
        auth_user_id (int)
        channel_id (int)
        u_id (int)
        
    Exceptions:
        InputError - channel_id does not refer to a valid channel
        InputError - u_id does not refer to a valid user
        InputError - u_id refers to a user who is already a member of the channel
        AccessError - channel_id is valid and the authorised user is not a member of the channel

    Return Value:
        N/A
    '''
    # Fetch data
    store = data_store.get()

    if is_database_exist():
        store = get_data()

    # Check if auth_user_id is valid
    valid = False
    for user in store['users']:
        if user['u_id'] == auth_user_id:
            valid = True
            auth_user = user # catch the authorized user
    if not valid:
        raise AccessError(description="Invalid token!")
    
    # Check if the channel_id is valid
    valid = False
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            valid = True
            target_channel = channel # Catch the channel where the new_member is gonna join
    if not valid:
        raise InputError(description="Invalid channel ID!")

    # Check if the user(u_id) is valid
    valid = False
    for user in store['users']:
        if user['u_id'] == u_id:
            valid = True
            invited_user = {
                'u_id': u_id,
                'email': user['email'],
                'name_first': user['name_first'],
                'name_last': user['name_last'],
                'handle_str': user['handle_str'],
                'permission_id': user['permission_id']
            } # Catch the invited_user without password
    if not valid:
        raise InputError(description="Invalid user ID!")

    # Check if the user is already a member of the channel
    for member in target_channel['all_members']:
        if member['u_id'] == invited_user['u_id']:
            raise InputError(description="Sorry, the invited user is already a member.")
    
    # Check if the auth user is not a member of the channel
    is_member = False
    for member in target_channel['all_members']:
        if member['u_id'] == auth_user['u_id']:
            is_member = True
    if not is_member:
        raise AccessError(description="Sorry, the authorized user is not a member of the channel.")

    # Append the new member to the target channel
    for index, channel in enumerate(store['channels']):
        if channel['channel_id'] == channel_id:
            store['channels'][index]['all_members'].append(invited_user)
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
    if is_database_exist():
        store = get_data()


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
    
    if is_database_exist():
        store = get_data()

    # Check if the channel_id is valid
    valid_channel = False
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            valid_channel = True
            target_channel = channel
    if valid_channel == False:
        raise InputError(description="Invalid channel ID!")

    # Check if authorised user is a member of the target channel
    # Search list of members in the target channel
    is_member = False
    for member in target_channel['all_members']:
        if member['u_id'] == auth_user_id:
            is_member = True
    if is_member == False:
        raise AccessError(description="Error: Authorised user is not a member")

    messages = target_channel['messages']
    total_messages = 0
    for message in messages:
        total_messages += 1

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
        for index, message in enumerate(reversed(messages[start:]), start):
            message_content = {
                    'message_id': message['message_id'],
                    'u_id': message['u_id'],
                    'message': message['message'],
                    'time_created': message['time_created'],
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


def channel_join_v1(auth_user_id, channel_id):
    """
    Add authorised users to the channel with given channel_id
    Arguments:
        auth_user_id (int) - The ID of the authorised valid user
        channel_id (int)   - The ID of the channel where the user will join in
    Exceptions:
        InputError         - Channel_id is invalid
                           - If the user is already a member of the channel
        AccessError        - Channel_id refers to a channel that is private
                             and the authorised user is not already a channel member
                             and is not a global owner
                           - Token invalid
    Return Value:
        Return an empty dictionary
    """

    # Fetch data
    store = data_store.get()

    if is_database_exist():
        store = get_data()

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
        raise AccessError(description="Invalid token!")

    # Check if the channel_id is valid
    valid = False
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            valid = True
            target_channel = channel # Catch the channel where the new_member is gonna join
    if not valid:
        raise InputError(description="Invalid channel ID!")

    # A user can't join a channel where he is alreday a member.
    for old_member in target_channel['all_members']:
        if old_member['u_id'] == new_member['u_id']:
            raise InputError(description="Sorry, you can't join the same channel agian.")

    # If the channel is private and the useer is not a member nor a global owner.
    if not target_channel['is_public'] and new_member['permission_id'] != 1:
        raise AccessError(description="Sorry, you can't join the private channel.")

    # Append the new member to the target channel
    for index, channel in enumerate(store['channels']):
        if channel['channel_id'] == channel_id:
            store['channels'][index]['all_members'].append(new_member)
    data_store.set(store)
    return {
    }

def channel_leave_v1(auth_user_id, channel_id):
    """ 
    users with auth_user_id leave the channel with given channel_id
    Arguments:
        auth_user_id (int) - The ID of the authorised valid user
        channel_id (int)   - The ID of the channel where the user will leave
    Exceptions:
        InputError         - channel_id does not refer to a valid channel
                           - auth_user invalid
        AccessError        - channel_id is valid and the authorised user
                             is not a member of the channel
    Return Value:
        Returns {} (dict) on success
    """
        # Fetch data
    store = data_store.get()
    if is_database_exist():
        store = get_data()

    # Check if the auth_user_id is valid
    valid = False
    for user in store['users']:
        if user['u_id'] == auth_user_id:
            target_user = {
                'u_id': auth_user_id,
                'email': user['email'],
                'name_first': user['name_first'],
                'name_last': user['name_last'],
                'handle_str': user['handle_str'],
                'permission_id': user['permission_id']
            } # Catch the new_member without password
            valid = True
    if not valid:
        raise AccessError(description="Invalid token!")

    # Check if the channel_id is valid
    valid = False
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            valid = True
            target_channel = channel
    if not valid:
        raise InputError(description="Invalid channel ID!")

    # A user can't leave a channel where he is not a member.
    is_member = False
    for member in target_channel['all_members']:
        if member['u_id'] == auth_user_id:
            is_member = True
    if not is_member:
        raise AccessError(description="This user is not a member of the channel!")

    # Check if the user is an owner
    is_owner = False
    for owner in target_channel['owner_members']:
        if owner['u_id'] == auth_user_id:
            is_owner = True
    
    for index, channel in enumerate(store['channels']):
        if channel['channel_id'] == channel_id:
            # Remove the user from owner list
            if is_owner:
                store['channels'][index]['owner_members'].remove(target_user)
            # Remove the user from member list
            store['channels'][index]['all_members'].remove(target_user)
    data_store.set(store)
    return {}

def channel_addowner_v1(auth_user_id, channel_id, u_id):
    """ 
    Make user with user id u_id an owner of the channel.
    Arguments:
        auth_user_id (int) - The ID of the authorised valid user
        channel_id (int)   - The ID of the channel where the user will join in
        u_id (int):        - The ID of the users
    Exceptions:
        InputError         - channel_id does not refer to a valid channel
                           - u_id does not refer to a valid user
                           - u_id refers to a user who is not a member of the channel
                           - u_id refers to a user who is already an owner of the channel
        AccessError        - channel_id is valid and the authorised user 
                             does not have owner permissions in the channel
                           - when token is invalid
    Return Value:
        Returns {} (dict) on success
    """    
    
    # Fetch data
    store = data_store.get()

    if is_database_exist():
        store = get_data()

    # Check if the auth_user_id is valid
    valid = False
    for user in store['users']:
        if user['u_id'] == auth_user_id:
            valid = True
    if not valid:
        raise AccessError(description="Invalid token!")

    # Check if the channel_id is valid
    valid = False
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            target_channel = channel
            valid = True
    if not valid:
        raise InputError(description="Invalid channel ID!")

    # Check if the u_id are valid
    valid = False
    for user in store['users']:
        if user['u_id'] == u_id:
            valid = True
            user_info = {
                'u_id': user['u_id'],
                'email': user['email'],
                'name_first': user['name_first'],
                'name_last': user['name_last'],
                'handle_str': user['handle_str'],
                'permission_id': user['permission_id']
            }
    if not valid:
        raise InputError(description="Invalid user ID!")

    # Check if the auth_user_id is in the all_members list
    auth_is_member = False
    for member in target_channel['all_members']:
        if member['u_id'] == auth_user_id:
            auth_is_member = True

    if not auth_is_member:
        raise AccessError(description="The authorized user is not a member of the channel!") 

    # Check if the user is not a member of the channel
    is_member = False
    for member in target_channel['all_members']:
        if member['u_id'] == u_id:
            is_member = True
    if not is_member:
        raise InputError(description="This user is not a member of the channel!")
    
    # Check if the user is already a owner of the channel
    for owner in target_channel['owner_members']:
        if owner['u_id'] == u_id:
            raise InputError(description="This user is already a owner of the channel!")
    
    # Check when the authorised user does not have owner permissions in the channel
    for user in store['users']:
        if user['u_id'] == auth_user_id:
            auth_user = user

    has_global_permission = False
    has_owner_permission = False
    if auth_user['permission_id'] == 1:
        has_global_permission = True
    else:
        for owner in target_channel['owner_members']:
            if owner['u_id'] == auth_user_id:
                has_owner_permission = True

    if not has_global_permission and not has_owner_permission:
            raise AccessError(description="The authorised user does not have owner permissions in the valid channel!")
    
    # Append the user to the owner list
    for index, channel in enumerate(store['channels']):
        if channel['channel_id'] == channel_id:
            store['channels'][index]['owner_members'].append(user_info)
    data_store.set(store)

    return {}

def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    """ 
    Make user with user id u_id an owner of the channel.
    Arguments:
        auth_user_id (int) - The ID of the authorised valid user
        channel_id (int)   - The ID of the channel where the user will join in
        u_id (int):        - The ID of the users
    Exceptions:
        InputError         - channel_id does not refer to a valid channel
                           - u_id does not refer to a valid user
                           - u_id refers to a user who is not an owner of the channel
                           - u_id refers to a user who is currently the only owner of the channel
        AccessError        - channel_id is valid and the authorised user 
                             does not have owner permissions in the channel
    Return Value:
        Returns {} (dict) on success
    """
    # Fetch data
    store = data_store.get()

    if is_database_exist():
        store = get_data()

    # Check if the channel_id is valid
    valid = False
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            target_channel = channel
            valid = True
    if not valid:
        raise InputError(description="Invalid channel ID!")

    # Check if the u_id are valid
    valid = False
    for user in store['users']:
        if user['u_id'] == u_id:
            valid = True
            user_info = {
                'u_id': user['u_id'],
                'email': user['email'],
                'name_first': user['name_first'],
                'name_last': user['name_last'],
                'handle_str': user['handle_str'],
                'permission_id': user['permission_id']
            }
    if not valid:
        raise InputError(description="Invalid user ID!")
    
    # Check if the user is not an owner of the channel
    is_owner = False
    num_owner = 0
    for owner in target_channel['owner_members']:
        num_owner += 1
        if owner['u_id'] == u_id:
            is_owner = True
    if not is_owner:
        raise InputError(description="This user is not an owner of the channel!")
    if num_owner == 1:
        raise InputError(description="You can't remove the owner of the channel!")

    # Check if the authorised user has owner permissions in the channel
    for user in store['users']:
        if user['u_id'] == auth_user_id:
            auth_user = user

    has_global_permission = False
    has_owner_permission = False
    if auth_user['permission_id'] == 1:
        has_global_permission = True
    else:
        for owner in target_channel['owner_members']:
            if owner['u_id'] == auth_user_id:
                has_owner_permission = True

    if not has_global_permission and not has_owner_permission:
        raise AccessError(description="The authorised user does not have owner permissions in the valid channel!")

    # Remove the user from the owner list
    for index, channel in enumerate(store['channels']):
        if channel['channel_id'] == channel_id:
            store['channels'][index]['owner_members'].remove(user_info)
    data_store.set(store)

    return {}
