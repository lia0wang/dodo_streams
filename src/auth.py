from src.data_store import data_store
from src.error import InputError

import re

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def auth_login_v1(email, password):
    return {
        'auth_user_id': 1,
    }

def auth_register_v1(email, password, name_first, name_last):

    # Check for input errors
    if not re.fullmatch(regex, email):
        raise InputError("Error: Invalid email")
    elif len(password) < 6:
        raise InputError("Error: Invalid password")
    elif len(name_first) < 1 or len(name_first) > 50:
        raise InputError("Error: Invalid first name ")
    elif len(name_last) < 1 or len(name_last) > 50:
        raise InputError("Error: Invalid first name ")

    # Fetch data
    store = data_store.get()

    # Check for repeated email
        # Put all emails in list
        # Append 'input email' to emails list
        # Check for duplicates in list of emails
    emails = []
    for user in store['users']:
        emails.append(user['email'])

    emails.append(email)
    if len(emails) != len(set(emails)):
        raise InputError("Error: email taken")

    # Generate handle
        # If handle is longer than 20 chars, cut off at 20 chars
        # Loop through users looking for repeated handles
        # Increment a repetition counter which will be added to repeated handle
    handle_str = name_first.lower() + name_last.lower()

    if len(handle_str) > 20:
        handle_str = handle_str[0:20]

    handle_rep_num = -1

    for user in store['users']:
        if user['handle_str'][0:len(handle_str)] == handle_str:
            handle_rep_num += 1
    if handle_rep_num != -1:
        handle_str = handle_str + str(handle_rep_num)

    # Generate user id
    id = len(store['users']) + 1

    # Create and store account
    user = {
        'u_id': id,
        'email': email,
        'password': password,
        'name_first': name_first,
        'name_last': name_last,
        'handle_str': handle_str
    }
    store['users'].append(user)
    data_store.set(store)

    return {
        'auth_user_id': id,
    }
