from src.helper import datetime_to_unix_time_stamp, check_valid_token
from src.data_store import data_store


def users_all_v1():
    '''
    Returns all users
    
    Arguments:
        token - an encrypted value containing u_id and session_id of a user

    Exceptions:
        AccessError - token is invalid
    
    Return Value:
        Returns a list of user dictionaries with their associated details.
        Each dictionary contains:
            u_id (int)
            email (string)
            name_first (string)
            name_last (string)
            handle_str (string)
    '''
    # Fetching data
    store = data_store.get()
       
    # Create list and add users to the list
    users = []
    for user in store['users']:
        if len(user['email']) != 0:
            new_user = {
                'u_id': user['u_id'],
                'email': user['email'],
                'name_first': user['name_first'],
                'name_last': user['name_last'],
                'handle_str': user['handle_str'], 
                'profile_img_url': user['profile_img_url']
            }
            users.append(new_user)
    return {"users": users}

def users_stats_v1(token):
    '''
    Fetches the required statistics about the use of UNSW Streams.
    '''
    db_store = data_store.get()

    num_channels_exist = len(db_store['channels'])
    num_dms_exist = len(db_store['dms'])
    num_messages_exist = db_store['message_count']

    num_users = len(db_store['users'])
    num_utilization_users = 0 #num_users_who_have_joined_at_least_one_channel_or_dm = 0
    
    utilization_rate = 0
    
    if db_store['users'] != None:
        num_users = len(db_store['users'])
        for user in db_store['users']:
            print('user: ', user)  
            if user['dms_joined']!= 0 or user['channels_joined']!=0:
                num_utilization_users +=1
                

    utilization_rate = num_utilization_users/num_users

    print('num_channels_exist: ',num_channels_exist)
    print('num_dms_exist: ',num_dms_exist)
    print('num_messages_exist: ',num_messages_exist)
    print('num_utilization_users: ',num_utilization_users)
    print('num_users: ',num_users)
    
    timestamp = datetime_to_unix_time_stamp()
    users_stats = {
        'channels_exist': [{'num_channels_exist':num_channels_exist,'timestamp':timestamp}],
        'dms_exist': [{'num_dms_exist':num_dms_exist,'timestamp':timestamp}],
        'messages_exist': [{'num_messages_exist':num_messages_exist,'timestamp':timestamp}],
        'utilization_rate': utilization_rate
        }
    print(users_stats)
    data_store.set(db_store)
    return users_stats  
