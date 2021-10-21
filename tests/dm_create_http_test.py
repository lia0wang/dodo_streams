import requests

from src.dm import dm_create_v1
from src import config

BASE_URL = config.url


def test_http_dm_create_basic():
    '''
    Test if the http dm/create/v1 function working properly
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

    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_create_param)

    assert dm.status_code == 200
    assert dm.json() == {'dm_id': 1, 'dm_name': 'hopefulboyyy, leonliao, shifanchen'} 

def test_http_invalid_user_id():
    '''
    Test when any of the user ids is invalid
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
        "u_ids": [user_1["auth_user_id"] + 999, user_2["auth_user_id"]] # user1 id is invalid whi=ile user2 id is valid
    }

    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_create_param)

    assert dm.status_code == 400

def test_http_one_member():
    '''
    Test when the creator is also the user who is invited to the dm.
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})

    register_param = {
        "email": "shifanchen@gmail.com",
        "password": "djkadldjsa21",
        "name_first": "shifan",
        "name_last": "chen"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    dm_create_param = {
        "token": auth_user["token"],
        "u_ids": [auth_user["auth_user_id"]]
    }

    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_create_param)

    assert dm.status_code == 403

def test_http_invalid_auth_user_token():
    '''
    Test when any of the auth user token is invalid
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
        "token": auth_user["token"] + "woaini",
        "u_ids": [user_1["auth_user_id"], user_2["auth_user_id"]] # user1 id is invalid whi=ile user2 id is valid
    }

    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_create_param)

    assert dm.status_code != 200
