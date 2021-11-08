import pytest
import requests
from json import loads
from src.other import clear_v1

from src import config

BASE_URL = config.url
OK = 200
ACCESS_ERROR = 403


def test_http_list_basic():
    '''
    Testing whether the v2 function works properly
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json={})
    
    user_0_json = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = user_0_json).json()

    channel_json = {
        'token': user['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_json).json()
    
    token_params = {
        'token': user['token']
    }
    
    response = requests.get(f"{BASE_URL}/channels/listall/v2", params = token_params)
    
    assert response.status_code == OK
    channel_list = response.json()
    
    assert channel_list == {'channels': [{'channel_id': channel['channel_id'], 'name': 'league'}]}

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
    requests.post(f"{BASE_URL}/channels/create/v2", json = channel_json).json()
    
    token_params = {
        'token': invalid['token'] # Incorrect token
    }
    
    response = requests.get(f"{BASE_URL}/channels/listall/v2", params = token_params)
    
    assert response.status_code == ACCESS_ERROR

def test_http_list_multiple():
    '''
    Test with multiple channels
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    user_0_json = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_0_json).json()


    user_1_json = {
        "email": "bob123@gmail.com",
        "password": "qwerty",
        "name_first": "Bob",
        "name_last": "Marley"
    }
    user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_1_json).json()
    
    channel_1_json = {
        'token': user_1['token'],
        'name': 'league1',
        'is_public': True
    }

    channel_2_json = {
        'token': user_2['token'],
        'name': 'league2',
        'is_public': False
    }

    channel_1 = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_1_json).json()
    channel_2 = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_2_json).json()
    
    token_params = {
        'token': user_1['token']
    }
    
    response = requests.get(f"{BASE_URL}/channels/listall/v2", params = token_params)
    
    assert response.status_code == OK
    channel_list = response.json()
    
    assert channel_list == {'channels': [{'channel_id': channel_1['channel_id'], 'name': 'league1'}, 
                                         {'channel_id': channel_2['channel_id'], 'name': 'league2'}]}