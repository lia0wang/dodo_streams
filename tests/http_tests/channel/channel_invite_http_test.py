import requests
import pytest

from src import config

BASE_URL = config.url

def test_http_channel_invite_basic():
    '''
    Tests for valid channel_invite_v1 implementation
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})

    register_param_1 = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    channel_param = {
        'token': user_1['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json() 

    register_param_2 = {
        "email": "z5306312@gmail.com",
        "password": "LeonLiao123",
        "name_first": "Leon",
        "name_last": "Liao"
    }
    user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()
    
    channel_invites_param = {
        'token': user_1['token'],
        'channel_id': channel['channel_id'],
        'u_id': user_2['auth_user_id']
    }
    response = requests.post(f"{BASE_URL}/channel/invite/v2", json = channel_invites_param)
    assert response.status_code == 200

def test_http_invalid_channel_id():
    '''
    Test if the channel_id is invalid
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})

    register_param = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    channel_param = {
        'token': user['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json() 

    register_param_2 = {
        "email": "z5306312@gmail.com",
        "password": "LeonLiao123",
        "name_first": "Leon",
        "name_last": "Liao"
    }
    user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()

    channel_invite_param = {
        'token': user['token'],
        'channel_id': channel['channel_id'] + 999,
        'u_id': user_2['auth_user_id']
    }
    response = requests.post(f"{BASE_URL}/channel/invite/v2", json = channel_invite_param)
    assert response.status_code == 400

def test_http_invalid_u_id():
    '''
    Test if the u_id is invalid
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})

    register_param = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    channel_param = {
        'token': user['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json() 

    register_param_2 = {
        "email": "z5306312@gmail.com",
        "password": "LeonLiao123",
        "name_first": "Leon",
        "name_last": "Liao"
    }
    user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()

    channel_invite_param = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'u_id': user_2['auth_user_id'] + 999
    }
    response = requests.post(f"{BASE_URL}/channel/invite/v2", json = channel_invite_param)
    assert response.status_code == 400

def test_http_user_is_member():
    '''
    Test when the user is already a member of the channel
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})

    register_param = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    channel_param = {
        'token': user['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json() 

    register_param_2 = {
        "email": "z5306312@gmail.com",
        "password": "LeonLiao123",
        "name_first": "Leon",
        "name_last": "Liao"
    }
    user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()

    channel_join_param = {
        'token': user_2['token'],
        'channel_id': channel['channel_id']
    }
    requests.post(f"{BASE_URL}/channel/join/v2", json = channel_join_param)

    channel_invite_param = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'u_id': user_2['auth_user_id']
    }
    response = requests.post(f"{BASE_URL}/channel/invite/v2", json = channel_invite_param)
    assert response.status_code == 400

def test_http_auth_is_not_member():
    '''
    Test when the authorize user is not a member of the channel
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})

    register_param = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    channel_param = {
        'token': user['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json() 

    register_param_2 = {
        "email": "z5306312@gmail.com",
        "password": "LeonLiao123",
        "name_first": "Leon",
        "name_last": "Liao"
    }
    user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()

    channel_leave_param = {
        'token': user['token'],
        'channel_id': channel['channel_id']
    }
    requests.post(f"{BASE_URL}/channel/leave/v1", json = channel_leave_param)

    channel_invite_param = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'u_id': user_2['auth_user_id']
    }
    response = requests.post(f"{BASE_URL}/channel/invite/v2", json = channel_invite_param)
    assert response.status_code == 403

def test_http_invalid_token():
    '''
    Testing whether the v2 function can identify incorrect tokens
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    invalid_user_json = {
        "email": "bob123@gmail.com",
        "password": "bobahe",
        "name_first": "Bob",
        "name_last": "Marley"
    }
    
    invalid = requests.post(f"{BASE_URL}/auth/register/v2", json = invalid_user_json).json()
    
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    user_1_json = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = user_1_json).json()

    channel_json = {
        'token': user['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_json).json()
    
    channel_invite_param = {
        'token': invalid['token'],
        'channel_id': channel['channel_id'],
        'u_id': user['auth_user_id']
    }
    response = requests.post(f"{BASE_URL}/channel/invite/v2", json = channel_invite_param)

    assert response.status_code == 403