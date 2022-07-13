from src.helper import get_data
from src.helper import save_database_updates

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
    store = get_data()
       
    # Create list and add users to the list
    users = []
    for user in store['users']:
        if len(user['email']) != 0:
            new_user = user
            del new_user['password']
            del new_user['session_list']
            users.append(new_user)
    return {"users": users}

def users_stats_v1(token):
    '''
    Fetches the required statistics about the use of UNSW Streams.
    Fetches the required statistics about this user's use of UNSW Streams.
    Arguments:
        token - Used to identify the user
    Return Value:
        Return workspace_stats dictionary    
    '''
    db_store = get_data()

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

    db_store['workspace_stats']['utilization_rate'] = utilization_rate
    workspace_stats = db_store['workspace_stats']
    save_database_updates(db_store) 
     
    print(workspace_stats)

    return workspace_stats  
