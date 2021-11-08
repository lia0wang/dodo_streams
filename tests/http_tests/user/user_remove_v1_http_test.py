import requests
import pytest
from src import config

BASE_URL = config.url
OK = 200
ACCESS_ERROR = 403
INPUT_ERROR = 400

def test_invalid_token():
    '''
    Checking if the function can identify an invalid token
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    invalid_user_json = {
        "email": "bob123@gmail.com",
        "password": "bobahe",
        "name_first": "Bob",
        "name_last": "Marley"
    }
    
    invalid = requests.post(f"{BASE_URL}/auth/register/v2", json = invalid_user_json).json()
    
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    user_1_json = {
        "email": "shifanchen@gmail.com",
        "password": "djkadldjsa21",
        "name_first": "shifan",
        "name_last": "chen"
    }
    requests.post(f"{BASE_URL}/auth/register/v2", json = user_1_json).json()

    user_2_json = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = user_2_json).json()
    
    delete_json = {
        'token': invalid['token'],     # Invalid token
        'u_id': user['auth_user_id']
    }
    
    response = requests.delete(f"{BASE_URL}/admin/user/remove/v1", json = delete_json)
    
    assert response.status_code == ACCESS_ERROR
    
def test_invalid_uid():
    '''
    Checking if the function identifies invalid u_ids
    '''
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
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = user_1_json).json()
    
    delete_json = {
        'token': auth_user['token'], 
        'u_id': user['auth_user_id'] + 12  # Invalid id
    }
    
    response = requests.delete(f"{BASE_URL}/admin/user/remove/v1", json = delete_json)
    assert response.status_code == INPUT_ERROR    
    
def test_last_global():
    '''
    Checking if the function identifies if the u_id is the only global owner
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    auth_user_json = {
        "email": "shifanchen@gmail.com",
        "password": "djkadldjsa21",
        "name_first": "shifan",
        "name_last": "chen"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = auth_user_json).json()
        
    delete_json = {
        'token': auth_user['token'], 
        'u_id': auth_user['auth_user_id']
    }
    
    response = requests.delete(f"{BASE_URL}/admin/user/remove/v1", json = delete_json)
    assert response.status_code == INPUT_ERROR
    
def test_token_not_global():
    '''
    Checking if the function identifies if the token's u_id is not global
    '''
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
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = user_1_json).json()
    
    delete_json = {
        'token': user['token'], 
        'u_id': auth_user['auth_user_id']
    }
    
    response = requests.delete(f"{BASE_URL}/admin/user/remove/v1", json = delete_json)
    assert response.status_code ==  ACCESS_ERROR
    
def test_basic():
    '''
    Checking if the function works normally
    '''
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
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = user_1_json).json()
    
    channel_create_json = {
        'token': auth_user['token'],
        'name': "channel",
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_create_json).json()
    
    channel_join_json = {
        'token': user['token'],
        'channel_id': channel['channel_id']
    }
    join = requests.post(f"{BASE_URL}/channel/join/v2", json = channel_join_json)
    assert join.status_code == OK
    
    channel_message_json = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello'
    }
    requests.post(f"{BASE_URL}/message/send/v1", json = channel_message_json).json()
    
    dm_create_json = {
        "token": user["token"],
        "u_ids": [auth_user["auth_user_id"]]
    }
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_create_json).json()
    
    dm_message_json = {
        'token': user['token'],
        'dm_id': dm['dm_id'],
        'message': 'Hey'
    }
    check = requests.post(f"{BASE_URL}/message/senddm/v1", json = dm_message_json)
    assert check.status_code == OK
    
    delete_json = {
        'token': auth_user['token'], 
        'u_id': user['auth_user_id']
    }
    
    response = requests.delete(f"{BASE_URL}/admin/user/remove/v1", json = delete_json)
    assert response.status_code == OK
    
    # Removed from users list
    token_params = {
        'token': auth_user['token']
    }
    user_list = requests.get(f"{BASE_URL}/users/all/v1", params = token_params).json()
    assert len(user_list['users']) == 1

    # Removed from channels
    channel_details_param = {
        'token': auth_user['token'],
        'channel_id': channel['channel_id']
    }
    channel_details = requests.get(f"{BASE_URL}/channel/details/v2", params = channel_details_param).json()
    assert len(channel_details['all_members']) == 1 
    
    # Removed from dms
    dm_details_param = {
        'token': auth_user['token'],
        'dm_id': dm['dm_id']
    }
    dm_details = requests.get(f"{BASE_URL}/dm/details/v1", params = dm_details_param).json()
    assert len(dm_details['members']) == 1 
    
    # Retrieve profile
    user_profile_param = {
        'token': auth_user['token'],
        'u_id': user['auth_user_id']
    }
    user_profile = requests.get(f"{BASE_URL}/user/profile/v1", params = user_profile_param).json()
    assert user_profile["user"]['name_first'] == "Removed"
    assert user_profile["user"]['name_last'] == "user"
    
    # Message content replaced by 'Removed user' in channels
    channel_message_details_param = {
        'token': auth_user['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    }
    channel_message_details = requests.get(f"{BASE_URL}/channel/messages/v2", params = channel_message_details_param).json()
    assert channel_message_details['messages'][0]['message'] == "Removed user"
    
    # Message content replaced by 'Removed user' in dms
    dm_message_details_param = {
        'token': auth_user['token'],
        'dm_id': dm['dm_id'],
        'start': 0
    }
    dm_message_details = requests.get(f"{BASE_URL}/dm/messages/v1", params = dm_message_details_param).json()
    assert dm_message_details['messages'][0]['message'] == "Removed user"
