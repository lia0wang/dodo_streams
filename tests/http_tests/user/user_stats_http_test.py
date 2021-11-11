import requests
import pytest
from src import config
BASE_URL = config.url
'''
def test_zero_activities_http():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    user_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_1).json()

    user_stats_request = {
        'token': user_1['token']
        }
    user_1_stats = requests.get(f"{BASE_URL}/user/stats/v1", params = user_stats_request)
    assert user_1_stats.status_code == 200
    user_1_stats = user_1_stats.json()
    print(user_1_stats)

    assert user_1_stats['channels_joined'][-1]['num_channels_joined'] == 0
    assert user_1_stats['dms_joined'][-1]['num_dms_joined'] == 0
    assert user_1_stats['messages_sent'][-1]['num_msgs_sent'] == 0
    assert user_1_stats['involvement_rate'] == 0
'''
def test_user_basic_dms_http():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    user_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_1).json()

    user_param_2= {
        "email": "test2@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Smith"
    }
    user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_2).json()

    dm_create_json = {
        "token": user_1["token"],
        "u_ids": [user_2["auth_user_id"]]
    }

    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_create_json).json()
    
    token_params = {
        "token": user_1["token"]
    }
    
    response = requests.get(f"{BASE_URL}/dm/list/v1", params = token_params)
    dm_list = response.json()
    
    assert response.status_code == 200
    assert dm_list == {"dms": [{'dm_id': dm['dm_id'], 'name': "agentsmith, johnsmith"}]}
    
    user_1_stats = requests.get(f"{BASE_URL}/user/stats/v1", params = token_params)
    assert user_1_stats.status_code == 200
    user_1_stats = user_1_stats.json()

    assert user_1_stats['channels_joined'][-1]['num_channels_joined'] == 0
    assert user_1_stats['dms_joined'][-1]['num_dms_joined'] == 1
    assert user_1_stats['messages_sent'][-1]['num_msgs_sent'] == 0
    assert user_1_stats['involvement_rate'] == 1

def test_user_basic_channels_http():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    user_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_1).json()

    channel_param = {
        'token': user_1['token'],
        'name': 'league',
        'is_public': True
    }
    requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json()
    
    token_params = {
        "token": user_1["token"]
    }
    
    user_1_stats = requests.get(f"{BASE_URL}/user/stats/v1", params = token_params)
    assert user_1_stats.status_code == 200
    user_1_stats = user_1_stats.json()

    assert user_1_stats['channels_joined'][-1]['num_channels_joined'] == 1
    assert user_1_stats['dms_joined'][-1]['num_dms_joined'] == 0
    assert user_1_stats['messages_sent'][-1]['num_msgs_sent'] == 0
    assert user_1_stats['involvement_rate'] == 1

def test_user_basic_msgs_http():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    user_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_1).json()

    channel_param = {
        'token': user_1['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json()
    
    msg_1 = 'test'
    
    message_send_program = {
        'token': user_1['token'],
        'channel_id': channel['channel_id'],
        'message': msg_1
    }
    msg_send = requests.post(f"{BASE_URL}/message/send/v1", json = message_send_program)
    assert msg_send.status_code == 200
    
    token_params = {
        "token": user_1["token"]
    }
    
    user_1_stats = requests.get(f"{BASE_URL}/user/stats/v1", params = token_params)
    assert user_1_stats.status_code == 200
    user_1_stats = user_1_stats.json()

    assert user_1_stats['channels_joined'][-1]['num_channels_joined'] == 1
    assert user_1_stats['dms_joined'][-1]['num_dms_joined'] == 0
    assert user_1_stats['messages_sent'][-1]['num_msgs_sent'] == 1
    assert user_1_stats['involvement_rate'] == 1 

def test_user_basic_dm_msgs_http():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    user_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_1).json()

    user_param_2= {
        "email": "test2@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Smith"
    }
    user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_2).json()

    dm_create_json = {
        "token": user_1["token"],
        "u_ids": [user_2["auth_user_id"]]
    }

    dm_return = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_create_json).json()
    
    token_params = {
        "token": user_1["token"]
    }

    msg_1 = 'test'
    
    dm_send_program = {
        'token': user_1['token'],
        'dm_id': dm_return['dm_id'],
        'message': msg_1
    }
    dm_send = requests.post(f"{BASE_URL}/message/senddm/v1", json = dm_send_program)
    assert dm_send.status_code == 200   
    
    user_1_stats = requests.get(f"{BASE_URL}/user/stats/v1", params = token_params)
    assert user_1_stats.status_code == 200
    user_1_stats = user_1_stats.json()

    assert user_1_stats['channels_joined'][-1]['num_channels_joined'] == 0
    assert user_1_stats['dms_joined'][-1]['num_dms_joined'] == 1
    assert user_1_stats['messages_sent'][-1]['num_msgs_sent'] == 1
    assert user_1_stats['involvement_rate'] == 1

def test_user_mutiple_users_http_1():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    user_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_1).json()

    user_param_2= {
        "email": "test2@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Smith"
    }
    user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_2).json()

    channel_param = {
        'token': user_1['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json()

    channel_invites_param = {
        'token': user_1['token'],
        'channel_id': channel['channel_id'],
        'u_id': user_2['auth_user_id']
    }
    
    requests.post(f"{BASE_URL}/channel/invite/v2", json = channel_invites_param)
     
    msg_1 = 'test'
    
    message_send_program = {
        'token': user_2['token'],
        'channel_id': channel['channel_id'],
        'message': msg_1
    }
    msg_send = requests.post(f"{BASE_URL}/message/send/v1", json = message_send_program)
    assert msg_send.status_code == 200
    
    token_params = {
        "token": user_1["token"]
    }
    
    user_1_stats = requests.get(f"{BASE_URL}/user/stats/v1", params = token_params)
    assert user_1_stats.status_code == 200
    user_1_stats = user_1_stats.json()

    assert user_1_stats['channels_joined'][-1]['num_channels_joined'] == 1
    assert user_1_stats['dms_joined'][-1]['num_dms_joined'] == 0
    assert user_1_stats['messages_sent'][-1]['num_msgs_sent'] == 0
    assert user_1_stats['involvement_rate'] == 0.5 

def test_user_mutiple_users_http_2():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    user_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_1).json()

    user_param_2= {
        "email": "test2@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Smith"
    }
    user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_2).json()

    channel_param = {
        'token': user_1['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json()

    channel_invites_param = {
        'token': user_1['token'],
        'channel_id': channel['channel_id'],
        'u_id': user_2['auth_user_id']
    }
    
    requests.post(f"{BASE_URL}/channel/invite/v2", json = channel_invites_param)
     
    msg_1 = 'test'
    
    message_send_program = {
        'token': user_2['token'],
        'channel_id': channel['channel_id'],
        'message': msg_1
    }
    msg_send = requests.post(f"{BASE_URL}/message/send/v1", json = message_send_program)
    assert msg_send.status_code == 200
    requests.post(f"{BASE_URL}/message/send/v1", json = message_send_program)
    
    token_params = {
        "token": user_1["token"]
    }
    
    user_1_stats = requests.get(f"{BASE_URL}/user/stats/v1", params = token_params)
    assert user_1_stats.status_code == 200
    user_1_stats = user_1_stats.json()

    assert user_1_stats['channels_joined'][-1]['num_channels_joined'] == 1
    assert user_1_stats['dms_joined'][-1]['num_dms_joined'] == 0
    assert user_1_stats['messages_sent'][-1]['num_msgs_sent'] == 0
    assert user_1_stats['involvement_rate'] == 1/3 

def test_user_mutiple_users_http_3():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    user_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_1).json()

    user_param_2= {
        "email": "test2@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Smith"
    }
    user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_2).json()

    channel_param = {
        'token': user_2['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json()
     
    msg_1 = 'test'
    
    message_send_program = {
        'token': user_2['token'],
        'channel_id': channel['channel_id'],
        'message': msg_1
    }
    msg_send = requests.post(f"{BASE_URL}/message/send/v1", json = message_send_program)
    assert msg_send.status_code == 200
    requests.post(f"{BASE_URL}/message/send/v1", json = message_send_program)
    
    token_params = {
        "token": user_1["token"]
    }
    
    user_1_stats = requests.get(f"{BASE_URL}/user/stats/v1", params = token_params)
    assert user_1_stats.status_code == 200
    user_1_stats = user_1_stats.json()

    assert user_1_stats['channels_joined'][-1]['num_channels_joined'] == 0
    assert user_1_stats['dms_joined'][-1]['num_dms_joined'] == 0
    assert user_1_stats['messages_sent'][-1]['num_msgs_sent'] == 0
    assert user_1_stats['involvement_rate'] == 0

def test_user_mutiple_users_msgs_http_4():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    user_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_1).json()

    user_param_2= {
        "email": "test2@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Smith"
    }
    user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_2).json()

    channel_param_1 = {
        'token': user_1['token'],
        'name': 'league',
        'is_public': True
    }
    channel_1 = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param_1).json()

    channel_invites_param = {
        'token': user_1['token'],
        'channel_id': channel_1['channel_id'],
        'u_id': user_2['auth_user_id']
    }
    requests.post(f"{BASE_URL}/channel/invite/v2", json = channel_invites_param)


    channel_param_2 = {
        'token': user_2['token'],
        'name': 'leagdsdue',
        'is_public': True
    }
    channel_2 = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param_2).json()    
     
    msg_1 = 'test'
    
    message_send_program = {
        'token': user_2['token'],
        'channel_id': channel_2['channel_id'],
        'message': msg_1
    }
    msg_send = requests.post(f"{BASE_URL}/message/send/v1", json = message_send_program)
    assert msg_send.status_code == 200
    requests.post(f"{BASE_URL}/message/send/v1", json = message_send_program)
    
    token_params = {
        "token": user_1["token"]
    }
    
    user_1_stats = requests.get(f"{BASE_URL}/user/stats/v1", params = token_params)
    assert user_1_stats.status_code == 200
    user_1_stats = user_1_stats.json()

    assert user_1_stats['channels_joined'][-1]['num_channels_joined'] == 1
    assert user_1_stats['dms_joined'][-1]['num_dms_joined'] == 0
    assert user_1_stats['messages_sent'][-1]['num_msgs_sent'] == 0
    assert user_1_stats['involvement_rate'] == 1/4

def test_user_mutiple_users_msgs_http_5():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    user_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_1).json()

    user_param_2= {
        "email": "test2@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Smith"
    }
    user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_2).json()
    
    user_param_3= {
        "email": "test3@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Johnson"
    }
    user_3 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_3).json()

    channel_param_1 = {
        'token': user_1['token'],
        'name': 'league',
        'is_public': True
    }
    channel_1 = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param_1).json()

    channel_invites_param_1 = {
        'token': user_1['token'],
        'channel_id': channel_1['channel_id'],
        'u_id': user_2['auth_user_id']
    }
    requests.post(f"{BASE_URL}/channel/invite/v2", json = channel_invites_param_1)


    channel_param_2 = {
        'token': user_2['token'],
        'name': 'leddague',
        'is_public': True
    }
    channel_2 = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param_2).json()
    
    channel_invites_param_2 = {
        'token': user_2['token'],
        'channel_id': channel_2['channel_id'],
        'u_id': user_1['auth_user_id']
    }
    requests.post(f"{BASE_URL}/channel/invite/v2", json = channel_invites_param_2)

    channel_param_3 = {
        'token': user_2['token'],
        'name': 'leafdfgue',
        'is_public': True
    }
    requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param_3).json()

    channel_param_4 = {
        'token': user_2['token'],
        'name': 'leaggfdfdfdue',
        'is_public': True
    }
    channel_4 = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param_4).json()    
    
     
    msg_1 = 'test'
    
    message_send_program = {
        'token': user_2['token'],
        'channel_id': channel_4['channel_id'],
        'message': msg_1
    }
    requests.post(f"{BASE_URL}/message/send/v1", json = message_send_program) #msg1
    requests.post(f"{BASE_URL}/message/send/v1", json = message_send_program) #msg2
    
    message_send_program = {
        'token': user_1['token'],
        'channel_id': channel_1['channel_id'],
        'message': msg_1
    }
    requests.post(f"{BASE_URL}/message/send/v1", json = message_send_program) #msg3
    requests.post(f"{BASE_URL}/message/send/v1", json = message_send_program) #msg4

    dm_create_json_1 = {
        "token": user_1["token"],
        "u_ids": [user_2["auth_user_id"]]
    }

    requests.post(f"{BASE_URL}/dm/create/v1", json = dm_create_json_1).json()   

    dm_create_json_2 = {
        "token": user_3["token"],
        "u_ids": [user_1["auth_user_id"]]
    }

    requests.post(f"{BASE_URL}/dm/create/v1", json = dm_create_json_2).json()   

    dm_create_json_3 = {
        "token": user_2["token"],
        "u_ids": [user_3["auth_user_id"]]
    }

    requests.post(f"{BASE_URL}/dm/create/v1", json = dm_create_json_3).json()
    
    token_params = {
        "token": user_1["token"]
    }
    
    user_1_stats = requests.get(f"{BASE_URL}/user/stats/v1", params = token_params)
    assert user_1_stats.status_code == 200
    user_1_stats = user_1_stats.json()

    assert user_1_stats['channels_joined'][-1]['num_channels_joined'] == 2
    assert user_1_stats['dms_joined'][-1]['num_dms_joined'] == 2
    assert user_1_stats['messages_sent'][-1]['num_msgs_sent'] == 2
    assert user_1_stats['involvement_rate'] == 6/11
