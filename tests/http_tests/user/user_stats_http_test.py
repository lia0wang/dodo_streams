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
    assert user_1_stats['involvement_rate'][0] == 0

def test_user_basic_dms_http():
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
    
    assert response.status_code == 200
    assert dm_list == {"dms": [{'dm_id': dm['dm_id'], 'name': "hopefulboyyy, shifanchen"}]}
    
    user_1_stats = requests.get(f"{BASE_URL}/user/stats/v1", json = token_params)
    assert user_1_stats.status_code == 200
    user_1_stats = user_1_stats.json()

    assert user_1_stats['involvement_rate'][0] == 1
    
