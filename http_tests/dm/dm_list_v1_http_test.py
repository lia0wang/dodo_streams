import requests
import pytest
from src import config

BASE_URL = config.url
OK = 200
ACCESS_ERROR = 403

import requests
import pytest
from src import config

BASE_URL = config.url
OK = 200
ACCESS_ERROR = 403

def test_invalid_token():
    '''
    Checking if the function can identify incorrect tokens
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
    
    auth_user_json = {
        "email": "shifanchen@gmail.com",
        "password": "djkadldjsa21",
        "name_first": "shifan",
        "name_last": "chen"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = auth_user_json).json()

    user_1_json = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_1_json).json()

    user_2_json = {
        "email": "z5306312@gmail.com",
        "password": "LeonLiao123",
        "name_first": "Leon",
        "name_last": "Liao"
    }
    user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_2_json).json()

    dm_create_json = {
        "token": auth_user["token"],
        "u_ids": [user_1["auth_user_id"], user_2["auth_user_id"]]
    }

    requests.post(f"{BASE_URL}/dm/create/v1", json = dm_create_json).json()
    
    token_params = {
        "token": invalid['token'] # Invalid token
    }
    
    response = requests.get(f"{BASE_URL}/dm/list/v1", params = token_params)
    
    assert response.status_code == ACCESS_ERROR

def test_no_dms():
    '''
    Checking if function recognises when there's no dms
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    auth_user_json = {
        "email": "shifanchen@gmail.com",
        "password": "djkadldjsa21",
        "name_first": "shifan",
        "name_last": "chen"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = auth_user_json).json()

    user_1_json = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_1_json).json()

    user_2_json = {
        "email": "z5306312@gmail.com",
        "password": "LeonLiao123",
        "name_first": "Leon",
        "name_last": "Liao"
    }
    user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_2_json).json()

    dm_create_json = {
        "token": auth_user["token"],
        "u_ids": [user_1["auth_user_id"]]
    }
    
    requests.post(f"{BASE_URL}/dm/create/v1", json = dm_create_json).json()
    
    token_params = {
        "token": user_2["token"]
    }
    
    response = requests.get(f"{BASE_URL}/dm/list/v1", params = token_params)
    dm_list = response.json()
    
    assert response.status_code == OK
    assert dm_list == {"dms": []}

def test_basic():
    '''
    Checking if the output is correct
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    auth_user_json = {
        "email": "shifanchen@gmail.com",
        "password": "djkadldjsa21",
        "name_first": "shifan",
        "name_last": "chen"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = auth_user_json).json()

    user_1_json = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_1_json).json()

    dm_create_json = {
        "token": auth_user["token"],
        "u_ids": [user_1["auth_user_id"]]
    }

    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_create_json).json()
    
    token_params = {
        "token": auth_user["token"]
    }
    
    response = requests.get(f"{BASE_URL}/dm/list/v1", params = token_params)
    dm_list = response.json()
    
    assert response.status_code == OK
    assert dm_list == {"dms": [{'dm_id': dm['dm_id'], 'name': "hopefulboyyy, shifanchen"}]}

def test_multiple_dms():
    '''
    Checking if multiple dms are returned correctly
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    auth_user_json = {
        "email": "shifanchen@gmail.com",
        "password": "djkadldjsa21",
        "name_first": "shifan",
        "name_last": "chen"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = auth_user_json).json()

    user_1_json = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_1_json).json()

    user_2_json = {
        "email": "z5306312@gmail.com",
        "password": "LeonLiao123",
        "name_first": "Leon",
        "name_last": "Liao"
    }
    user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_2_json).json()

    dm_create_1_json = {
        "token": auth_user["token"],
        "u_ids": [user_1["auth_user_id"]]
    }
    
    dm_1 = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_create_1_json).json()
    
    dm_create_2_json = {
        "token": auth_user["token"],
        "u_ids":[user_2["auth_user_id"]]
    }

    dm_2 = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_create_2_json).json()
    
    token_params = {
        "token": auth_user["token"]
    }
    
    response = requests.get(f"{BASE_URL}/dm/list/v1", params = token_params)
    dm_list = response.json()
    
    assert response.status_code == OK
    assert dm_list == {"dms": [{'dm_id': dm_1['dm_id'], 'name': "hopefulboyyy, shifanchen"}, 
                       {'dm_id': dm_2['dm_id'], 'name': "leonliao, shifanchen"}]}
