import threading
from datetime import datetime, timezone, timedelta
from src.helper import get_data, save_database_updates
from src.error import AccessError, InputError
        
def standup_start_v1(auth_user_id, channel_id, length):
    '''
    Start a standup in the current channel for X sec.
    Arguments:
        auth_user_id (int)  - The ID of the valid user.
        channel_id (int)    - The id of the channel.
        length (int)        - The length of the time that the standup last
    Exceptions:
        InputError          - channel_id invalid
                            - negative length
                            - an active standup is currently running in the channel
        AccessError         - when channel_id is valid but the auth_user is not a member
    Return Value:
        {
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

    # Check if the length is negative
    if length < 0:
        raise InputError(description="The give length should not be negative!")

    # Check if the auth user is not a member of the channel
    auth_is_member = False
    for member in target_channel['all_members']:
        if member['u_id'] == auth_user_id:
            auth_is_member = True
    if not auth_is_member:
            raise AccessError(description="The authorized user is not a member of the channel.")
    
    # Check if the standup is currently running in the channel
    if target_channel['standup']['is_active']:
        raise InputError(description="An active standup is currently running in the channel!")

    # Turn on the standup and set the X-sec that it finished.
    target_channel['standup']['is_active'] = True
   
    add_utc_now = datetime.now(timezone.utc) + timedelta(seconds=length)
    time_finish = int(add_utc_now.timestamp())
    target_channel['standup']['time_finish'] = time_finish
    
    # Send all msgs from the buffer after X-sec
    timer = threading.Timer(int(length), buffer_msg_send, [auth_user_id, target_channel['channel_id']])
    timer.start()

    save_database_updates(store)
    
    return {
        'time_finish': target_channel['standup']['time_finish']
    }

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
    if target_channel['standup']['is_active'] == False:
        raise InputError(description="The active standup is not currently running in the channel.")
    
    msg = (auth_user['handle_str'], message)
    target_channel['standup']['buffer'].append(msg)
    save_database_updates(store)

    return {}

def buffer_msg_send(target_user_id, channel_id):
    '''
    Excute sending messages to the channel from the standup
    '''
    store = get_data()

    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            target_channel = channel

    len_msg = len(target_channel['standup']['buffer'])

    # Check if there is any msgs to send
    if len_msg != 0:
        # from the buffer, get the msgs
        msgs = ''
        # channel['standup']['buffer'] = (auth_user['handle_str'], message)
        for (handle_str, msg) in target_channel['standup']['buffer']:
            a_msg = handle_str + ': ' + msg
            msgs = msgs + a_msg + '\n'
        
        # remove the '\n' of the last msg
        msgs = msgs[:-1]
    
        # get the msg_id
        message_id = store['message_index']
        store['message_index'] += 1

        msg = {
            'message_id': message_id,
            'u_id': target_user_id,
            'message': msgs,
            'channel_id': target_channel['channel_id'],
            'time_created': target_channel['standup']['time_finish'],
            'is_pinned': False,
            'reacts': [
                {
                    'react_id': 1,
                    'u_ids': [],
                    'is_this_user_reacted': False
                }
            ],
        }
        target_channel['messages'].append(msg)
 
        # clear the standup
        target_channel['standup']['is_active'] = False
        target_channel['standup']['time_finish'] = None
        target_channel['standup']['buffer'] = []

    save_database_updates(store)
