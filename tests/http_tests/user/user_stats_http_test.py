import requests
import pytest
from src import config
BASE_URL = config.url

def test_zero_activities_http():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    user_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_1).json()

    user_stats_request = {
        'token': user_1['token']
        }
    user_1_stats = requests.get(f"{BASE_URL}/user/stats/v1", json = user_stats_request)
    assert user_1_stats.status_code == 200
    user_1_stats = user_1_stats.json()
    print(user_1_stats)

    assert user_1_stats['channels_joined'][0] == 0
    assert user_1_stats['dms_joined'][0] == 0
    assert user_1_stats['messages_sent'][0] == 0
    assert user_1_stats['involvement_rate'][0] == 0

def test_user_basic_dms_http():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    user_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_1).json()

    user_param_2= {
        "email": "test2@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Smith"
    }
    user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_2).json()

    dm_create_json = {
        "token": user_1["token"],
        "u_ids": [user_2["auth_user_id"]]
    }

    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_create_json).json()
    
    token_params = {
        "token": user_1["token"]
    }
    
    response = requests.get(f"{BASE_URL}/dm/list/v1", params = token_params)
    dm_list = response.json()
    
    assert response.status_code == 200
    assert dm_list == {"dms": [{'dm_id': dm['dm_id'], 'name': "agentsmith, johnsmith"}]}
    
    user_1_stats = requests.get(f"{BASE_URL}/user/stats/v1", json = token_params)
    assert user_1_stats.status_code == 200
    user_1_stats = user_1_stats.json()

    assert user_1_stats['channels_joined'][0] == 0
    assert user_1_stats['dms_joined'][0] == 1
    assert user_1_stats['messages_sent'][0] == 0
    assert user_1_stats['involvement_rate'][0] == 1

def test_user_basic_channels_http():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    user_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_1).json()

    channel_param = {
        'token': user_1['token'],
        'name': 'league',
        'is_public': True
    }
    requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json()
    
    token_params = {
        "token": user_1["token"]
    }
    
    
    user_1_stats = requests.get(f"{BASE_URL}/user/stats/v1", json = token_params)
    assert user_1_stats.status_code == 200
    user_1_stats = user_1_stats.json()

    assert user_1_stats['channels_joined'][0] == 1
    assert user_1_stats['dms_joined'][0] == 0
    assert user_1_stats['messages_sent'][0] == 0
    assert user_1_stats['involvement_rate'][0] == 1

def test_user_basic_msgs_http():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    user_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_1).json()

    channel_param = {
        'token': user_1['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json()
    
    msg_1 = 'test'
    
    message_send_program = {
        'token': user_1['token'],
        'channel_id': channel['channel_id'],
        'message': msg_1
    }
    msg_send = requests.post(f"{BASE_URL}/message/send/v1", json = message_send_program)
    assert msg_send.status_code == 200
    
    token_params = {
        "token": user_1["token"]
    }
    
    user_1_stats = requests.get(f"{BASE_URL}/user/stats/v1", json = token_params)
    assert user_1_stats.status_code == 200
    user_1_stats = user_1_stats.json()

    assert user_1_stats['channels_joined'][0] == 1
    assert user_1_stats['dms_joined'][0] == 0
    assert user_1_stats['messages_sent'][0] == 1
    assert user_1_stats['involvement_rate'][0] == 1   

def test_user_basic_dm_msgs_http():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    user_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_1).json()

    user_param_2= {
        "email": "test2@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Smith"
    }
    user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_2).json()

    dm_create_json = {
        "token": user_1["token"],
        "u_ids": [user_2["auth_user_id"]]
    }

    dm_return = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_create_json).json()
    
    token_params = {
        "token": user_1["token"]
    }

    msg_1 = 'test'
    
    dm_send_program = {
        'token': user_1['token'],
        'dm_id': dm_return['dm_id'],
        'message': msg_1
    }
    dm_send = requests.post(f"{BASE_URL}/message/senddm/v1", json = dm_send_program)
    assert dm_send.status_code == 200   
    
    user_1_stats = requests.get(f"{BASE_URL}/user/stats/v1", json = token_params)
    assert user_1_stats.status_code == 200
    user_1_stats = user_1_stats.json()

    assert user_1_stats['channels_joined'][0] == 0
    assert user_1_stats['dms_joined'][0] == 1
    assert user_1_stats['messages_sent'][0] == 1
    assert user_1_stats['involvement_rate'][0] == 1
