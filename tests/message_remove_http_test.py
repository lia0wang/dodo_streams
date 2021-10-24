import requests
import pytest
import json
from src.message import message_send_v1, message_remove_v1

from src import config

BASE_URL = config.url

def test_msg_rm_invalid_msg_id():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    message_1 = "dsdaada"
    message_2 = "pojno"
    
    register_param_1 = {
        "email": "test@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    auth_user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()
    
    channel_param_1 = {
        'token': auth_user_1['token'],
        'name': 'league',
        'is_public': True
    }
    channel_1 = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param_1).json()
    
    message_send_program_1 = {
        'token': auth_user_1['token'],
        'channel_id': channel_1['channel_id'],
        'message': message_1
    }

    msg_id_1 = requests.post(f"{BASE_URL}/message/send/v1",json = message_send_program_1).json()

    register_param_2 = {
        "email": "tset@gmail.com",
        "password": "abcd1234",
        "name_first": "Smith",
        "name_last": "John"
    }
    auth_user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()
    
    channel_param_2 = {
        'token': auth_user_2['token'],
        'name': 'league',
        'is_public': True
    }
    channel_2 = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param_2).json()
    
    message_send_program_2 = {
        'token': auth_user_2['token'],
        'channel_id': channel_2['channel_id'],
        'message': message_2
    }

    msg_id_2 = requests.post(f"{BASE_URL}/message/send/v1",json = message_send_program_2).json()
 

    message_remove_program_1 = {
        'token': auth_user_1['token'],
        'message_id': msg_id_2['message_id']
    }
    message_remove_program_2 = {
        'token': auth_user_2['token'],
        'message_id': msg_id_1['message_id']
    }

    dm_remove_1 = requests.delete(f"{BASE_URL}/message/remove/v1", json = message_remove_program_1)
    assert dm_remove_1.status_code == 400  
    dm_remove_2 = requests.delete(f"{BASE_URL}/message/remove/v1", json = message_remove_program_2)
    assert dm_remove_2.status_code == 400  

def test_msg_rm_invalid_msg_id_2():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    message_1 = "dsdaada"
    message_2 = "pojno"
    
    register_param_1 = {
        "email": "test@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    auth_user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()
    
    channel_param_1 = {
        'token': auth_user_1['token'],
        'name': 'league',
        'is_public': True
    }
    channel_1 = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param_1).json()
    
    message_send_program_1 = {
        'token': auth_user_1['token'],
        'channel_id': channel_1['channel_id'],
        'message': message_1
    }

    msg_id_1 = requests.post(f"{BASE_URL}/message/send/v1",json = message_send_program_1).json()

    msg_id_1['message_id'] +=99
    
    message_remove_program_1 = {
        'token': auth_user_1['token'],
        'message_id': msg_id_1
    }

    dm_remove_1 = requests.delete(f"{BASE_URL}/message/remove/v1", json = message_remove_program_1)
    assert dm_remove_1.status_code == 400  
    
