import requests
import pytest
from src.other import clear_v1

from src import config

BASE_URL = config.url

def test_http_channels_create_basic():
    '''
    Test if the http channels/create/v2 function working properly
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
    response = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param)

    assert response.status_code == 200

    channel = response.json()
    channel_id = channel['channel_id']
    assert channel_id == 1

def test_http_invalid_channel_name():
    '''
    Test when the channel_name is invalid
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})

    register_param = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    channel_param_1 = {
        'token': user['token'],
        'name': 'aaaabbbbccccddddeeee1',
        'is_public': True
    }

    channel_param_2 = {
        'token': user['token'],
        'name': '',
        'is_public': True
    }

    response_1 = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param_1)
    response_2 = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param_2)

    assert response_1.status_code == 400
    assert response_2.status_code == 400

def test_http_invalid_token():
    '''
    Test when the user token is invalid
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
        'token': user['token'] + '1', # token invalid
        'name': 'league',
        'is_public': True
    }
    response = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param)

    assert response.status_code == 500

def test_http_create_multiples():
    '''
    Test when create multiple channels
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    channel_param_1 = {
        'token': user['token'], # token invalid
        'name': 'league1',
        'is_public': True
    }

    channel_param_2 = {
        'token': user['token'], # token invalid
        'name': 'league2',
        'is_public': False
    }

    response_1 = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param_1)
    response_2 = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param_2)
    assert response_1.status_code == 200
    assert response_2.status_code == 200

    channel_1 = response_1.json()
    channel_id_1 = channel_1['channel_id']
    channel_2 = response_2.json()
    channel_id_2 = channel_2['channel_id']
    assert channel_id_1 == 1
    assert channel_id_2 == 2
