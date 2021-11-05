import requests
import pytest
from src import config

BASE_URL = config.url
OK = 200
ACCESS_ERROR = 403
INPUT_ERROR = 400

def test_invalid_token():
    '''
    Checking if the function identifies incorrect tokens
    '''
    # Creating invalid user token
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    user_json_0 = {
        "email": "bob123@gmail.com",
        "password": "bobahe",
        "name_first": "Bob",
        "name_last": "Marley"
    }
    
    invalid_user = requests.post(f"{BASE_URL}/auth/register/v2", json = user_json_0).json()
    
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    # Creating new users
    
    user_json_1 = {
        "email": "shifanchen@gmail.com",
        "password": "djkadldjsa21",
        "name_first": "shifan",
        "name_last": "chen"
    }
    requests.post(f"{BASE_URL}/auth/register/v2", json = user_json_1).json()
    
    user_json_2 = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    requests.post(f"{BASE_URL}/auth/register/v2", json = user_json_2).json()
    
    # Using invalid user token
    
    message_pin_json = {
        'token': invalid_user['token'], # Invalid Token
        'message_id': 12,
    }

    response = requests.post(f"{BASE_URL}/message/pin/v1", json = message_pin_json)
    
    assert response.status_code == ACCESS_ERROR


def test_invalid_message_id():
    '''
    Testing if the function identifies invalid message ids
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    # Creating users
    
    user_json_1 = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = user_json_1).json()

    user_json_2 = {
        "email": "bob123@gmail.com",
        "password": "bobahe",
        "name_first": "Bob",
        "name_last": "Marley"
    }
    user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_json_2).json()
    
    # Creating and joining channel
    channel_json_1 = {
        'token': auth_user['token'],
        'name': 'league1',
        'is_public': True
    }
    channel_1 = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_json_1).json()
    
    join_json = {
        'token': user_2['token'],
        'channel_id': channel_1['channel_id']
    }
    requests.post(f"{BASE_URL}/channel/join/v2", json = join_json)

    # Sending message
    message_info_json = {
        'token': auth_user['token'],
        'channel_id': channel_1['channel_id'],
        'message': "Hello"
    }
    message = requests.post(f"{BASE_URL}/message/send/v1", json = message_info_json).json()
    
    # Calling wrong message
    message_pin_json = {
        'token': auth_user['token'],
        'message_id': message['message_id'] + 35
    }
    response = requests.post(f"{BASE_URL}/message/pin/v1", json = message_pin_json)
    assert response.status_code == INPUT_ERROR


def test_message_already_pinned():
    '''
    Testing if the function checks if the message is already pinned
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    # Creating users
    user_json_1 = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = user_json_1).json()

    user_json_2 = {
        "email": "bob123@gmail.com",
        "password": "bobahe",
        "name_first": "Bob",
        "name_last": "Marley"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_json_2).json()
    
    # Creating and joining channels
    channel_json_1 = {
        'token': auth_user['token'],
        'name': 'league1',
        'is_public': True
    }
    channel_1 = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_json_1).json()
    
    join_json = {
        'token': user_1['token'],
        'channel_id': channel_1['channel_id']
    }
    requests.post(f"{BASE_URL}/channel/join/v2", json = join_json)

    # Sending message
    message_info_json = {
        'token': auth_user['token'],
        'channel_id': channel_1['channel_id'],
        'message': "Hello"
    }
    
    message = requests.post(f"{BASE_URL}/message/send/v1", json = message_info_json).json()
    
    # Pinning the same message twice
    message_pin_json = {
        'token': auth_user['token'],
        'message_id': message['message_id']
    }
    requests.post(f"{BASE_URL}/message/pin/v1", json = message_pin_json)

    message_pin_json = {
        'token': auth_user['token'],
        'message_id': message['message_id']
    }
    response = requests.post(f"{BASE_URL}/message/pin/v1", json = message_pin_json)
    assert response.status_code == INPUT_ERROR

    # Creating dm
    dm_create_json = {
        'token': auth_user['token'],
        'u_ids': [user_1['auth_user_id']],
    }
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_create_json).json()

    # Sending message in dm
    dm_message_json = {
        'token': auth_user['token'],
        'dm_id': dm['dm_id'],
        'message': "Hi"
    }
    dm_message = requests.post(f"{BASE_URL}/message/senddm/v1", json = dm_message_json).json()

    # Pinning message twice
    message_pin_json = {
        'token': auth_user['token'],
        'message_id': dm_message['message_id']
    }
    requests.post(f"{BASE_URL}/message/pin/v1", json = message_pin_json)

    message_pin_json = {
        'token': auth_user['token'],
        'message_id': dm_message['message_id']
    }
    response = requests.post(f"{BASE_URL}/message/pin/v1", json = message_pin_json)
    assert response.status_code == INPUT_ERROR


def test_non_owner_permissions():
    '''
    Testing if the function checks owner permissions
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    # Creating users
    user_json_1 = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = user_json_1).json()

    user_json_2 = {
        "email": "bob123@gmail.com",
        "password": "bobahe",
        "name_first": "Bob",
        "name_last": "Marley"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_json_2).json()
    
    # Creating and joining channel
    channel_json_1 = {
        'token': auth_user['token'],
        'name': 'league1',
        'is_public': True
    }
    channel_1 = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_json_1).json()
    
    join_json = {
        'token': user_1['token'],
        'channel_id': channel_1['channel_id']
    }
    requests.post(f"{BASE_URL}/channel/join/v2", json = join_json)

    # Sending message
    message_info_json = {
        'token': auth_user['token'],
        'channel_id': channel_1['channel_id'],
        'message': "Hello"
    }
    message = requests.post(f"{BASE_URL}/message/send/v1", json = message_info_json).json()
    
    # Unauthorised user pinning message
    message_pin_json = {
        'token': user_1['token'],
        'message_id': message['message_id']
    }
    response = requests.post(f"{BASE_URL}/message/pin/v1", json = message_pin_json)
    assert response.status_code == ACCESS_ERROR

    # Creating dm
    dm_create_json = {
        'token': auth_user['token'],
        'u_ids': [user_1['auth_user_id']],
    }
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_create_json).json()

    # Sending message in dm
    dm_message_json = {
        'token': auth_user['token'],
        'dm_id': dm['dm_id'],
        'message': "Hi"
    }
    dm_message = requests.post(f"{BASE_URL}/message/senddm/v1", json = dm_message_json).json()

    # Unauthorised user pinning message
    message_pin_json = {
        'token': user_1['token'],
        'message_id': dm_message['message_id']
    }
    response = requests.post(f"{BASE_URL}/message/pin/v1", json = message_pin_json)
    assert response.status_code == ACCESS_ERROR


def test_not_member():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    # Creating users
    user_json_1 = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = user_json_1).json()

    user_json_2 = {
        "email": "bob123@gmail.com",
        "password": "bobahe",
        "name_first": "Bob",
        "name_last": "Marley"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_json_2).json()
    
    # Creating channel but not joining
    channel_json_1 = {
        'token': auth_user['token'],
        'name': 'league1',
        'is_public': True
    }
    channel_1 = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_json_1).json()

    # Sending message
    message_info_json = {
        'token': auth_user['token'],
        'channel_id': channel_1['channel_id'],
        'message': "Hello"
    }
    message = requests.post(f"{BASE_URL}/message/send/v1", json = message_info_json).json()
    
    # Member not in channel pinning message
    message_pin_json = {
        'token': user_1['token'],
        'message_id': message['message_id']
    }
    response = requests.post(f"{BASE_URL}/message/pin/v1", json = message_pin_json)
    assert response.status_code == INPUT_ERROR

    # Creating dm without second user
    dm_create_json = {
        'token': auth_user['token'],
        'u_ids': [],
    }
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_create_json).json()

    # Sending message in dm
    dm_message_json = {
        'token': auth_user['token'],
        'dm_id': dm['dm_id'],
        'message': "Hi"
    }
    dm_message = requests.post(f"{BASE_URL}/message/senddm/v1", json = dm_message_json).json()

    # Second user pinning message
    message_pin_json = {
        'token': user_1['token'],
        'message_id': dm_message['message_id']
    }
    response = requests.post(f"{BASE_URL}/message/pin/v1", json = message_pin_json)
    assert response.status_code == INPUT_ERROR


def test_valid():
    '''
    Testing if the function works properly
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    # Creating users
    user_json_1 = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = user_json_1).json()

    user_json_2 = {
        "email": "bob123@gmail.com",
        "password": "bobahe",
        "name_first": "Bob",
        "name_last": "Marley"
    }
    user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_json_2).json()
    
    # Creating and joining channel
    channel_json_1 = {
        'token': auth_user['token'],
        'name': 'league1',
        'is_public': True
    }
    channel_1 = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_json_1).json()
    
    join_json = {
        'token': user_2['token'],
        'channel_id': channel_1['channel_id']
    }
    requests.post(f"{BASE_URL}/channel/join/v2", json = join_json)

    # Sending message
    message_info_json = {
        'token': auth_user['token'],
        'channel_id': channel_1['channel_id'],
        'message': "Hello"
    }
    message = requests.post(f"{BASE_URL}/message/send/v1", json = message_info_json).json()

    # Checking if message is pinned
    messages_info_param = {
        'token': auth_user['token'],
        'channel_id': channel_1['channel_id'],
        'start': 0,
    }
    messages = requests.get(f"{BASE_URL}/channel/messages/v2", params = messages_info_param).json()
    assert messages['messages'][0]['is_pinned'] == False
    
    # Pinning message and checking if pinned
    message_pin = {
        'token': auth_user['token'],
        'message_id': message['message_id']
    }
    response = requests.post(f"{BASE_URL}/message/pin/v1", json = message_pin)
    response.status_code == OK

    messages_info_param = {
        'token': auth_user['token'],
        'channel_id': channel_1['channel_id'],
        'start': 0,
    }
    messages = requests.get(f"{BASE_URL}/channel/messages/v2", params = messages_info_param).json()
    assert messages['messages'][0]['is_pinned'] == True

    # Sending second message
    message_info_json = {
        'token': user_2['token'],
        'channel_id': channel_1['channel_id'],
        'message': "Hi"
    }
    message_1 = requests.post(f"{BASE_URL}/message/send/v1", json = message_info_json).json()
    
    # Making second user global owner
    permission_info_json = {
        'token': auth_user['token'],
        'u_id': user_2['auth_user_id'],
        'permission_id': 1
    }
    response = requests.post(f"{BASE_URL}/admin/userpermission/change/v1", json = permission_info_json)

    # Second user pinning message
    message_pin_json = {
        'token': user_2['token'],
        'message_id': message_1['message_id']
    }
    response = requests.post(f"{BASE_URL}/message/pin/v1", json = message_pin_json)
    assert response.status_code == OK

    # Checking if message was pinned
    messages_info_param = {
        'token': auth_user['token'],
        'channel_id': channel_1['channel_id'],
        'start': 0,
    }
    messages = requests.get(f"{BASE_URL}/channel/messages/v2", params = messages_info_param).json()
    assert messages['messages'][1]['is_pinned'] == True

    # Creating dm
    dm_param_1 = {
        'token': auth_user['token'],
        'u_ids': [user_2['auth_user_id']],
    }
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_param_1).json()

    # Sending message in dm
    dm_message_json = {
        'token': auth_user['token'],
        'dm_id': dm['dm_id'],
        'message': "Hi"
    }
    dm_message = requests.post(f"{BASE_URL}/message/senddm/v1", json = dm_message_json).json()

    # Pinning message in dm
    message_pin_json = {
        'token': auth_user['token'],
        'message_id': dm_message['message_id']
    }
    response = requests.post(f"{BASE_URL}/message/pin/v1", json = message_pin_json)
    assert response.status_code == OK
    
    # Checking message is pinned
    messages_info_json = {
        'token': auth_user['token'],
        'dm_id': dm['dm_id'],
        'start': 0,
    }
    messages = requests.get(f"{BASE_URL}/dm/messages/v1", params = messages_info_json).json()
    assert messages['messages'][0]['is_pinned'] == True