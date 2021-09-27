from src.data_store import data_store
from src.error import AccessError, InputError

def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

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
            valid = True
    if valid == False:
        raise AccessError("Invalid user ID!")
    
    # Check if the channel_id is valid
    valid = False
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            valid = True
    if valid == False:
        raise InputError("Invalid channel ID!")

    # Check when the user is not a member nor an owner and the channel is private
    

    return {
    }
