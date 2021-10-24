import requests
import pytest
import json

from src import config

BASE_URL = config.url

def test_msg_test_normal():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param = {
        "email": "test@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()
    
    channel_param = {
        'token': auth_user['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json()
    msg = "test"

    message_send_program = {
        'token': auth_user['token'],
        'channel_id': channel['channel_id'],
        'message': msg
    }

    response = requests.post(f"{BASE_URL}/message/send/v1",json = message_send_program)
    assert response.status_code == 200    

def test_msg_invalid_length_too_long():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param = {
        "email": "test@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()
    
    channel_param = {
        'token': auth_user['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json()
    invalid_msg = ',' * 1001

    message_send_program = {
        'token': auth_user['token'],
        'channel_id': channel['channel_id'],
        'message': invalid_msg
    }

    response = requests.post(f"{BASE_URL}/message/send/v1",json = message_send_program)
    assert response.status_code == 400

def test_msg_invalid_length_too_short():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param = {
        "email": "test@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()
    
    channel_param = {
        'token': auth_user['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json()
    invalid_msg = ''

    message_send_program = {
        'token': auth_user['token'],
        'channel_id': channel['channel_id'],
        'message': invalid_msg
    }

    response = requests.post(f"{BASE_URL}/message/send/v1",json = message_send_program)
    assert response.status_code == 400


def test_msg__invalid_auth_id_http():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    user1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    register_param_2 = {
        "email": "test2@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Smith"
    }
    user2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()

    channel_param = {
        'token': user1['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json()
    
    msg = 'test'

    message_send_program = {
        'token': user2['token'],
        'channel_id': channel['channel_id'],
        'message': msg
    }

    response = requests.post(f"{BASE_URL}/message/send/v1",json = message_send_program)
    assert response.status_code == 403
