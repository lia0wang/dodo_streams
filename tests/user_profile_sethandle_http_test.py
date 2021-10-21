import requests
import pytest

BASE_URL = 'http://localhost:8080'


def test_http_sethandle_once():
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
    sethandle_param = {
        "token": register_return1["token"],
        "handle_str": "newhandle"
    }
    requests.put(f"{BASE_URL}/user/profile/sethandle/v1", json = sethandle_param)
    profile_param = {
        "u_id": register_return1["auth_user_id"],
        "token": register_return1["token"]
    }
    profile_return = requests.get(f"{BASE_URL}/user/profile/v1", json = profile_param).json()

    ch_details_param = {
        "token": register_return1["token"], 
        "channel_id": create_return["channel_id"]
    }
    request_data = requests.get(f"{BASE_URL}/channel/details/v2", json = ch_details_param).json()

    assert profile_return['handle_str'] == "newhandle"
    assert request_data["owner_members"][0]["handle_str"] == "newhandle"
    assert request_data["all_members"][0]["handle_str"] == "newhandle"


def test_http_sethandle_twice():
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
    sethandle_param = {
        "token": register_return1["token"],
        "handle_str": "newhandle"
    }
    requests.put(f"{BASE_URL}/user/profile/sethandle/v1", json = sethandle_param)
    profile_param = {
        "u_id": register_return1["auth_user_id"],
        "token": register_return1["token"]
    }
    profile_return = requests.get(f"{BASE_URL}/user/profile/v1", json = profile_param).json()

    ch_details_param = {
        "token": register_return1["token"], 
        "channel_id": create_return["channel_id"]
    }
    request_data = requests.get(f"{BASE_URL}/channel/details/v2", json = ch_details_param).json()

    assert profile_return['handle_str'] == "newhandle"
    assert request_data["owner_members"][0]["handle_str"] == "newhandle"
    assert request_data["all_members"][0]["handle_str"] == "newhandle"

    sethandle_param = {
        "token": register_return1["token"],
        "handle_str": "newnewhandle"
    }
    requests.put(f"{BASE_URL}/user/profile/sethandle/v1", json = sethandle_param)

    request_data = requests.get(f"{BASE_URL}/channel/details/v2", json = ch_details_param).json()
    profile_return = requests.get(f"{BASE_URL}/user/profile/v1", json = profile_param).json()

    assert profile_return['handle_str'] == "newnewhandle"
    assert request_data["owner_members"][0]["handle_str"] == "newnewhandle"
    assert request_data["all_members"][0]["handle_str"] == "newnewhandle"

def test_http_sethandle_different_users():
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
    sethandle_param1 = {
        "token": register_return1["token"],
        "handle_str": "newhandle1"
    }
    sethandle_param2 = {
        "token": register_return2["token"],
        "handle_str": "newhandle2"
    }
    sethandle_param3 = {
        "token": register_return3["token"],
         "handle_str": "newhandle3"
    }
    requests.put(f"{BASE_URL}/user/profile/sethandle/v1", json = sethandle_param1)
    requests.put(f"{BASE_URL}/user/profile/sethandle/v1", json = sethandle_param2)
    requests.put(f"{BASE_URL}/user/profile/sethandle/v1", json = sethandle_param3)
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
    profile_return1 = requests.get(f"{BASE_URL}/user/profile/v1", json = profile_param1).json()
    profile_return2 = requests.get(f"{BASE_URL}/user/profile/v1", json = profile_param2).json()
    profile_return3 = requests.get(f"{BASE_URL}/user/profile/v1", json = profile_param3).json()

    assert profile_return1['handle_str'] == "newhandle1"
    assert profile_return2['handle_str'] == "newhandle2"
    assert profile_return3['handle_str'] == "newhandle3"
    

def test_http_channel_member_sethandle():
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
    sethandle_param1 = {
        "token": register_return2["token"],
        "handle_str": "newhandle"
    }
    requests.put(f"{BASE_URL}/user/profile/sethandle/v1", json = sethandle_param1)

    get_request = requests.get(f"{BASE_URL}/channel/details/v2", json = ch_join_param)
    request_data = get_request.json()

    assert request_data["all_members"][1]["handle_str"] == "newhandle"

def test_http_invalid_sethandle_char_length():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    register_param_1 = {
        "email": "11037@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boy"
    }

    register_return1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1)
    register_return1 = register_return1.json()
    # testing edge cases: in order, handle strings of 2, 3, 20 and 21 characeters
    sethandle_param1 = {
        "token": register_return1["token"],
        "handle_str": "me"
    }
    request_data = requests.put(f"{BASE_URL}/user/profile/sethandle/v1", json = sethandle_param1)
    assert request_data.status_code == 400
    sethandle_param1 = {
        "token": register_return1["token"],
        "handle_str": "mew"
    }
    request_data = requests.put(f"{BASE_URL}/user/profile/sethandle/v1", json = sethandle_param1)
    assert request_data.status_code == 200
    sethandle_param1 = {
        "token": register_return1["token"],
        "handle_str": "012345678901234567890"
    }
    request_data = requests.put(f"{BASE_URL}/user/profile/sethandle/v1", json = sethandle_param1)
    assert request_data.status_code == 200
    sethandle_param1 = {
        "token": register_return1["token"],
        "handle_str": "012345678901234567891"
    }
    request_data = requests.put(f"{BASE_URL}/user/profile/sethandle/v1", json = sethandle_param1)
    assert request_data.status_code == 400

def test_http_invalid_sethandle_alphanum():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    register_param_1 = {
        "email": "11037@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boy"
    }

    register_return1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1)
    register_return1 = register_return1.json()
    sethandle_param1 = {
        "token": register_return1["token"],
        "handle_str": "newh@ndle#"
    }
    request_data = requests.put(f"{BASE_URL}/user/profile/sethandle/v1", json = sethandle_param1)
    assert request_data.status_code == 400
    sethandle_param1 = {
        "token": register_return1["token"],
        "handle_str": "newh^andle__^"
    }
    request_data = requests.put(f"{BASE_URL}/user/profile/sethandle/v1", json = sethandle_param1)
    assert request_data.status_code == 400


def test_http_invalid_sethandle_duplicate():
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

    sethandle_param1 = {
        "token": register_return2["token"],
        "handle_str": "motherreggie"
    }
    request_data = requests.put(f"{BASE_URL}/user/profile/sethandle/v1", json = sethandle_param1)
    assert request_data.status_code == 400
    sethandle_param2 = {
        "token": register_return3["token"],
        "handle_str": "motherreggie0"
    }
    request_data = requests.put(f"{BASE_URL}/user/profile/sethandle/v1", json = sethandle_param2)
    assert request_data.status_code == 400
