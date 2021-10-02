from src.data_store import data_store
from src.error import AccessError, InputError

def channel_invite_v1(auth_user_id, channel_id, u_id):
    store = data_store.get()
    valid_user1 = False
    valid_user2 = False
    valid_channel = False
    isMember = False
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
            } 
    # auth_user_id is invalid         
    if valid_user1 == False:
        raise AccessError("Authorised u_id does not refer to a valid user")
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
                    isMember = True # Check if authorised user is a member of the channel
                    break
            for user in chan["all_members"]:
                if user['u_id'] == new_member['u_id']: # Duplicated user
                    raise InputError("The user is already a member of the channel")
                
    if valid_channel == False:
        raise InputError("channel_id does not refer to a valid channel")
   
    if isMember == False:
        raise AccessError("Authorised user is not a member of the channel")
   
    # Add user to the channel after checking all conditions
    target_channel['all_members'].append(new_member)
    data_store.set(store)
    return {
    }
    
def channel_details_v1(auth_user_id, channel_id):
    # Fetch data
    store = data_store.get()

    # Check if auth_user_id refers to existing user
    valid_user = False
    for user in store['users']:
        if user['u_id'] == auth_user_id:
            valid_user = True
    if valid_user == False:
        raise AccessError("Error: Invalid user id")
    
    # Check if channel_id refers to valid channel
    # Find and save target channel if it exists
    valid_channel = False
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            target_channel = channel
            valid_channel = True
    if valid_channel == False:
        raise InputError("Error: Invalid channel id")

    # Check if authorised user is a member of the target channel
    # Search list of members in the target channel
    is_member = False
    for member in target_channel['all_members']:
        if member['u_id'] == auth_user_id:
            is_member = True
    if is_member == False:
        raise AccessError("Error: Authorised user is not a member")

    # Return details
    return {
        'name': target_channel['name'],
        'is_public': target_channel['is_public'],
        'owner_members': target_channel['owner_members'],
        'all_members': target_channel['all_members']
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
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
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
            raise AccessError("Sorry, you can't join the same channel agian.")

    # If the channel is private and the useer is not a member nor a global owner.
    if not target_channel['is_public'] and new_member['permission_id'] != 1:
        raise AccessError("Sorry, you can't join the private channel.")

    # Append the new member to the target channel
    target_channel['all_members'].append(new_member)
    data_store.set(store)

    return {
    }