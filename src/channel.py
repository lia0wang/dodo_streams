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
            new_member = user
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
    channel_join_v1(u_id,channel_id)


def channel_details_v1(auth_user_id, channel_id):
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'email': 'example@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'haydenjacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'email': 'example@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'haydenjacobs',
            }
        ],
    }

def channel_messages_v1(auth_user_id, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
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
            new_member = user # Catch the new_member
            valid = True
    if valid == False:
        raise AccessError("Invalid user ID!")
    
    # Check if the channel_id is valid
    valid = False
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            valid = True
            target_channel = channel # Catch the channel where the new_member is gonna join
    if valid == False:
        raise InputError("Invalid channel ID!")
    
    # A user can't join a channel where he is alreday a member.
    for old_member in target_channel['all_members']:
        if old_member['u_id'] == new_member['u_id']:
            raise AccessError("Sorry, you can't join the same channel agian.")

    # A user can't join the private channel when the use is not a member nor a global owner.
    if target_channel['is_public'] == False:
        raise AccessError("Sorry, you can't join the private channel.")

    # Append the new member to the target channel
    target_channel['all_members'].append(new_member)
    data_store.set(store)

    return {
    }
