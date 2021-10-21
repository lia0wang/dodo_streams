import pytest
import requests
import pytest
import json

from src import config

BASE_URL = config.url
 
def test_http_details_multiple_members():
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
    get_request = requests.get(f"{BASE_URL}/channel/details/v2", json = ch_join_param)
    request_data = get_request.json()

    assert request_data["name"] == "TheRealMonsters"
    assert request_data["is_public"] == True

    assert request_data["owner_members"][0]["u_id"] == register_return1["auth_user_id"]
    assert request_data["owner_members"][0]["email"] == "11037@gmail.com"
    assert request_data["owner_members"][0]["name_first"] == "Hopeful"
    assert request_data["owner_members"][0]["name_last"] == "Boy"
    assert request_data["owner_members"][0]["handle_str"] == "hopefulboy"    

    assert request_data["all_members"][0]["u_id"] == register_return1["auth_user_id"]
    assert request_data["all_members"][0]["email"] == "11037@gmail.com"
    assert request_data["all_members"][0]["name_first"] == "Hopeful"
    assert request_data["all_members"][0]["name_last"] == "Boy"
    assert request_data["all_members"][0]["handle_str"] == "hopefulboy"    

    assert request_data["all_members"][1]["u_id"] == register_return2["auth_user_id"]
    assert request_data["all_members"][1]["email"] == "MotherReggie@gmail.com"
    assert request_data["all_members"][1]["name_first"] == "Mother"
    assert request_data["all_members"][1]["name_last"] == "Reggie"
    assert request_data["all_members"][1]["handle_str"] == "motherreggie"  

    assert request_data["all_members"][2]["u_id"] == register_return3["auth_user_id"]
    assert request_data["all_members"][2]["email"] == "groundpound@gmail.com"
    assert request_data["all_members"][2]["name_first"] == "Mario"
    assert request_data["all_members"][2]["name_last"] == "Pratt"
    assert request_data["all_members"][2]["handle_str"] == "mariopratt"  

def test_http_details_one_member():
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
    ch_details_param = {
        "token": register_return1["token"], 
        "channel_id": create_return["channel_id"]
    }
    get_request = requests.get(f"{BASE_URL}/channel/details/v2", json = ch_details_param)
    request_data = get_request.json()

    assert request_data["name"] == "TheRealMonsters"
    assert request_data["is_public"] == True

    assert request_data["owner_members"][0]["u_id"] == register_return1["auth_user_id"]
    assert request_data["owner_members"][0]["email"] == "11037@gmail.com"
    assert request_data["owner_members"][0]["name_first"] == "Hopeful"
    assert request_data["owner_members"][0]["name_last"] == "Boy"
    assert request_data["owner_members"][0]["handle_str"] == "hopefulboy"    

    assert request_data["all_members"][0]["u_id"] == register_return1["auth_user_id"]
    assert request_data["all_members"][0]["email"] == "11037@gmail.com"
    assert request_data["all_members"][0]["name_first"] == "Hopeful"
    assert request_data["all_members"][0]["name_last"] == "Boy"
    assert request_data["all_members"][0]["handle_str"] == "hopefulboy"   

def test_http_invalid_channel_id():
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
    ch_details_param = {
        "token": register_return1["token"], 
        "channel_id": create_return["channel_id"] + 1
    }
    get_request = requests.get(f"{BASE_URL}/channel/details/v2", json = ch_details_param)
    assert get_request.status_code == 400

def test_http_not_member():
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

    register_return1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1)
    register_return1 = register_return1.json()
    register_return2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2)
    register_return2 = register_return2.json()
    # 2nd registered user creates a channel
    ch_create_param = {
        "token": register_return2["token"],
        "name": "TheFakeMonsters",
        "is_public": True
    }
    create_return = requests.post(f"{BASE_URL}/channels/create/v2", json = ch_create_param).json()
    # 1st registered user requests details of channel created by 2nd user without joining
    ch_details_param = {
        "token": register_return1["token"], 
        "channel_id": create_return["channel_id"]
    }
    get_request = requests.get(f"{BASE_URL}/channel/details/v2", json = ch_details_param)
    assert get_request.status_code == 403

def test_http_details_multiple_channels():
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

    ch_create_param1 = {
        "token": register_return1["token"],
        "name": "TheRealMonsters",
        "is_public": True
    }
    ch_create_param2 = {
        "token": register_return2["token"],
        "name": "SuperBeautyCuties",
        "is_public": True
    }
    create_return1 = requests.post(f"{BASE_URL}/channels/create/v2", json = ch_create_param1)
    create_return1 = create_return1.json()
    create_return2 = requests.post(f"{BASE_URL}/channels/create/v2", json = ch_create_param2)
    create_return2 = create_return2.json()
    ch_param1 = {
        "token": register_return1["token"], 
        "channel_id": create_return1["channel_id"]
    }
    ch_param2 = {
        "token": register_return3["token"], 
        "channel_id": create_return2["channel_id"]
    }
    requests.post(f"{BASE_URL}/channel/join/v2", json = ch_param2)
    get_request1 = requests.get(f"{BASE_URL}/channel/details/v2", json = ch_param1)
    request_data1 = get_request1.json()
    get_request2 = requests.get(f"{BASE_URL}/channel/details/v2", json = ch_param2)
    request_data2 = get_request2.json()

    # check details of first channel
    assert request_data1["name"] == "TheRealMonsters"
    assert request_data1["is_public"] == True

    assert request_data1["owner_members"][0]["u_id"] == register_return1["auth_user_id"]
    assert request_data1["owner_members"][0]["email"] == "11037@gmail.com"
    assert request_data1["owner_members"][0]["name_first"] == "Hopeful"
    assert request_data1["owner_members"][0]["name_last"] == "Boy"
    assert request_data1["owner_members"][0]["handle_str"] == "hopefulboy"    

    assert request_data1["all_members"][0]["u_id"] == register_return1["auth_user_id"]
    assert request_data1["all_members"][0]["email"] == "11037@gmail.com"
    assert request_data1["all_members"][0]["name_first"] == "Hopeful"
    assert request_data1["all_members"][0]["name_last"] == "Boy"
    assert request_data1["all_members"][0]["handle_str"] == "hopefulboy"    
    # check details of 2nd channel
    assert request_data2["name"] == "SuperBeautyCuties"
    assert request_data2["is_public"] == True

    assert request_data2["owner_members"][0]["u_id"] == register_return2["auth_user_id"]
    assert request_data2["owner_members"][0]["email"] == "MotherReggie@gmail.com"
    assert request_data2["owner_members"][0]["name_first"] == "Mother"
    assert request_data2["owner_members"][0]["name_last"] == "Reggie"
    assert request_data2["owner_members"][0]["handle_str"] == "motherreggie"  

    assert request_data2["all_members"][0]["u_id"] == register_return2["auth_user_id"]
    assert request_data2["all_members"][0]["email"] == "MotherReggie@gmail.com"
    assert request_data2["all_members"][0]["name_first"] == "Mother"
    assert request_data2["all_members"][0]["name_last"] == "Reggie"
    assert request_data2["all_members"][0]["handle_str"] == "motherreggie"  

    assert request_data2["all_members"][1]["u_id"] == register_return3["auth_user_id"]
    assert request_data2["all_members"][1]["email"] == "groundpound@gmail.com"
    assert request_data2["all_members"][1]["name_first"] == "Mario"
    assert request_data2["all_members"][1]["name_last"] == "Pratt"
    assert request_data2["all_members"][1]["handle_str"] == "mariopratt"  