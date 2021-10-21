import pytest
import requests
import pytest
import json
from src import config

BASE_URL = config.url

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

    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_create_param).json()

    dm_details_param = {
        "token": auth_user["token"], 
        "dm_id": dm["dm_id"]
    }

    get_request = requests.get(f"{BASE_URL}/dm/details/v1", json = dm_details_param)
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

    assert request_data['members'][2]['u_id'] == user_2["auth_user_id"]
    assert request_data['members'][2]['email'] == "z5306312@gmail.com"
    assert request_data['members'][2]['name_first'] == "Leon"
    assert request_data['members'][2]['name_last'] == "Liao"
    assert request_data['members'][2]['handle_str'] == "leonliao"  

def test_http_invalid_dm_id():
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

    dm_create_param = {
        "token": auth_user["token"],
        "u_ids": [user_1["auth_user_id"]]
    }

    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_create_param).json()

    dm_details_param = {
        "token": auth_user["token"], 
        "dm_id": dm["dm_id"] + 1
    }

    get_request = requests.get(f"{BASE_URL}/dm/details/v1", json = dm_details_param)
    assert get_request.status_code == 400

def test_http_not_member():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param = {
        "email": "shifanchen@gmail.com",
        "password": "djkadldjsa21",
        "name_first": "shifan",
        "name_last": "chen"
    }
    register_param_1 = {
        "email": "wangliao@gmail.com",
        "password": "Hope11037",
        "name_first": "ang",
        "name_last": "angliao"
    }
    register_param_2 = {
        "email": "z5306312@gmail.com",
        "password": "LeonLiao123",
        "name_first": "Leon",
        "name_last": "Liao"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()
    user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()

    dm_create_param = {
        "token": auth_user["token"],
        "u_ids": [user_1["auth_user_id"]]
    }

    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_create_param).json()

    # 2nd registered user requests details of channel created by auth user without joining
    dm_details_param = {
        "token": user_2["token"], 
        "dm_id": dm["dm_id"]
    }

    get_request = requests.get(f"{BASE_URL}/dm/details/v1", json = dm_details_param)
    assert get_request.status_code == 403



def test_http_details_multiple_dms():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    register_param_1 = {
        "email": "11037@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boy"
    }
    register_param_2 = {
        "email": "MotherReggie@gmail.com",
        "password": "localizeM3",
        "name_first": "Leon",
        "name_last": "Liao"
    }
    register_param_3 = {
        "email": "groundpound@gmail.com",
        "password": "UltraPowerful",
        "name_first": "shifan",
        "name_last": "chen"
    }

    register_return1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1)
    register_return1 = register_return1.json()
    register_return2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2)
    register_return2 = register_return2.json()
    register_return3 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_3)
    register_return3 = register_return3.json()

    dm_create_param1 = {
        "token": register_return1["token"],
        "u_ids": register_return2["auth_user_id"]
    }

    dm_create_param2 = {
        "token": register_return2["token"],
        "u_ids": register_return3["auth_user_id"]
    }

    dm_create_return1 = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_create_param1)
    dm_create_return1 = dm_create_return1.json()
    dm_create_return2 = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_create_param2)
    dm_create_return2 = dm_create_return2.json()

    dm_details_param1 = {
        "token": register_return1["token"], 
        "dm_id": dm_create_return1["dm_id"]
    }

    dm_details_param2 = {
        "token": register_return3["token"], 
        "dm_id": dm_create_return2["dm_id"]
    }

    get_request1 = requests.get(f"{BASE_URL}/dm/details/v1", json = dm_details_param1)
    request_data1 = get_request1.json()
    get_request2 = requests.get(f"{BASE_URL}/dm/details/v1", json = dm_details_param2)
    request_data2 = get_request2.json()

    # check details of first dm
    assert request_data1["name"] == 'hopefulboyyy, leonliao'

    assert request_data1["members"][0]["u_id"] == register_return1["auth_user_id"]
    assert request_data1["members"][0]["email"] == "11037@gmail.com"
    assert request_data1["members"][0]["name_first"] == "Hopeful"
    assert request_data1["members"][0]["name_last"] == "Boy"
    assert request_data1["members"][0]["handle_str"] == "hopefulboy"    

    assert request_data1["members"][1]["u_id"] == register_return2["auth_user_id"]
    assert request_data1["members"][1]["email"] == "MotherReggie@gmail.com"
    assert request_data1["members"][1]["name_first"] == "Leon"
    assert request_data1["members"][1]["name_last"] == "Liao"
    assert request_data1["members"][1]["handle_str"] == "leonliao"    

    # check details of 2nd dm
    assert request_data2["name"] == "leonliao, shifanchen"

    assert request_data2["members"][0]["u_id"] == register_return2["auth_user_id"]
    assert request_data2["members"][0]["email"] == "MotherReggie@gmail.com"
    assert request_data2["members"][0]["name_first"] == "Leon"
    assert request_data2["members"][0]["name_last"] == "Liao"
    assert request_data2["members"][0]["handle_str"] == "leonliao"  

    assert request_data2["members"][1]["u_id"] == register_return3["auth_user_id"]
    assert request_data2["members"][1]["email"] == "groundpound@gmail.com"
    assert request_data2["members"][1]["name_first"] == "shifan"
    assert request_data2["members"][1]["name_last"] == "chen"
    assert request_data2["members"][1]["handle_str"] == "shifanchen"  