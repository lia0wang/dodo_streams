import requests
import pytest
from src.other import clear_v1

from src import config

BASE_URL = config.url
def test_http_channel_join_basic():
    '''
    Test if channel/join/v2 working properly,
    create a public channel with user 1 and let user 2 join that channel
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
    
    channel_join_param = {
        'token': user_2['token'],
        'channel_id': channel['channel_id']
    }

    response = requests.post(f"{BASE_URL}/channel/join/v2", json = channel_join_param)
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

    channel_join_param = {
        'token': user['token'],
        'channel_id': channel['channel_id'] + 1
    }

    response = requests.post(f"{BASE_URL}/channel/join/v2", json = channel_join_param)
    assert response.status_code == 400

def test_join_private_channel():
    '''
    Test when the channel is private and the user who wants to join that channel
    is neither channel member nor global owner.
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})

    # Create a private channel with user 1
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
        'is_public': False
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json() 

    # Let user 2 join the private channel, and it will get a forbidden response
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

    response = requests.post(f"{BASE_URL}/channel/join/v2", json = channel_join_param)
    assert response.status_code == 403

def test_http_none_existing_channel():
    '''
    Test when the channel is none-existing
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})

    register_param = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    channel_join_param = {
        'token': user['token'],
        'channel_id': -1
    }

    response = requests.post(f"{BASE_URL}/channel/join/v2", json = channel_join_param)
    assert response.status_code == 400

def test_http_global_owner():
    '''
    Test if a global owner can join the private channel.
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    # The first user will be the global owner
    register_param_1 = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    global_owner = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    register_param_2 = {
        "email": "z5306312@gmail.com",
        "password": "LeonLiao123",
        "name_first": "Leon",
        "name_last": "Liao"
    }
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()

    # Create a private channel with non-gloabl-owner user
    channel_param = {
        'token': user['token'],
        'name': 'league',
        'is_public': False
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json()

    # Let the global owner join the channel
    channel_join_param = {
        'token': global_owner['token'],
        'channel_id': channel['channel_id']
    }

    response = requests.post(f"{BASE_URL}/channel/join/v2", json = channel_join_param)
    assert response.status_code == 200
def test_http_duplicated_joins():
    '''
    Test when join the same channel duplicated times,
    create a public channel with user 1
    let user 2 join multiple times
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

    channel_join_param = {
        'token': user_2['token'],
        'channel_id': channel['channel_id']
    }
    response = requests.post(f"{BASE_URL}/channel/join/v2", json = channel_join_param)
    assert response.status_code == 200

    response = requests.post(f"{BASE_URL}/channel/join/v2", json = channel_join_param)
    assert response.status_code == 400

    response = requests.post(f"{BASE_URL}/channel/join/v2", json = channel_join_param)
    assert response.status_code == 400