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
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param_0 = {
        "email": "bob123@gmail.com",
        "password": "bobahe",
        "name_first": "Bob",
        "name_last": "Marley"
    }
    
    invalid = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_0).json()
    
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param_1 = {
        "email": "shifanchen@gmail.com",
        "password": "djkadldjsa21",
        "name_first": "shifan",
        "name_last": "chen"
    }
    requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()
    
    register_param_2 = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()
    
    permission_info = {
        'token': invalid['token'], # Invalid Token
        'message_id': 12,
    }

    response = requests.post(f"{BASE_URL}/message/pin/v1", json = permission_info)
    
    assert response.status_code == ACCESS_ERROR


def test_invalid_message_id():
    '''
    Testing if the function identifies invalid message ids
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param_1 = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    register_param_2 = {
        "email": "bob123@gmail.com",
        "password": "bobahe",
        "name_first": "Bob",
        "name_last": "Marley"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()
    
    channel_param_1 = {
        'token': auth_user['token'],
        'name': 'league1',
        'is_public': True
    }
    channel_1 = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param_1).json()
    
    join_details = {
        'token': user_1['token'],
        'channel_id': channel_1['channel_id']
    }
    requests.post(f"{BASE_URL}/channel/join/v2", json = join_details)


    message_info = {
        'token': auth_user['token'],
        'channel_id': channel_1['channel_id'],
        'message': "Hello"
    }
    
    message = requests.post(f"{BASE_URL}/message/send/v1", json = message_info).json()
    
    message_pin = {
        'token': auth_user['token'],
        'message_id': message['message_id'] + 35
    }
    response = requests.post(f"{BASE_URL}/message/pin/v1", json = message_pin)
    assert response.status_code == INPUT_ERROR


def test_message_already_pinned():
    '''
    Testing if the function checks if the message is already pinned
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param_1 = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    register_param_2 = {
        "email": "bob123@gmail.com",
        "password": "bobahe",
        "name_first": "Bob",
        "name_last": "Marley"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()
    
    channel_param_1 = {
        'token': auth_user['token'],
        'name': 'league1',
        'is_public': True
    }
    channel_1 = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param_1).json()
    
    join_details = {
        'token': user_1['token'],
        'channel_id': channel_1['channel_id']
    }
    requests.post(f"{BASE_URL}/channel/join/v2", json = join_details)


    message_info = {
        'token': auth_user['token'],
        'channel_id': channel_1['channel_id'],
        'message': "Hello"
    }
    
    message = requests.post(f"{BASE_URL}/message/send/v1", json = message_info).json()
    
    message_pin = {
        'token': auth_user['token'],
        'message_id': message['message_id']
    }
    requests.post(f"{BASE_URL}/message/pin/v1", json = message_pin)

    message_pin = {
        'token': auth_user['token'],
        'message_id': message['message_id']
    }
    response = requests.post(f"{BASE_URL}/message/pin/v1", json = message_pin)
    assert response.status_code == INPUT_ERROR

    dm_param_1 = {
        'token': auth_user['token'],
        'u_ids': [user_1['auth_user_id']],
    }
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_param_1).json()

    dm_message = {
        'token': auth_user['token'],
        'dm_id': dm['dm_id'],
        'message': "Hi"
    }
    
    dm_message = requests.post(f"{BASE_URL}/message/senddm/v1", json = dm_message).json()

    message_pin = {
        'token': auth_user['token'],
        'message_id': dm_message['message_id']
    }
    requests.post(f"{BASE_URL}/message/pin/v1", json = message_pin)

    message_pin = {
        'token': auth_user['token'],
        'message_id': dm_message['message_id']
    }
    response = requests.post(f"{BASE_URL}/message/pin/v1", json = message_pin)
    assert response.status_code == INPUT_ERROR


def test_non_owner_permissions():
    '''
    Testing if the function checks owner permissions
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param_1 = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    register_param_2 = {
        "email": "bob123@gmail.com",
        "password": "bobahe",
        "name_first": "Bob",
        "name_last": "Marley"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()
    
    channel_param_1 = {
        'token': auth_user['token'],
        'name': 'league1',
        'is_public': True
    }
    channel_1 = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param_1).json()
    
    join_details = {
        'token': user_1['token'],
        'channel_id': channel_1['channel_id']
    }
    requests.post(f"{BASE_URL}/channel/join/v2", json = join_details)


    message_info = {
        'token': auth_user['token'],
        'channel_id': channel_1['channel_id'],
        'message': "Hello"
    }
    
    message = requests.post(f"{BASE_URL}/message/send/v1", json = message_info).json()
    
    message_pin = {
        'token': user_1['token'],
        'message_id': message['message_id']
    }
    response = requests.post(f"{BASE_URL}/message/pin/v1", json = message_pin)
    assert response.status_code == ACCESS_ERROR

    dm_param_1 = {
        'token': auth_user['token'],
        'u_ids': [user_1['auth_user_id']],
    }
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_param_1).json()

    dm_message = {
        'token': auth_user['token'],
        'dm_id': dm['dm_id'],
        'message': "Hi"
    }
    
    dm_message = requests.post(f"{BASE_URL}/message/senddm/v1", json = dm_message).json()

    message_pin = {
        'token': user_1['token'],
        'message_id': dm_message['message_id']
    }
    response = requests.post(f"{BASE_URL}/message/pin/v1", json = message_pin)
    assert response.status_code == ACCESS_ERROR


def test_not_member():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param_1 = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    register_param_2 = {
        "email": "bob123@gmail.com",
        "password": "bobahe",
        "name_first": "Bob",
        "name_last": "Marley"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()
    
    channel_param_1 = {
        'token': auth_user['token'],
        'name': 'league1',
        'is_public': True
    }
    channel_1 = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param_1).json()

    message_info = {
        'token': auth_user['token'],
        'channel_id': channel_1['channel_id'],
        'message': "Hello"
    }
    
    message = requests.post(f"{BASE_URL}/message/send/v1", json = message_info).json()
    
    message_pin = {
        'token': user_1['token'],
        'message_id': message['message_id']
    }
    response = requests.post(f"{BASE_URL}/message/pin/v1", json = message_pin)
    assert response.status_code == INPUT_ERROR

    dm_param_1 = {
        'token': auth_user['token'],
        'u_ids': [],
    }
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_param_1).json()

    dm_message = {
        'token': auth_user['token'],
        'dm_id': dm['dm_id'],
        'message': "Hi"
    }
    
    dm_message = requests.post(f"{BASE_URL}/message/senddm/v1", json = dm_message).json()

    message_pin = {
        'token': user_1['token'],
        'message_id': dm_message['message_id']
    }
    response = requests.post(f"{BASE_URL}/message/pin/v1", json = message_pin)
    assert response.status_code == INPUT_ERROR

def test_valid():
    '''
    Testing if the function works properly
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param_1 = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    register_param_2 = {
        "email": "bob123@gmail.com",
        "password": "bobahe",
        "name_first": "Bob",
        "name_last": "Marley"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()
    
    channel_param_1 = {
        'token': auth_user['token'],
        'name': 'league1',
        'is_public': True
    }
    channel_1 = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param_1).json()
    
    join_details = {
        'token': user_1['token'],
        'channel_id': channel_1['channel_id']
    }
    requests.post(f"{BASE_URL}/channel/join/v2", json = join_details)


    message_info = {
        'token': auth_user['token'],
        'channel_id': channel_1['channel_id'],
        'message': "Hello"
    }
    
    message = requests.post(f"{BASE_URL}/message/send/v1", json = message_info).json()

    messages_info = {
        'token': auth_user['token'],
        'channel_id': channel_1['channel_id'],
        'start': 0,
    }

    messages = requests.get(f"{BASE_URL}/channel/messages/v2", params = messages_info).json()

    assert messages['messages'][0]['is_pinned'] == False
    
    message_pin = {
        'token': auth_user['token'],
        'message_id': message['message_id']
    }
    response = requests.post(f"{BASE_URL}/message/pin/v1", json = message_pin)
    response.status_code == OK

    messages_info = {
        'token': auth_user['token'],
        'channel_id': channel_1['channel_id'],
        'start': 0,
    }

    messages = requests.get(f"{BASE_URL}/channel/messages/v2", params = messages_info).json()

    assert messages['messages'][0]['is_pinned'] == True

    message_info = {
        'token': user_1['token'],
        'channel_id': channel_1['channel_id'],
        'message': "Hi"
    }
    
    message_1 = requests.post(f"{BASE_URL}/message/send/v1", json = message_info).json()
    
    permission_info = {
        'token': auth_user['token'],
        'u_id': user_1['auth_user_id'],
        'permission_id': 1
    }

    response = requests.post(f"{BASE_URL}/admin/userpermission/change/v1", json = permission_info)

    message_pin = {
        'token': user_1['token'],
        'message_id': message_1['message_id']
    }
    response = requests.post(f"{BASE_URL}/message/pin/v1", json = message_pin)
    assert response.status_code == OK

    messages_info = {
        'token': auth_user['token'],
        'channel_id': channel_1['channel_id'],
        'start': 0,
    }

    messages = requests.get(f"{BASE_URL}/channel/messages/v2", params = messages_info).json()
    assert messages['messages'][1]['is_pinned'] == True

    dm_param_1 = {
        'token': auth_user['token'],
        'u_ids': [user_1['auth_user_id']],
    }
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_param_1).json()

    dm_message = {
        'token': auth_user['token'],
        'dm_id': dm['dm_id'],
        'message': "Hi"
    }
    
    dm_message = requests.post(f"{BASE_URL}/message/senddm/v1", json = dm_message).json()

    message_pin = {
        'token': auth_user['token'],
        'message_id': dm_message['message_id']
    }
    response = requests.post(f"{BASE_URL}/message/pin/v1", json = message_pin)
    assert response.status_code == OK
    
    messages_info = {
        'token': auth_user['token'],
        'dm_id': dm['dm_id'],
        'start': 0,
    }

    messages = requests.get(f"{BASE_URL}/dm/messages/v1", params = messages_info).json()
    assert messages['messages'][0]['is_pinned'] == True