import pytest
import requests
from json import loads
from src.other import clear_v1

BASE_URL = 'http://localhost:8080'


def test_http_list_basic():
    '''
    Testing whether the v2 function works properly
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json={})
    
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
    
    token = {
        'token': user['token']
    }
    
    response = requests.get(f"{BASE_URL}/channels/listall/v2", json = token)
    
    assert response.status_code == 200
    channel_list = response.json()
    
    assert channel_list == {'channels': [{'channel_id': channel['channel_id'], 'name': 'league'}]}

def test_http_invalid_token():
    '''
    Testing whether the v2 function can identify incorrect tokens
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json={})
    
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
    requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json()
    
    token = {
        'token': user['token'] + '1' # Incorrect token
    }
    
    response = requests.get(f"{BASE_URL}/channels/listall/v2", json = token)
    
    assert response.status_code != 200

def test_http_list_multiple():
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

    channel_1 = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param_1).json()
    channel_2 = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param_2).json()
    
    token = {
        'token': user['token']
    }
    
    response = requests.get(f"{BASE_URL}/channels/listall/v2", json = token)
    
    assert response.status_code == 200
    channel_list = response.json()
    
    assert channel_list == {'channels': [{'channel_id': channel_1['channel_id'], 'name': 'league1'}, 
                                         {'channel_id': channel_2['channel_id'], 'name': 'league2'}]}