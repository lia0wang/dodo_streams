from src.data_store import data_store
from src.error import AccessError, InputError
from src.helper import get_data, save_database_updates

def channels_list_v1(auth_user_id):
    ''' 
    Creates a dictionary containing a list of all the channels the user is a part of.
    
    Arguments:
        auth_user_id (int)  - The ID of the valid user.

    Exceptions:
        AccessError - Nonexistent auth_user_id entered

    Return Value:
        Return a dictionary containing the channel id and channel name of every
        channel where the user is a member.
    '''

    # Fetching data
    store = get_data()

    # Creating dictionary
    channels_list = dict()
    
    # Checking if the auth_user_id is correct
    valid = False
    for user in store['users']:
        if user['u_id'] == auth_user_id:
            valid = True
    
    if not valid:
        raise AccessError("Error: Invalid token")

    # Creating a list of channels
    channels_list['channels'] = []

    # Adding all channels the user is part of to the list
    for channel in store['channels']:
        for member in channel['all_members']:
            if member['u_id'] == auth_user_id:
                channel_dict = {
                    'channel_id': channel['channel_id'],
                    'name': channel['name']
                }
                channels_list['channels'].append(channel_dict)
    return channels_list

def channels_listall_v1(auth_user_id):
    ''' 
    Creates a dictionary containing a list of all the channels.
    
    Arguments:
        auth_user_id (int)  - The ID of the valid user.

    Exceptions:
        AccessError - Nonexistent auth_user_id entered

    Return Value:
        Return a dictionary containing the channel id and channel name of every
        channel.
    '''

    # Fetch data
    store = get_data()
    
    # Creating dictionary
    channels_list = dict()
    
    # Checking if the auth_user_id is correct
    valid = False
    for user in store['users']:
        if user['u_id'] == auth_user_id:
            valid = True
        
    if not valid:
        raise AccessError("Error: Invalid token")
    
    # Creating a list of channels
    channels_list['channels'] = []

    # Adding all channels to the dictionary
    for channel in store['channels']:
        channel_dict = {
            'channel_id': channel['channel_id'],
            'name': channel['name']
        }
        channels_list['channels'].append(channel_dict)

    return channels_list

def channels_create_v1(auth_user_id, name, is_public):
    '''
    Creates a new channel with the given name that is either a public or private channel.
    The user who created it automatically joins the channel.
    The only channel owner is the user who created the channel.
    Arguments:
        auth_user_id (int)  - The ID of the valid user.
        name (string)       - The name of the channel.
        is_public (boolean) - The state tells if the channel is private or public.
                              True for public and False for private.
    Exceptions:
        InputError - Length of name is less than 1 or more than 20 characters.
    Return Value:
        Return a dictionary containing a valid channel_id.
    '''

    # Fetch data

    store = get_data()

    # Check if the auth_user_id is valid
    valid = False
    for user in store['users']:
        if user['u_id'] == auth_user_id:
            valid = True
            user_info = {
                'u_id': auth_user_id,
                'email': user['email'],
                'name_first': user['name_first'],
                'name_last': user['name_last'],
                'handle_str': user['handle_str'],
                'permission_id': user['permission_id']
            }
    if not valid:
        raise AccessError(description="Invalid user ID!")

    # Raise an InputError when the channel's name is less than 1 char or greater than 20 char
    if len(name) < 1 or len(name) > 20:
        raise InputError(description='The name length is not between 1 and 20 characters.')

    # Generate the channel_id
    new_channel_id = len(store['channels']) + 1

    # Creates a new channel with:
    channel = {
        'channel_id': new_channel_id,
        'name': name, # the given name
        'is_public': is_public, # is either a public or private channel.
        'owner_members': [user_info],
        'all_members': [user_info], # Since members are many, it supposed to be a dict type.
        'messages': [],
        'standup': {
            'is_active': False,
            'buffer': [],
            'time_finish': None
        }
    }

    # Append the created channel to channels database
    store['channels'].append(channel)
    save_database_updates(store)

    return {
        'channel_id': new_channel_id,
    }
