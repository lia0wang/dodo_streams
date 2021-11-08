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
        'u_id': user_1['auth_user_id'],
        'permission_id': 2
    }

    response = requests.post(f"{BASE_URL}/admin/userpermission/change/v1", json = permission_info)
    
    assert response.status_code == ACCESS_ERROR

def test_invalid_uid():
    '''
    Checking if the function idenitifies invalid u_ids
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param_1 = {
        "email": "shifanchen@gmail.com",
        "password": "djkadldjsa21",
        "name_first": "shifan",
        "name_last": "chen"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    register_param_2 = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()
    
    permission_info = {
        'token': auth_user['token'],
        'u_id': user_1['auth_user_id'] + 26,
        'permission_id': 2
    }

    response = requests.post(f"{BASE_URL}/admin/userpermission/change/v1", json = permission_info)
    
    assert response.status_code == INPUT_ERROR
    
def test_last_global():
    '''
    Checking if the function identifies if the u_id is the only global owner
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param_1 = {
        "email": "shifanchen@gmail.com",
        "password": "djkadldjsa21",
        "name_first": "shifan",
        "name_last": "chen"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()
    
    permission_info = {
        'token': auth_user['token'],
        'u_id': auth_user['auth_user_id'],
        'permission_id': 2
    }

    response = requests.post(f"{BASE_URL}/admin/userpermission/change/v1", json = permission_info)
    
    assert response.status_code == INPUT_ERROR
    
def test_invalid_permission():
    '''
    Checking if the function identifies if the permission_id is invalid
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param_1 = {
        "email": "shifanchen@gmail.com",
        "password": "djkadldjsa21",
        "name_first": "shifan",
        "name_last": "chen"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    register_param_2 = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()
    
    permission_info = {
        'token': auth_user['token'],
        'u_id': user_1['auth_user_id'],
        'permission_id': 7
    }

    response = requests.post(f"{BASE_URL}/admin/userpermission/change/v1", json = permission_info)
    
    assert response.status_code == INPUT_ERROR
    
def test_token_not_global():
    '''
    Checking if the function identifies if the token's u_id is not global owner
    '''
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
    
    register_param_3 = {
        "email": "bob123@gmail.com",
        "password": "bobahe",
        "name_first": "Bob",
        "name_last": "Marley"
    }
    user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_3).json()
    
    permission_info = {
        'token': user_1['token'],
        'u_id': user_2['auth_user_id'],
        'permission_id': 1
    }

    response = requests.post(f"{BASE_URL}/admin/userpermission/change/v1", json = permission_info)
    
    assert response.status_code == ACCESS_ERROR
    
def test_basic():
    '''
    Checking if the function works normally
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
    
    permission_info = {
        'token': auth_user['token'],
        'u_id': user_1['auth_user_id'],
        'permission_id': 1
    }

    response = requests.post(f"{BASE_URL}/admin/userpermission/change/v1", json = permission_info)
    
    assert response.status_code == OK
    
    token = {
        'token': user_1['token']
    }
    
    user_list = requests.get(f"{BASE_URL}/users/all/v1", params = token).json()
    assert user_list["users"][0]['u_id'] == auth_user['auth_user_id']
    assert user_list["users"][0]['email'] == "11037.666@gmail.com"
    assert user_list["users"][0]['name_first'] == "Hopeful"
    assert user_list["users"][0]['name_last'] == "Boyyy"
    assert user_list["users"][0]['handle_str'] == "hopefulboyyy"

    assert user_list["users"][1]['u_id'] == user_1['auth_user_id']
    assert user_list["users"][1]['email'] == "bob123@gmail.com"
    assert user_list["users"][1]['name_first'] == "Bob"
    assert user_list["users"][1]['name_last'] == "Marley"
    assert user_list["users"][1]['handle_str'] == "bobmarley"

    message_info = {
        'token': auth_user['token'],
        'channel_id': channel_1['channel_id'],
        'message': "Hello"
    }
    
    message = requests.post(f"{BASE_URL}/message/send/v1", json = message_info).json()
    
    message_remove = {
        'token': user_1['token'],
        'message_id': message['message_id']
    }
    response = requests.delete(f"{BASE_URL}/message/remove/v1", json = message_remove)
    assert response.status_code == OK