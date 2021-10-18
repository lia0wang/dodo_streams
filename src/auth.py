import re
import os
from src.helper import get_data, create_handle, create_permission_id, is_database_exist
from src.data_store import data_store
from src.error import InputError

def auth_login_v1(email, password):
    """
    checks if auth_user_id is a valid u_id and password matches the respective
    u_id. 

    Arguments:
        email (string)    
        password (string)    
        ...

    Exceptions:
        InputError - Occurs when email entered does not belong to a user
        InputError - Occurs when password is not correct

    Return Value:
        Returns auth_user_id on condition that the auth_user_id is a valid u_id
        that has been registered and password is correct for that u_id.

    """


    
    store = data_store.get()
    for user in store['users']:
        if user['email'] == email:
            if user['password'] == password:
                return {
                    'auth_user_id' : user['u_id']
                }
            else:
                raise InputError('Error: Invalid password')
    raise InputError('Error: Invalid email')

def auth_register_v1(email, password, name_first, name_last):
    '''
    Using a given email, password and first and lastnames, creates a new account
    and appends account to list of users in database.

    Arguments:
        email (string) - email of the registering user
        password (string) - passsword of the registering user
        name_first (string) - first name of the registering user
        name_last (string) - last name of the registering user

    Exceptions:
        InputError - occurs when email entered is not a valid email
        InputError - occurs when email is being used by another user
        InputError - occurs when length of password is less than 6 characters
        InputError - occurs when first name is not between 1 and 50 characters (inclusive)
        InputError - occurs when last name is not between 1 and 50 characters (inclusive)

    Return Value:
        Returns auth_user_id (integer in a dictionary accessed using key 'auth_user_id')
        on the condition that the email, password first and last names are all valid
    '''

    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    # Check for input errors
    if not re.fullmatch(regex, email):
        raise InputError("Error: Invalid email")
    if len(password) < 6:
        raise InputError("Error: Invalid password")
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError("Error: Invalid first name")
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError("Error: Invalid last name")

    # Fetch data
    store = data_store.get()

    if is_database_exist() == True:
        database_store = get_data()

    # Check for repeated email
        # Put all emails in list
        # Append 'input email' to emails list
        # Check for duplicates in list of emails
    
    if is_database_exist() == True:
        emails = []
        for user in database_store['users']:
            emails.append(user['email'])
        emails.append(email)
        if len(emails) != len(set(emails)):
            raise InputError("Error: email taken")
    elif len(store['users']) != 0:
        emails = []
        for user in store['users']:
            emails.append(user['email'])

        emails.append(email)
        if len(emails) != len(set(emails)):
            raise InputError("Error: email taken")

    # Generate handle
    if is_database_exist() == True:
        handle_str = create_handle(name_first, name_last, database_store)
    else:
        handle_str = create_handle(name_first, name_last, store)
  

    # Generate permission_id
    if is_database_exist() == True:
        permission_id = create_permission_id(database_store)
    else:
        permission_id = create_permission_id(store)
 

    # Generate id
        # Check if database file exists.
        # Check if database file is empty.
        # If it exists and is not empty then, generate id according to...
        # length of users list in data base.
        # Otherwise generate id according to users in data_store.
    if is_database_exist() == True:
        user_id = len(database_store['users']) + 1
    else:
        user_id = len(store['users']) + 1

    # Create and store account
    user = {
        'u_id': user_id,
        'email': email,
        'password': password,
        'name_first': name_first,
        'name_last': name_last,
        'handle_str': handle_str,
        'permission_id': permission_id
    }
    store['users'].append(user)
    data_store.set(store)

    return {
        'auth_user_id': user_id,
    }
