import requests
import pytest
import json

from src import config

BASE_URL = config.url

def test_dm_normal():
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
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_param).json()
    
    msg = "test"

    dm_send_program = {
        'token': auth_user['token'],
        'dm_id': dm['dm_id'],
        'message': msg
    }
    response = requests.post(f"{BASE_URL}/message/senddm/v1", json = dm_send_program)
    assert response.status_code == 200    

def test_dm_invalid_length_too_short():
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
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_param).json()
    
    invalid_msg = ''

    dm_send_program = {
        'token': auth_user['token'],
        'dm_id': dm['dm_id'],
        'message': invalid_msg
    }
    response = requests.post(f"{BASE_URL}/message/senddm/v1", json = dm_send_program)
    assert response.status_code == 400

def test_dm_invalid_length_too_long():
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
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_param).json()
    
    invalid_msg = ',' * 1001

    dm_send_program = {
        'token': auth_user['token'],
        'dm_id': dm['dm_id'],
        'message': invalid_msg
    }
    response = requests.post(f"{BASE_URL}/message/senddm/v1", json = dm_send_program)
    assert response.status_code == 400

### AccessError

def test_dm__invalid_auth_id_http():
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

    register_param_3 = {
        "email": "test3@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Johnson"
    }
    user3 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_3).json()


    u_id2 = user2['auth_user_id']
    u_id3 = user3['auth_user_id']


    u_ids = [u_id2,u_id3]
    
    dm_param = {
        'token': user1['token'],
        'u_ids': u_ids
    }
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_param).json()
    
    msg = "test"

    dm_send_program = {
        'token': user2['token'],
        'dm_id': dm['dm_id'],
        'message': msg
    }

    response = requests.post(f"{BASE_URL}/message/senddm/v1",json = dm_send_program)
    assert response.status_code == 403
    
    
