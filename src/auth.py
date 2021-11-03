import re
import os
import smtplib, ssl
from src.helper import get_data, create_handle, create_permission_id, hash_encrypt, save_database_updates
from src.helper import create_reset_code, create_password_reset_jwt
from src.data_store import data_store
from src.error import InputError
from src.other import clear_v1

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
    store = get_data()
    for user in store['users']:
        if user['email'] == email:
            # check if encrypted password in database matches 
            # input password after encryption
            if user['password'] == hash_encrypt(password):
                return {
                    'auth_user_id' : user['u_id']
                }
            else:
                raise InputError(description = 'Error: Invalid password')
    raise InputError(description = 'Error: Invalid email')

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
    if os.path.getsize("database.json") == 0:
        clear_v1()  

    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    # Check for input errors
    if not re.fullmatch(regex, email):
        raise InputError(description = "Error: Invalid email")
    if len(password) < 6:
        raise InputError(description = "Error: Invalid password")
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError(description = "Error: Invalid first name")
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError(description = "Error: Invalid last name")

    # Fetch data
 
    store = get_data()

    # Check for repeated email
        # Put all emails in list
        # Append 'input email' to emails list
        # Check for duplicates in list of emails
    if len(store['users']) != 0:
        emails = []
        for user in store['users']:
            emails.append(user['email'])

        emails.append(email)
        if len(emails) != len(set(emails)):
            raise InputError("Error: email taken")



    # Generate handle
    handle_str = create_handle(name_first, name_last, store)
  
    # Generate permission_id
    permission_id = create_permission_id(store)
 
    # Generate id
    user_id = len(store['users']) + 1

    # Create and store account
    user = {
        'u_id': user_id,
        'email': email,
        # encrypt password
        'password': hash_encrypt(password),
        'name_first': name_first,
        'name_last': name_last,
        'handle_str': handle_str,
        'permission_id': permission_id
    }
    store['users'].append(user)
    save_database_updates(store)

    return {
        'auth_user_id': user_id,
    }

def auth_passwordreset_request_v1(email):
    db_store = get_data()
    # See if email is registered in database
    for index, user in enumerate(db_store['users']):
        if user['email'] == email:
            db_store['users'][index]['session_list'] = []
            reset_code = create_reset_code()
            reset_token = create_password_reset_jwt(user['u_id'], reset_code)
            db_store['reset_tokens'].append(reset_token)
            save_database_updates(db_store)

            port = 465 
            smtp_server = "smtp.gmail.com"
            sender_email = "noreply.dodostreams@gmail.com" 
            receiver_email = email
            password = "Dodostreams1531"
            message = f"""\
Subject: Reset Code

This is an automatically generated e-mail from Streams.

-------------------------
Thank you for using a Streams Account.
Please use the following code to change your password.

{reset_code}

If you do not know why you have received this e-mail, please delete it.

-------------------------
Sincerely.
Streams Co."""
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message)