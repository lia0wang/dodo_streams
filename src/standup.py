from src.helper import get_data, save_database_updates
from src.error import AccessError, InputError

def standup_start_v1():
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

def standup_active_v1(auth_user_id, channel_id):
    '''
    Return whether a standuo is active in a channel.
    And the what time it finishes.
    Return None for inactive standup.
    Arguments:
        auth_user_id (int)  - The ID of the valid user.
        channel_id (int)    - The id of the channel.
    Exceptions:
        InputError          - channel_id invalid
        AccessError         - channel_id valid but the auth user is not a member of the channel
    Return Value:
        {
            is_active,
            time_finish
        }
    '''
    store = get_data()

    # Check if the channel_id is valid
    valid = False
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            target_channel = channel
            valid = True
    if not valid:
        raise InputError(description="Invalid channel ID!")

    # Check if the auth user is not a member of the channel
    auth_is_member = False
    for member in target_channel['all_members']:
        if member['u_id'] == auth_user_id:
            auth_is_member = True
    if not auth_is_member:
            raise AccessError(description="The authorized user is not a member of the channel.")

    return{
        'is_active': target_channel['standup']['is_active'],
        'time_finish': target_channel['standup']['time_finish']
    }


def standup_send_v1(auth_user_id, channel_id, message):
    '''
    Send a message to get buffered in the standup queue.
    Assume the standup is active.
    Arguments:
        auth_user_id (int)  - The ID of the valid user.
        channel_id (int)    - The id of the channel.
        message (str)       - the sent message
    Exceptions:
        InputError          - channel_id invalid
                            - length of message is over 1000 char
                            - an active standup is not currently running in the channel
        AccessError         - channel_id valid but the auth user is not a member of the channel
    Return Value:
        {}
    '''
    store = get_data()

    for user in store['users']:
        if user['u_id'] == auth_user_id:
            auth_user = user
            valid = True

    # Check if the channel_id is valid
    valid = False
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            target_channel = channel
            valid = True
    if not valid:
        raise InputError(description="Invalid channel ID!")

    # Check if the length of message is > 1000
    if len(message) > 1000:
        raise InputError(description="This message is over 1000 characters!")

    # Check if the auth user is not a member of the channel
    auth_is_member = False
    for member in target_channel['all_members']:
        if member['u_id'] == auth_user_id:
            auth_is_member = True
    if not auth_is_member:
            raise AccessError(description="The authorized user is not a member of the channel.")

    # Check if an active standup is not currently running in the channel.
    if not target_channel['standup']['is_active']:
        raise InputError(description="The active standup is not currently running in the channel.")
    
    msg = {
        'handle_str': auth_user['handle_str'],
        'message': message
    }
    
    target_channel['standup']['buffer'].append(msg)
    save_database_updates(store)
    return {}