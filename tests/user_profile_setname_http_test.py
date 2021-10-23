import requests
import pytest
from src import config

BASE_URL = config.url

def test_http_setname_once():
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
    setname_param = {
        "token": register_return1["token"],
        "name_first": "new",
        "name_last": "name"
    }
    requests.put(f"{BASE_URL}/user/profile/setname/v1", json = setname_param)
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

    assert profile_return['name_first'] == "new"
    assert profile_return['name_last'] == "name"

    assert request_data["owner_members"][0]["name_first"] == "new"
    assert request_data["owner_members"][0]["name_last"] == "name"

    assert request_data["all_members"][0]["name_first"] == "new"
    assert request_data["all_members"][0]["name_last"] == "name"

def test_http_setname_twice():
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
    setname_param = {
        "token": register_return1["token"],
        "name_first": "new",
        "name_last": "name"
    }
    requests.put(f"{BASE_URL}/user/profile/setname/v1", json = setname_param)
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

    assert profile_return['name_first'] == "new"
    assert profile_return['name_last'] == "name"

    assert request_data["owner_members"][0]["name_first"] == "new"
    assert request_data["owner_members"][0]["name_last"] == "name"

    assert request_data["all_members"][0]["name_first"] == "new"
    assert request_data["all_members"][0]["name_last"] == "name"

    setname_param = {
        "token": register_return1["token"],
        "name_first": "even",
        "name_last": "newerName"
    }
    requests.put(f"{BASE_URL}/user/profile/setname/v1", json = setname_param)

    request_data = requests.get(f"{BASE_URL}/channel/details/v2", params = ch_details_param).json()
    profile_return = requests.get(f"{BASE_URL}/user/profile/v1", params = profile_param).json()

    assert profile_return['name_first'] == "even"
    assert profile_return['name_last'] == "newerName"

    assert request_data["owner_members"][0]["name_first"] == "even"
    assert request_data["owner_members"][0]["name_last"] == "newerName"

    assert request_data["all_members"][0]["name_first"] == "even"
    assert request_data["all_members"][0]["name_last"] == "newerName"

def test_http_setname_different_users():
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
    setname_param1 = {
        "token": register_return1["token"],
        "name_first": "new",
        "name_last": "Name"
    }
    setname_param2 = {
        "token": register_return2["token"],
        "name_first": "name",
        "name_last": "new"
    }
    setname_param3 = {
        "token": register_return3["token"],
        "name_first": "evolved",
        "name_last": "newerName"
    }
    requests.put(f"{BASE_URL}/user/profile/setname/v1", json = setname_param1)
    requests.put(f"{BASE_URL}/user/profile/setname/v1", json = setname_param2)
    requests.put(f"{BASE_URL}/user/profile/setname/v1", json = setname_param3)
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

    assert profile_return1['name_first'] == "new"
    assert profile_return1['name_last'] == "Name"

    assert profile_return2['name_first'] == "name"
    assert profile_return2['name_last'] == "new"

    assert profile_return3['name_first'] == "evolved"
    assert profile_return3['name_last'] == "newerName"

def test_http_channel_member_setname():
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
    setname_param1 = {
        "token": register_return2["token"],
        "name_first": "new",
        "name_last": "Name"
    }
    requests.put(f"{BASE_URL}/user/profile/setname/v1", json = setname_param1)

    get_request = requests.get(f"{BASE_URL}/channel/details/v2", params = ch_join_param)
    request_data = get_request.json()

    assert request_data["all_members"][1]["name_first"] == "new"
    assert request_data["all_members"][1]["name_last"] == "Name"

def test_http_invalid_setname_first():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    register_param_1 = {
        "email": "11037@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boy"
    }

    register_return1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1)
    register_return1 = register_return1.json()

    setname_param1 = {
        "token": register_return1["token"],
        "name_first": "",
        "name_last": "Name"
    }
    request_data = requests.put(f"{BASE_URL}/user/profile/setname/v1", json = setname_param1)
    assert request_data.status_code == 400
    setname_param1 = {
        "token": register_return1["token"],
        "name_first": "1",
        "name_last": "Name"
    }
    request_data = requests.put(f"{BASE_URL}/user/profile/setname/v1", json = setname_param1)
    assert request_data.status_code == 200
    # test name_first of 51 characters
    setname_param1 = {
        "token": register_return1["token"],
        "name_first": "MynameisYoshikageKiraIm33yearsoldMyhouseisinthenort",
        "name_last": "Name"
    }
    request_data = requests.put(f"{BASE_URL}/user/profile/setname/v1", json = setname_param1)
    assert request_data.status_code == 400
    # test name_first of 50 characters
    setname_param1 = {
        "token": register_return1["token"],
        "name_first": "MynameisYoshikageKiraIm33yearsoldMyhouseisinthenor",
        "name_last": "Name"
    }
    request_data = requests.put(f"{BASE_URL}/user/profile/setname/v1", json = setname_param1)
    assert request_data.status_code == 200

def test_http_invalid_setname_last():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    register_param_1 = {
        "email": "11037@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boy"
    }

    register_return1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1)
    register_return1 = register_return1.json()

    setname_param1 = {
        "token": register_return1["token"],
        "name_last": "",
        "name_first": "Name"
    }
    request_data = requests.put(f"{BASE_URL}/user/profile/setname/v1", json = setname_param1)
    assert request_data.status_code == 400
    setname_param1 = {
        "token": register_return1["token"],
        "name_last": "1",
        "name_first": "Name"
    }
    request_data = requests.put(f"{BASE_URL}/user/profile/setname/v1", json = setname_param1)
    assert request_data.status_code == 200
    # test name_last of 51 characters
    setname_param1 = {
        "token": register_return1["token"],
        "name_last": "MynameisYoshikageKiraIm33yearsoldMyhouseisinthenort",
        "name_first": "Name"
    }
    request_data = requests.put(f"{BASE_URL}/user/profile/setname/v1", json = setname_param1)
    assert request_data.status_code == 400
    # test name_last of 50 characters
    setname_param1 = {
        "token": register_return1["token"],
        "name_last": "MynameisYoshikageKiraIm33yearsoldMyhouseisinthenor",
        "name_first": "Name"
    }
    request_data = requests.put(f"{BASE_URL}/user/profile/setname/v1", json = setname_param1)
    assert request_data.status_code == 200