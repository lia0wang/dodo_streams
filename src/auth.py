from src.data_store import data_store
from src.error import InputError

import re

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def auth_login_v1(email, password):
    return {
        'auth_user_id': 1,
    }

def auth_register_v1(email, password, name_first, name_last):
    #
    if not re.fullmatch(regex, email):
        raise InputError("Error: Invalid email")
    elif len(password) < 6:
        raise InputError("Error: Invalid password")
    elif len(name_first) < 1 and len(name_first) > 50:
        raise InputError("Error: Invalid first name ")
    elif len(name_last) < 1 and len(name_last) > 50:
        raise InputError("Error: Invalid first name ")

    store = data_store.get()
    # Check for duplicate email only if users list is not empty
    if len(store['users']) != 0:

        # Put all emails in list
        emails = []
        for user in store['users']:
            emails.append(user['email'])

        # append input email
        emails.append(email)
        # Check for dupliates in list of emails
        if len(emails) != len(set(emails)):
            raise InputError("Error: email taken")

    # Create user id
    id = len(store['users']) + 1
    
    # If inputs have passed the checks append user dictionary
    user = {
        'user_id': id,
        'email': email,
        'password': password,
        'name_first': name_first,
        'name_last': name_last
    }
    store['users'].append(user)
    data_store.set(store)

    return {
        'auth_user_id': id,
    }
