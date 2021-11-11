import requests
import pytest

from src import config

BASE_URL = config.url


def test_http_setemail_once():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    register_param_1 = {
        "email": "11037@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boy"
    }

    register_return1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1)
    register_return1 = register_return1.json()
    ch_create_param = {
        "token": register_return1["token"],
        "name": "TheRealMonsters",
        "is_public": True
    }
    create_return = requests.post(f"{BASE_URL}/channels/create/v2", json = ch_create_param)
    create_return = create_return.json()
    setemail_param = {
        "token": register_return1["token"],
        "email": "standuser@gmail.com"
    }
    requests.put(f"{BASE_URL}/user/profile/setemail/v1", json = setemail_param)
    profile_param = {
        "u_id": register_return1["auth_user_id"],
        "token": register_return1["token"]
    }
    profile_return = requests.get(f"{BASE_URL}/user/profile/v1", params = profile_param).json()

    ch_details_param = {
        "token": register_return1["token"], 
        "channel_id": create_return["channel_id"]
    }
    request_data = requests.get(f"{BASE_URL}/channel/details/v2", params = ch_details_param).json()

    assert profile_return["user"]['email'] == "standuser@gmail.com"
    assert request_data["owner_members"][0]["email"] == "standuser@gmail.com"
    assert request_data["all_members"][0]["email"] == "standuser@gmail.com"


def test_http_setemail_twice():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    register_param_1 = {
        "email": "11037@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boy"
    }

    register_return1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1)
    register_return1 = register_return1.json()
    ch_create_param = {
        "token": register_return1["token"],
        "name": "TheRealMonsters",
        "is_public": True
    }
    create_return = requests.post(f"{BASE_URL}/channels/create/v2", json = ch_create_param)
    create_return = create_return.json()
    setemail_param = {
        "token": register_return1["token"],
        "email": "standuser@gmail.com"
    }
    requests.put(f"{BASE_URL}/user/profile/setemail/v1", json = setemail_param)
    profile_param = {
        "u_id": register_return1["auth_user_id"],
        "token": register_return1["token"]
    }
    profile_return = requests.get(f"{BASE_URL}/user/profile/v1", params = profile_param).json()

    ch_details_param = {
        "token": register_return1["token"], 
        "channel_id": create_return["channel_id"]
    }
    request_data = requests.get(f"{BASE_URL}/channel/details/v2", params = ch_details_param).json()

    assert profile_return["user"]['email'] == "standuser@gmail.com"
    assert request_data["owner_members"][0]["email"] == "standuser@gmail.com"
    assert request_data["all_members"][0]["email"] == "standuser@gmail.com"

    setemail_param = {
        "token": register_return1["token"],
        "email": "eekumbokum@gmail.com"
    }
    requests.put(f"{BASE_URL}/user/profile/setemail/v1", json = setemail_param)

    request_data = requests.get(f"{BASE_URL}/channel/details/v2", params = ch_details_param).json()
    profile_return = requests.get(f"{BASE_URL}/user/profile/v1", params = profile_param).json()

    assert profile_return["user"]['email'] == "eekumbokum@gmail.com"
    assert request_data["owner_members"][0]["email"] == "eekumbokum@gmail.com"
    assert request_data["all_members"][0]["email"] == "eekumbokum@gmail.com"

def test_http_setemail_different_users():
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
        "name_first": "Mother",
        "name_last": "Reggie"
    }
    register_return1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1)
    register_return1 = register_return1.json()
    register_return2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2)
    register_return2 = register_return2.json()
    register_return3 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_3)
    register_return3 = register_return3.json()
    setemail_param1 = {
        "token": register_return1["token"],
        "email": "CrazyDiamond@gmail.com"
    }
    setemail_param2 = {
        "token": register_return2["token"],
        "email": "TheHand@gmail.com"
    }
    setemail_param3 = {
        "token": register_return3["token"],
        "email": "Echoes@gmail.com"
    }
    requests.put(f"{BASE_URL}/user/profile/setemail/v1", json = setemail_param1)
    requests.put(f"{BASE_URL}/user/profile/setemail/v1", json = setemail_param2)
    requests.put(f"{BASE_URL}/user/profile/setemail/v1", json = setemail_param3)
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

    assert profile_return1["user"]['email'] == "CrazyDiamond@gmail.com"
    assert profile_return2["user"]['email'] == "TheHand@gmail.com"
    assert profile_return3["user"]['email'] == "Echoes@gmail.com"
    

def test_http_channel_member_setemail():
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
        "name_first": "Mario",
        "name_last": "Pratt"
    }

    register_return1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1)
    register_return1 = register_return1.json()
    register_return2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2)
    register_return2 = register_return2.json()
    register_return3 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_3)
    register_return3 = register_return3.json()

    ch_create_param = {
        "token": register_return1["token"],
        "name": "TheRealMonsters",
        "is_public": True
    }
    create_return = requests.post(f"{BASE_URL}/channels/create/v2", json = ch_create_param)
    create_return = create_return.json()
    ch_join_param = {
        "token": register_return2["token"], 
        "channel_id": create_return["channel_id"]
    }
    ch_join_param2 = {
        "token": register_return3["token"], 
        "channel_id": create_return["channel_id"]
    }
    requests.post(f"{BASE_URL}/channel/join/v2", json = ch_join_param)
    requests.post(f"{BASE_URL}/channel/join/v2", json = ch_join_param2)
    setemail_param1 = {
        "token": register_return2["token"],
        "email": "TheHand@gmail.com"
    }
    requests.put(f"{BASE_URL}/user/profile/setemail/v1", json = setemail_param1)

    get_request = requests.get(f"{BASE_URL}/channel/details/v2", params = ch_join_param)
    request_data = get_request.json()

    assert request_data["all_members"][1]["email"] == "TheHand@gmail.com"

def test_http_invalid_setemail():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    register_param_1 = {
        "email": "11037@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boy"
    }

    register_return1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1)
    register_return1 = register_return1.json()

    setemail_param1 = {
        "token": register_return1["token"],
        "email": "11037.666@gmail&.com"
    }
    request_data = requests.put(f"{BASE_URL}/user/profile/setemail/v1", json = setemail_param1)
    assert request_data.status_code == 400
    setemail_param1 = {
        "token": register_return1["token"],
        "email": "@xample.com"
    }
    request_data = requests.put(f"{BASE_URL}/user/profile/setemail/v1", json = setemail_param1)
    assert request_data.status_code == 400



def test_http_invalid_setemail_duplicate():
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
        "name_first": "Mother",
        "name_last": "Reggie"
    }
    register_return1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1)
    register_return1 = register_return1.json()
    register_return2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2)
    register_return2 = register_return2.json()
    register_return3 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_3)
    register_return3 = register_return3.json()

    setemail_param1 = {
        "token": register_return2["token"],
        "email": "11037@gmail.com"
    }
    request_data = requests.put(f"{BASE_URL}/user/profile/setemail/v1", json = setemail_param1)
    assert request_data.status_code == 400
    setemail_param2 = {
        "token": register_return3["token"],
        "email": "MotherReggie@gmail.com"
    }
    request_data = requests.put(f"{BASE_URL}/user/profile/setemail/v1", json = setemail_param2)
    assert request_data.status_code == 400
