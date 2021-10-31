
import requests
import pytest
import json
from src.message import message_send_v1, message_edit_v1, message_remove_v1

from src import config

BASE_URL = config.url

def test_msg_edit_normal():
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
    msg2 = "edit"
    target_message = requests.post(f"{BASE_URL}/message/send/v1",json = message_send_program)
    assert target_message.status_code == 200
    target_message = target_message.json()
    message_edit_program = {
        'token': auth_user['token'],
        'message_id': target_message['message_id'],
        'message': msg2
    }

    response = requests.put(f"{BASE_URL}/message/edit/v1",json = message_edit_program)

    assert response.status_code == 200
    

def test_cannot_remove_deleted_message_http():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    message_1 = "dsdaada"
    
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

    message_remove_program_1 = {
        'token': auth_user_1['token'],
        'message_id': msg_id_1['message_id']
    }

    message_2 = "jhndgbf"
    
    message_edit_program_1 = {
        'token': auth_user_1['token'],
        'message_id': msg_id_1['message_id'],
        'message': message_2
    }  

    msg_remove_1 = requests.delete(f"{BASE_URL}/message/remove/v1", json = message_remove_program_1)
    assert msg_remove_1.status_code == 200  
    msg_edit_1 = requests.put(f"{BASE_URL}/message/edit/v1", json = message_edit_program_1)
    assert msg_edit_1.status_code == 400   

def test_msg_edit_invalid_input():
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
    msg2 = "1"*1001
    target_message = requests.post(f"{BASE_URL}/message/send/v1",json = message_send_program)
    assert target_message.status_code == 200
    target_message = target_message.json()
    message_edit_program = {
        'token': auth_user['token'],
        'message_id': target_message['message_id'],
        'message': msg2
    }

    response = requests.put(f"{BASE_URL}/message/edit/v1",json = message_edit_program)

    assert response.status_code == 400

def test_global_owner_can_edit_members_message_channel_http():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()
    
    channel_param = {
        'token': user_1['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json()


    register_param_2 = {
        "email": "test2@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Smith"
    }
    user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()


    channel_invites_param = {
        'token': user_1['token'],
        'channel_id': channel['channel_id'],
        'u_id': user_2['auth_user_id']
    }
    
    invite= requests.post(f"{BASE_URL}/channel/invite/v2", json = channel_invites_param)

    msg = "test"
    message_send_program = {
        'token': user_2['token'],
        'channel_id': channel['channel_id'],
        'message': msg
    }
    
    target_message = requests.post(f"{BASE_URL}/message/send/v1",json = message_send_program)
    assert target_message.status_code == 200
    target_message = target_message.json()

    msg2 = "edit"
    message_edit_program = {
        'token': user_1['token'],
        'message_id': target_message['message_id'],
        'message': msg2
    }

    response = requests.put(f"{BASE_URL}/message/edit/v1",json = message_edit_program)

    assert response.status_code == 200
