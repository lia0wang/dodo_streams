import requests

from src.message import message_send_v1, message_senddm_v1

from src import config

BASE_URL = config.url

def invalid_length_too_long():
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

def invalid_length_too_short():
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
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param)
    
    invalid_msg = ''

    message_send_program = {
        'token': auth_user['token'],
        'channel_id': channel['channel_id'],
        'message': invalid_msg
    }
    response = requests.post(f"{BASE_URL}/message/send/v1", json = message_send_program)
    assert response.status_code == 400

def invalid_length_dm_too_short():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    register_param_2 = {
        "email": "test2@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Smith"
    }
    user1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()
    
    register_param_3 = {
        "email": "test3@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Johnson"
    }
    user2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_3).json()

    u_id1 = user1['auth_user_id']
    u_id2 = user2['auth_user_id']
    u_ids = [u_id1,u_id2]

    dm_param = {
        'token': auth_user['token'],
        'u_ids': u_ids
    }
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_param)
    
    invalid_msg = ''

    dm_send_program = {
        'token': auth_user['token'],
        'dm_id': dm['dm_id'],
        'message': invalid_msg
    }
    response = requests.post(f"{BASE_URL}/message/senddm/v1", json = dm_send_program)
    assert response.status_code == 400


def invalid_length_dm_too_long():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    register_param_2 = {
        "email": "test2@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Smith"
    }
    user1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()
    
    register_param_3 = {
        "email": "test3@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Johnson"
    }
    user2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_3).json()

    u_id1 = user1['auth_user_id']
    u_id2 = user2['auth_user_id']
    u_ids = [u_id1,u_id2]

    dm_param = {
        'token': auth_user['token'],
        'u_ids': u_ids
    }
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_param)
    
    invalid_msg = ',' * 1000

    dm_send_program = {
        'token': auth_user['token'],
        'dm_id': dm['dm_id'],
        'message': invalid_msg
    }
    response = requests.post(f"{BASE_URL}/message/senddm/v1", json = dm_send_program)
    assert response.status_code == 400
