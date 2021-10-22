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
    
    register_param_0 = {
        "email": "bob123@gmail.com",
        "password": "bobahe",
        "name_first": "Bob",
        "name_last": "Marley"
    }
    
    invalid = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_0).json()
    
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param_1 = {
        "email": "shifanchen@gmail.com",
        "password": "djkadldjsa21",
        "name_first": "shifan",
        "name_last": "chen"
    }
    requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    register_param_2 = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()
    
    delete_info = {
        'token': invalid['token'],     # Invalid token
        'u_id': user['auth_user_id']
    }
    
    response = requests.delete(f"{BASE_URL}/admin/user/remove/v1", json = delete_info)
    
    assert response.status_code == ACCESS_ERROR
    
def test_invalid_uid():
    '''
    Checking if the function identifies invalid u_ids
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param_1 = {
        "email": "shifanchen@gmail.com",
        "password": "djkadldjsa21",
        "name_first": "shifan",
        "name_last": "chen"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    register_param_2 = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()
    
    delete_info = {
        'token': auth_user['token'], 
        'u_id': user['auth_user_id'] + 12  # Invalid id
    }
    
    response = requests.delete(f"{BASE_URL}/admin/user/remove/v1", json = delete_info)
    assert response.status_code == INPUT_ERROR    
    
def test_last_global():
    '''
    Checking if the function identifies if the u_id is the only global owner
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param_1 = {
        "email": "shifanchen@gmail.com",
        "password": "djkadldjsa21",
        "name_first": "shifan",
        "name_last": "chen"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()
        
    delete_info = {
        'token': auth_user['token'], 
        'u_id': auth_user['auth_user_id']
    }
    
    response = requests.delete(f"{BASE_URL}/admin/user/remove/v1", json = delete_info)
    assert response.status_code == INPUT_ERROR
    
def test_token_not_global():
    '''
    Checking if the function identifies if the token's u_id is not global
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param_1 = {
        "email": "shifanchen@gmail.com",
        "password": "djkadldjsa21",
        "name_first": "shifan",
        "name_last": "chen"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    register_param_2 = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()
    
    delete_info = {
        'token': user['token'], 
        'u_id': auth_user['auth_user_id']
    }
    
    response = requests.delete(f"{BASE_URL}/admin/user/remove/v1", json = delete_info)
    assert response.status_code ==  ACCESS_ERROR
    
def test_basic():
    '''
    Checking if the function works normally
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param_1 = {
        "email": "shifanchen@gmail.com",
        "password": "djkadldjsa21",
        "name_first": "shifan",
        "name_last": "chen"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    register_param_2 = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()
    
    channel_create_param = {
        'token': auth_user['token'],
        'name': "channel",
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_create_param).json()
    
    channel_join_param = {
        'token': user['token'],
        'channel_id': channel['channel_id']
    }
    join = requests.post(f"{BASE_URL}/channel/join/v2", json = channel_join_param)
    assert join.status_code == OK
    
    channel_message_param = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello'
    }
    send = requests.post(f"{BASE_URL}/message/send/v1", json = channel_message_param)
    assert send.status_code == OK
    
    channel_message_details_param = {
        'token': auth_user['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    }
    channel_message_details = requests.get(f"{BASE_URL}/channel/messages/v2", json = channel_message_details_param).json()
    assert channel_message_details['messages'] == "Removed user"
    
    dm_create_param = {
        "token": auth_user["token"],
        "u_ids": [user["auth_user_id"]]
    }
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_create_param).json()
    
    dm_message_param = {
        'token': user['token'],
        'dm_id': dm['dm_id'],
        'message': 'Hey'
    }
    requests.post(f"{BASE_URL}/message/senddm/v1", json = dm_message_param).json()
    
    delete_info = {
        'token': auth_user['token'], 
        'u_id': user['auth_user_id']
    }
    
    response = requests.delete(f"{BASE_URL}/admin/user/remove/v1", json = delete_info)
    assert response.status_code == OK
    
    # Removed from users list
    token = {
        'token': auth_user['token']
    }
    user_list = requests.get(f"{BASE_URL}/users/all/v1", json = token).json()
    assert user_list == [{'u_id': 1, 'email': register_param_1['email'], 'name_first': register_param_1['name_first'], 
                          'name_last': register_param_1['name_last'], 'handle_str': "shifanchen", 'permission_id': 1}]
    
    # Removed from channels
    channel_details_param = {
        'token': auth_user['token'],
        'channel_id': channel['channel_id']
    }
    channel_details = requests.get(f"{BASE_URL}/channel/details/v2", json = channel_details_param).json()
    assert channel_details['all_members'] == [{'u_id': 1, 'email': register_param_1['email'], 'name_first': register_param_1['name_first'], 
                                              'name_last': register_param_1['name_last'], 'handle_str': "shifanchen"}]
    
    # Removed from dms
    dm_details_param = {
        'token': auth_user['token'],
        'dm_id': dm['dm_id']
    }
    dm_details = requests.get(f"{BASE_URL}/dm/details/v1", json = dm_details_param).json()
    assert dm_details['members'] == [{'u_id': 1, 'email': register_param_1['email'], 'name_first': register_param_1['name_first'], 
                                       'name_last': register_param_1['name_last'], 'handle_str': "shifanchen"}]
    
    # Retrieve profile
    user_profile_param = {
        'token': auth_user['token'],
        'u_id': user['auth_user_id']
    }
    user_profile = requests.get(f"{BASE_URL}/user/profile/v1", json = user_profile_param).json()
    assert user_profile['name_first'] == "Removed"
    assert user_profile['name_last'] == "user"
    
    # Message content replaced by 'Removed user' in channels
    channel_message_details_param = {
        'token': auth_user['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    }
    channel_message_details = requests.get(f"{BASE_URL}/channel/messages/v2", json = channel_message_details_param).json()
    assert channel_message_details['messages'] == "Removed user"
    # [0]['message']
    
    # Message content replaced by 'Removed user' in dms
    dm_message_details_param = {
        'token': auth_user['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    }
    dm_message_details = requests.get(f"{BASE_URL}/dm/messages/v1", json = dm_message_details_param).json()
    assert dm_message_details['messages'][0]['message'] == "Removed user"