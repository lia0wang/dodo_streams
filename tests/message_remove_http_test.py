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

    msg_1 = requests.post(f"{BASE_URL}/message/send/v1",json = message_send_program_1)

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

    msg_2 = requests.post(f"{BASE_URL}/message/send/v1",json = message_send_program_2)

    message_remove_program_1 = {
        'token': auth_user_1['token'],
        'channel_id': channel_2['channel_id'],
    }
    message_remove_program_2 = {
        'token': auth_user_2['token'],
        'channel_id': channel_1['channel_id'],
    }

    reponse_1 = requests.post(f"{BASE_URL}/message/remove/v2", json = message_remove_program_1)
    reponse_1 = requests.post(f"{BASE_URL}/message/remove/v2", json = message_remove_program_2)


    
