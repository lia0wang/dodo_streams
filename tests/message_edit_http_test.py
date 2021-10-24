
import requests
import pytest
import json
from src.message import message_send_v1, message_edit_v1, message_remove_v1

from src import config

BASE_URL = config.url
'''
def test_msg_ed_normal_html():
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

    target_message = requests.post(f"{BASE_URL}/message/send/v1",json = message_send_program).json()

    print(target_message)

    edit_msg = "edit_test"

    
    message_edit_program = {
        'token': auth_user['token'],
        'message_id': target_message['message_id'],
        'message': edit_msg
    }

    channel_list = requests.get(f"{BASE_URL}/channels/list/v2",json = auth_user['token']).json()

    print(channel_list)

    response = requests.put(f"{BASE_URL}/message/edit/v1",json = message_edit_program)
    print(response.json())
    assert response.status_code == 200
'''
def test_msg_ed_invalid_length_too_long_html():
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

    target_message = requests.post(f"{BASE_URL}/message/send/v1",json = message_send_program).json()

    invalid_msg = ',' * 1001
    
    message_edit_program = {
        'token': auth_user['token'],
        'message_id': target_message['message_id'],
        'message': msg
    }

    response = requests.put(f"{BASE_URL}/message/edit/v1",json = message_edit_program)

    assert response.status_code == 400


