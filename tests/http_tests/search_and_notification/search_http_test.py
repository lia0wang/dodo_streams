import requests
import pytest
from src import config

BASE_URL = config.url

@pytest.fixture
def users_json():
    users_json_list = []
    users_json_list.append({
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    })
    users_json_list.append({
        "email": "test2@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Smith"
    })
    users_json_list.append({
        "email": "test3@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Johnson"
    })
    return users_json_list
@pytest.fixture
def channel_json():
    return {
        "token": "",
        "name": "TheStrongest",
        "is_public": True
    }
@pytest.fixture
def message_strings():
    messages = []
    messages.append("Zakeru")
    messages.append("Baou Zakeruga")
    messages.append("Teozakeru")
    messages.append("Zageruzemu")
    return messages

def test_search_one_message(users_json, channel_json, message_strings):
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = users_json[0]).json()
    channel_json["token"] = auth_user["token"]
    channel1 = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_json).json()
    message_send_json = {
        'token': auth_user['token'],
        'channel_id': channel1['channel_id'],
        'message': message_strings[0]
    }
    requests.post(f"{BASE_URL}/message/send/v1", json = message_send_json)
    search_params = {
        "token": auth_user['token'],
        "query_str": "za"
    }
    search_get = requests.get(f"{BASE_URL}/search/v1", params = search_params).json()
    assert len(search_get["messages"]) == 1
    assert search_get["messages"][0]["message"] == "Zakeru"

def test_search_multi_channels_messages(users_json, channel_json, message_strings):
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = users_json[0]).json()
    user1 = requests.post(f"{BASE_URL}/auth/register/v2", json = users_json[1]).json()
    user2 = requests.post(f"{BASE_URL}/auth/register/v2", json = users_json[2]).json()
    channel_json["token"] = auth_user["token"]
    channel1 = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_json).json()
    channel_json["name"] = "The Real Monsters"
    channel2 = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_json).json()

    channel_join_json = {
        'token': user1['token'],
        'channel_id': channel1['channel_id']
    }
    requests.post(f"{BASE_URL}/channel/join/v2", json = channel_join_json)
    channel_join_json["token"] = user2["token"]
    channel_join_json["channel_id"] = channel2["channel_id"]
    requests.post(f"{BASE_URL}/channel/join/v2", json = channel_join_json)
    
    message_send_json = {
        'token': auth_user['token'],
        'channel_id': channel1['channel_id'],
        'message': message_strings[0]
    }
    message_send_json2 = {
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'message': message_strings[1]
    }
    message_send_json3 = {
        'token': auth_user['token'],
        'channel_id': channel2['channel_id'],
        'message': message_strings[2]
    }
    message_send_json4 = {
        'token': user2['token'],
        'channel_id': channel2['channel_id'],
        'message': message_strings[3]
    }
    requests.post(f"{BASE_URL}/message/send/v1", json = message_send_json)  
    requests.post(f"{BASE_URL}/message/send/v1", json = message_send_json2)
    requests.post(f"{BASE_URL}/message/send/v1", json = message_send_json3)
    requests.post(f"{BASE_URL}/message/send/v1", json = message_send_json4)
    search_params = {
        "token": auth_user['token'],
        "query_str": "za"
    }
    search_get = requests.get(f"{BASE_URL}/search/v1", params = search_params).json()
    assert len(search_get["messages"]) == 2
    search_params["query_str"] = "te"
    search_get = requests.get(f"{BASE_URL}/search/v1", params = search_params).json()
    assert len(search_get["messages"]) == 1
    assert search_get["messages"][0]["message"] == "Teozakeru"
    search_params["query_str"] = "wow"
    search_get = requests.get(f"{BASE_URL}/search/v1", params = search_params).json()
    assert len(search_get["messages"]) == 0

def test_search_multi_dms_messages(users_json, message_strings):
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = users_json[0]).json()
    user1 = requests.post(f"{BASE_URL}/auth/register/v2", json = users_json[1]).json()
    user2 = requests.post(f"{BASE_URL}/auth/register/v2", json = users_json[2]).json()
    dm_json1 = {
        'token': auth_user['token'],
        'u_ids': [user1["auth_user_id"]]
    }
    dm_json2 = {
        'token': auth_user['token'],
        'u_ids': [user2["auth_user_id"]]
    }
    dm1 = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_json1).json()
    dm2 = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_json2).json()
    message_send_json = {
        'token': auth_user['token'],
        'dm_id': dm1['dm_id'],
        'message': message_strings[0]
    }
    message_send_json2 = {
        'token': user1['token'],
        'dm_id': dm1['dm_id'],
        'message': message_strings[1]
    }
    message_send_json3 = {
        'token': auth_user['token'],
        'dm_id': dm2['dm_id'],
        'message': message_strings[2]
    }
    message_send_json4 = {
        'token': user2['token'],
        'dm_id': dm2['dm_id'],
        'message': message_strings[3]
    }
    requests.post(f"{BASE_URL}/message/senddm/v1", json = message_send_json)  
    requests.post(f"{BASE_URL}/message/senddm/v1", json = message_send_json2)
    requests.post(f"{BASE_URL}/message/senddm/v1", json = message_send_json3)
    requests.post(f"{BASE_URL}/message/senddm/v1", json = message_send_json4)
    search_params = {
        "token": auth_user['token'],
        "query_str": "za"
    }
    search_get = requests.get(f"{BASE_URL}/search/v1", params = search_params).json()
    assert len(search_get["messages"]) == 2
    search_params["query_str"] = "te"
    search_get = requests.get(f"{BASE_URL}/search/v1", params = search_params).json()
    assert len(search_get["messages"]) == 1
    assert search_get["messages"][0]["message"] == "Teozakeru"
    search_params["query_str"] = "wow"
    search_get = requests.get(f"{BASE_URL}/search/v1", params = search_params).json()
    assert len(search_get["messages"]) == 0

def test_search_channels_and_dms_messages(users_json, channel_json, message_strings):
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = users_json[0]).json()
    user1 = requests.post(f"{BASE_URL}/auth/register/v2", json = users_json[1]).json()

    channel_json["token"] = auth_user["token"]
    channel1 = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_json).json()

    channel_join_json = {
        'token': user1['token'],
        'channel_id': channel1['channel_id']
    }
    requests.post(f"{BASE_URL}/channel/join/v2", json = channel_join_json)
    dm_json1 = {
        'token': auth_user['token'],
        'u_ids': [user1["auth_user_id"]]
    }
    dm1 = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_json1).json()

    message_send_json1 = {
        'token': auth_user['token'],
        'channel_id': channel1['channel_id'],
        'message': message_strings[0]
    }
    message_send_json2 = {
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'message': message_strings[1]
    }
    message_senddm_json1 = {
        'token': auth_user['token'],
        'dm_id': dm1['dm_id'],
        'message': message_strings[2]
    }
    message_senddm_json2 = {
        'token': user1['token'],
        'dm_id': dm1['dm_id'],
        'message': message_strings[3]
    }
    requests.post(f"{BASE_URL}/message/send/v1", json = message_send_json1)  
    requests.post(f"{BASE_URL}/message/send/v1", json = message_send_json2)
    requests.post(f"{BASE_URL}/message/senddm/v1", json = message_senddm_json1)
    requests.post(f"{BASE_URL}/message/senddm/v1", json = message_senddm_json2)
    search_params = {
        "token": auth_user['token'],
        "query_str": "za"
    }
    search_get = requests.get(f"{BASE_URL}/search/v1", params = search_params).json()
    assert len(search_get["messages"]) == 2
    search_params["query_str"] = "te"
    search_get = requests.get(f"{BASE_URL}/search/v1", params = search_params).json()
    assert len(search_get["messages"]) == 1
    assert search_get["messages"][0]["message"] == "Teozakeru"
    search_params["query_str"] = "wow"
    search_get = requests.get(f"{BASE_URL}/search/v1", params = search_params).json()
    assert len(search_get["messages"]) == 0

def test_search_invalid_query_str(users_json, channel_json, message_strings):
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = users_json[0]).json()
    channel_json["token"] = auth_user["token"]
    channel1 = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_json).json()


    message_send_json = {
        'token': auth_user['token'],
        'channel_id': channel1['channel_id'],
        'message': message_strings[0]
    }
    requests.post(f"{BASE_URL}/message/send/v1", json = message_send_json)  

    search_params = {
        "token": auth_user['token'],
        "query_str": "i" * 1001
    }
    search_get = requests.get(f"{BASE_URL}/search/v1", params = search_params)
    assert search_get.status_code == 400
    search_params["query_str"] = ""
    search_get = requests.get(f"{BASE_URL}/search/v1", params = search_params)
    assert search_get.status_code == 400
    search_params["query_str"] = "i" * 1000
    search_get = requests.get(f"{BASE_URL}/search/v1", params = search_params)
    assert search_get.status_code == 200