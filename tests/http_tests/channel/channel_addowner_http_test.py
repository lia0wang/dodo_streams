import re
import requests
import pytest

from src import config
from src.channel import channel_addowner_v1

BASE_URL = config.url

def test_invalid_channel_id():
    '''
    Test when the channel_id is invalid
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})

    register_param = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    owner = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    channel_param = {
        'token': owner['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json() 

    register_param_1 = {
        "email": "liaowang@gmail.com",
        "password": "liaowang0207",
        "name_first": "wang",
        "name_last": "liao"
    }
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    channel_join_param = {
        'token': user['token'],
        'channel_id': channel['channel_id']
    }
    requests.post(f"{BASE_URL}/channel/join/v2", json = channel_join_param)

    channel_addowner_param = {
        'token': owner['token'],
        'channel_id': channel['channel_id'] + 999,
        'u_id': user['auth_user_id']
    }
    response = requests.post(f"{BASE_URL}/channel/addowner/v1", json = channel_addowner_param)

    assert response.status_code == 400

def test_invalid_user_id():
    '''
    Test when the u_id is invalid
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})

    register_param = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    owner = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    channel_param = {
        'token': owner['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json() 

    register_param_1 = {
        "email": "liaowang@gmail.com",
        "password": "liaowang0207",
        "name_first": "wang",
        "name_last": "liao"
    }
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    channel_join_param = {
        'token': user['token'],
        'channel_id': channel['channel_id']
    }
    requests.post(f"{BASE_URL}/channel/join/v2", json = channel_join_param)

    channel_addowner_param = {
        'token': owner['token'],
        'channel_id': channel['channel_id'],
        'u_id': user['auth_user_id'] + 999
    }
    response = requests.post(f"{BASE_URL}/channel/addowner/v1", json = channel_addowner_param)

    assert response.status_code == 400

def test_none_exist_user():
    '''
    Test when the user is not a member of the channel
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})

    register_param = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    owner = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    channel_param = {
        'token': owner['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json() 

    register_param_1 = {
        "email": "liaowang@gmail.com",
        "password": "liaowang0207",
        "name_first": "wang",
        "name_last": "liao"
    }
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    channel_addowner_param = {
        'token': owner['token'],
        'channel_id': channel['channel_id'],
        'u_id': user['auth_user_id']
    }
    response = requests.post(f"{BASE_URL}/channel/addowner/v1", json = channel_addowner_param)

    assert response.status_code == 400

def test_add_exist_owner():
    '''
    Test when the user is already a owner of the chanenl
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})

    register_param = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    owner = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    channel_param = {
        'token': owner['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json() 

    register_param_1 = {
        "email": "liaowang@gmail.com",
        "password": "liaowang0207",
        "name_first": "wang",
        "name_last": "liao"
    }
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    channel_join_param = {
        'token': user['token'],
        'channel_id': channel['channel_id']
    }
    requests.post(f"{BASE_URL}/channel/join/v2", json = channel_join_param)

    channel_addowner_param = {
        'token': owner['token'],
        'channel_id': channel['channel_id'],
        'u_id': user['auth_user_id']
    }
    response1 = requests.post(f"{BASE_URL}/channel/addowner/v1", json = channel_addowner_param)

    assert response1.status_code == 200

    channel_addowner_param = {
        'token': owner['token'],
        'channel_id': channel['channel_id'],
        'u_id': user['auth_user_id']
    }
    response2 = requests.post(f"{BASE_URL}/channel/addowner/v1", json = channel_addowner_param)

    assert response2.status_code == 400

def test_no_permission():
    '''
    Test when the auth user has no owner permission
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    register_param = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    global_owner = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    channel_param = {
        'token': global_owner['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json() 

    register_param_1 = {
        "email": "liaowang@gmail.com",
        "password": "liaowang0207",
        "name_first": "wang",
        "name_last": "liao"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    register_param_2 = {
        "email": "chenshifan@gmail.com",
        "password": "chenshifan2341",
        "name_first": "shifan",
        "name_last": "chen"
    }
    user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()

    channel_join_param_1 = {
        'token': user_1['token'],
        'channel_id': channel['channel_id']
    }
    requests.post(f"{BASE_URL}/channel/join/v2", json = channel_join_param_1)

    channel_join_param_2 = {
        'token': user_2['token'],
        'channel_id': channel['channel_id']
    }
    requests.post(f"{BASE_URL}/channel/join/v2", json = channel_join_param_2)

    channel_addowner_param = {
        'token': user_1['token'],
        'channel_id': channel['channel_id'],
        'u_id': user_2['auth_user_id']
    }
    response = requests.post(f"{BASE_URL}/channel/addowner/v1", json = channel_addowner_param)

    assert response.status_code == 403

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
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_json).json()
    
    channel_addowner_param = {
        'token': invalid['token'],
        'channel_id': channel['channel_id'],
        'u_id': user['auth_user_id']
    }
    response = requests.post(f"{BASE_URL}/channel/addowner/v1", json = channel_addowner_param)

    assert response.status_code == 403