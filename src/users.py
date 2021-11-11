from src.helper import get_data


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