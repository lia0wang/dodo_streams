import requests
import pytest
from src import config

BASE_URL = config.url

# test multiple profiles
def test_http_multiple_profile():
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
        "name_first": "Mother",
        "name_last": "Reggie"
    }
    register_param_3 = {
        "email": "groundpound@gmail.com",
        "password": "UltraPowerful",
        "name_first": "MOther",
        "name_last": "ReGgie"
    }

    register_return1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1)
    register_return1 = register_return1.json()
    register_return2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2)
    register_return2 = register_return2.json()
    register_return3 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_3)
    register_return3 = register_return3.json()
    profile_param1 = {
        "u_id": register_return1["auth_user_id"],
        "token": register_return1["token"]
    }
    profile_param2 = {
        "u_id": register_return2["auth_user_id"],
        "token": register_return2["token"]
    }
    profile_param3 = {
        "u_id": register_return3["auth_user_id"],
        "token": register_return3["token"]
    }
    profile_return1 = requests.get(f"{BASE_URL}/user/profile/v1", params = profile_param1).json()
    profile_return2 = requests.get(f"{BASE_URL}/user/profile/v1", params = profile_param2).json()
    profile_return3 = requests.get(f"{BASE_URL}/user/profile/v1", params = profile_param3).json()

    assert profile_return1['u_id'] == register_return1["auth_user_id"]
    assert profile_return1['email'] == "11037@gmail.com"
    assert profile_return1['name_first'] == "Hopeful"
    assert profile_return1['name_last'] == "Boy"
    assert profile_return1['handle_str'] == "hopefulboy"

    assert profile_return2['u_id'] == register_return2["auth_user_id"]
    assert profile_return2['email'] == "MotherReggie@gmail.com"
    assert profile_return2['name_first'] == "Mother"
    assert profile_return2['name_last'] == "Reggie"
    assert profile_return2['handle_str'] == "motherreggie"

    assert profile_return3['u_id'] == register_return3["auth_user_id"]
    assert profile_return3['email'] == "groundpound@gmail.com"
    assert profile_return3['name_first'] == "MOther"
    assert profile_return3['name_last'] == "ReGgie"
    assert profile_return3['handle_str'] == "motherreggie0"
    
# test only existing profile
def test_http_only_profile():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    register_param_1 = {
        "email": "11037@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boy"
    }
    register_return1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1)
    register_return1 = register_return1.json()
    profile_param1 = {
        "u_id": register_return1["auth_user_id"],
        "token": register_return1["token"]
    }
    profile_return1 = requests.get(f"{BASE_URL}/user/profile/v1", params = profile_param1).json()

    assert profile_return1['u_id'] == register_return1["auth_user_id"]
    assert profile_return1['email'] == "11037@gmail.com"
    assert profile_return1['name_first'] == "Hopeful"
    assert profile_return1['name_last'] == "Boy"
    assert profile_return1['handle_str'] == "hopefulboy"

# testing 'u_id does not refer to existing user' error
def test_http_profile_u_id_invlaid():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    register_param_1 = {
        "email": "11037@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boy"
    }
    register_return1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1)
    register_return1 = register_return1.json()
    profile_param1 = {
        "u_id": register_return1["auth_user_id"] + 1,
        "token": register_return1["token"]
    }
    profile_return = requests.get(f"{BASE_URL}/user/profile/v1", params = profile_param1)
    assert profile_return.status_code == 400