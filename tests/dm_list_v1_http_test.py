import requests
import pytest
from src import config

BASE_URL = config.url

def test_invalid_token():
    '''
    Checking if the function can identify incorrect tokens
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param = {
        "email": "shifanchen@gmail.com",
        "password": "djkadldjsa21",
        "name_first": "shifan",
        "name_last": "chen"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    register_param_1 = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    register_param_2 = {
        "email": "z5306312@gmail.com",
        "password": "LeonLiao123",
        "name_first": "Leon",
        "name_last": "Liao"
    }
    user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()

    dm_create_param = {
        "token": auth_user["token"],
        "u_ids": [user_1["auth_user_id"], user_2["auth_user_id"]]
    }

    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_create_param).json()
    
    token = {
        "token": auth_user["token"] + "1" # Invalid token
    }
    
    response = requests.get(f"{BASE_URL}/dm/list/v1", json = token)
    
    assert response.status_code != 200

    
def test_basic():
    '''
    Checking if the output is correct
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param = {
        "email": "shifanchen@gmail.com",
        "password": "djkadldjsa21",
        "name_first": "shifan",
        "name_last": "chen"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    register_param_1 = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    dm_create_param = {
        "token": auth_user["token"],
        "u_ids": [user_1["auth_user_id"]]
    }

    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_create_param).json()
    
    token = {
        "token": auth_user["token"]
    }
    
    response = requests.get(f"{BASE_URL}/dm/list/v1", json = token)
    dm_list = response.json()
    
    assert response.status_code == 200
    assert dm_list == [{'dm_id': dm['dm_id'], 'dm_name': "shifanchen, hopefulboyyy"}]

def test_multiple_dms():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param = {
        "email": "shifanchen@gmail.com",
        "password": "djkadldjsa21",
        "name_first": "shifan",
        "name_last": "chen"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    register_param_1 = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    register_param_2 = {
        "email": "z5306312@gmail.com",
        "password": "LeonLiao123",
        "name_first": "Leon",
        "name_last": "Liao"
    }
    user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()

    dm_create_param_1 = {
        "token": auth_user["token"],
        "u_ids": [user_1["auth_user_id"]]
    }
    
    dm_1 = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_create_param_1).json()
    
    dm_create_param_2 = {
        "token": auth_user["token"],
        "u_ids":[user_2["auth_user_id"]]
    }

    dm_2 = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_create_param_2).json()
    
    token = {
        "token": auth_user["token"]
    }
    
    response = requests.get(f"{BASE_URL}/dm/list/v1", json = token)
    dm_list = response.json()
    
    assert response.status_code == 200
    assert dm_list == [{'dm_id': dm_1['dm_id'], 'dm_name': "shifanchen, hopefulboyyy"}, 
                       {'dm_id': dm_2['dm_id'], 'dm_name': "shifachen, leonliao"}]