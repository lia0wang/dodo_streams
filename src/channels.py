from src.data_store import data_store
from src.error import InputError

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

    # Fetch data
    store = data_store.get()
    
    # Raise an InputError when the channel's name
    # is less than 1 char or greater than 20 char 
    if len(name) < 1 or len(name) > 20:
        raise InputError('The name length is not between 1 and 20 characters.')

    # Generate the channel_id
    new_channel_id = len(store['channels']) + 1

    # The user who created it automatically joins the channel. 
    # the only channel owner is the user who created the channel.
    # Creates a new channel with the given name that is either a public or private channel. 
    channel = {
        'channel_id': new_channel_id,
        'owner': auth_user_id,
        'name': name,
        'is_public': is_public
    }
    
    store['channels'].append(channel)
    data_store.set(store)

    return {
        'channel_id': new_channel_id,
    }
