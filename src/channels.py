from src.data_store import data_store
from src.error import AccessError, InputError

def channels_list_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_listall_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

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
    store = data_store.get()
    
    # Check if the auth_user_id is valid
    valid = False
    for user in store['users']:
        if user['u_id'] == auth_user_id:
            valid = True
    if valid == False:
        raise AccessError("Invalid user ID!")

    # Raise an InputError when the channel's name is less than 1 char or greater than 20 char 
    if len(name) < 1 or len(name) > 20:
        raise InputError('The name length is not between 1 and 20 characters.')

    # Generate the channel_id
    new_channel_id = len(store['channels']) + 1
    
    # Get the auth_user info
    # The user who created it becomes one of the members.
    # the initail channel owner (who created the channel).
    def get_user_info(id):
        '''
        The function is to get user's info and return them as a dict
        '''
        for user in store['users']:
            if user['u_id'] == id:
                return {
                    'u_id': id,
                    'email': user['email'],
                    'password': user['password'],
                    'name_first': user['name_first'],
                    'name_last': user['name_last'],
                    'handle_str': user['handle_str']
                }
        return {}
    member_dict = get_user_info(auth_user_id)
    owner_dict = get_user_info(auth_user_id)

    # Creates a new channel with:
    channel = {
        'channel_id': new_channel_id,
        'name': name, # the given name
        'is_public': is_public, # is either a public or private channel. 
        'owner_members': [owner_dict],
        'all_members': [member_dict] # Since members are many, it supposed to be a dict type.
    }

    # Append the created channel to channels database
    store['channels'].append(channel)
    data_store.set(store)

    return {
        'channel_id': new_channel_id,
    }
