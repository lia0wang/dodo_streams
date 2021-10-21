import pytest
import requests
import pytest
import json

BASE_URL = "http://localhost:8080"

 
def test_http_details_multiple_members():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param = {
        "email": "shifanchen@gmail.com",
        "password": "djkadldjsa21",
        "name_first": "shifan",
        "name_last": "chen"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    register_param_1 = {
        "email": "wangliao@gmail.com",
        "password": "Hope11037",
        "name_first": "ang",
        "name_last": "angliao"
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

    dm_param = {
        "token": auth_user["token"], 
        "dm_id": dm["dm_id"]
    }

    get_request = requests.get(f"{BASE_URL}/dm/details/v1", json = dm_param)
    request_data = get_request.json()

    # Checking details of multiple members
    assert request_data['members'][0]['u_id'] == auth_user["auth_user_id"]
    assert request_data['members'][0]['email'] == "shifan@gmail.com"
    assert request_data['members'][0]['name_first'] == "shifan"
    assert request_data['members'][0]['name_last'] == "chen"
    assert request_data['members'][0]['handle_str'] == "shifanchen"    

    assert request_data['members'][1]['u_id'] == user_1["auth_user_id"]
    assert request_data['members'][1]['email'] == "wangliao@gmail.com"
    assert request_data['members'][1]['name_first'] == "ang"
    assert request_data['members'][1]['name_last'] == "liao"
    assert request_data['members'][1]['handle_str'] == "angliao"  

    assert request_data['members'][1]['u_id'] == user_2["auth_user_id"]
    assert request_data['members'][1]['email'] == "z5306312@gmail.com"
    assert request_data['members'][1]['name_first'] == "Leon"
    assert request_data['members'][1]['name_last'] == "Liao"
    assert request_data['members'][1]['handle_str'] == "leonliao"  
