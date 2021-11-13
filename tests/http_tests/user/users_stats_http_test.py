import requests
import pytest
from src import config
BASE_URL = config.url
    
def test_users_zero_activities_http():
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
    
    users_stats = requests.get(f"{BASE_URL}/users/stats/v1", params = user_stats_request)
    assert users_stats.status_code == 200
    users_stats = users_stats.json()
    print(users_stats)

    assert users_stats['workspace_stats']['channels_exist'][-1]['num_channels_exist'] == 0
    assert users_stats['workspace_stats']['dms_exist'][-1]['num_dms_exist'] == 0
    assert users_stats['workspace_stats']['messages_exist'][-1]['num_messages_exist'] == 0
    assert users_stats['workspace_stats']['utilization_rate'] == 0

def test_users_mutiple_users_msgs_http_4():
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
    
    msg_2 = 'test'
    
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
        "token": user_2["token"],
        "u_ids": [user_1["auth_user_id"]]
    }

    requests.post(f"{BASE_URL}/dm/create/v1", json = dm_create_json_2).json()   

    dm_create_json_3 = {
        "token": user_2["token"],
        "u_ids": [user_1["auth_user_id"]]
    }

    dm_3 = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_create_json_3).json()

    dm_send_program = {
        'token': user_2['token'],
        'dm_id': dm_3['dm_id'],
        'message': msg_2
    }
    response = requests.post(f"{BASE_URL}/message/senddm/v1", json = dm_send_program)
    assert response.status_code == 200    

    user_stats_request_1 = {
        'token': user_1['token']
        }
    user_stats_request_2 = {
        'token': user_2['token']
        }
    user_stats_request_3 = {
        'token': user_3['token']
        }

    
    user_1_stats = requests.get(f"{BASE_URL}/user/stats/v1", params = user_stats_request_1)
    assert user_1_stats.status_code == 200
    user_1_stats = user_1_stats.json()
    
    user_2_stats = requests.get(f"{BASE_URL}/user/stats/v1", params = user_stats_request_2)
    assert user_2_stats.status_code == 200
    user_2_stats = user_2_stats.json()

    user_3_stats = requests.get(f"{BASE_URL}/user/stats/v1", params = user_stats_request_3)
    assert user_3_stats.status_code == 200
    user_3_stats = user_3_stats.json()
    
    assert user_1_stats['user_stats']['channels_joined'][-1]['num_channels_joined'] == 2
    assert user_1_stats['user_stats']['dms_joined'][-1]['num_dms_joined'] == 3
    assert user_1_stats['user_stats']['messages_sent'][-1]['num_messages_sent'] == 2
    assert user_1_stats['user_stats']['involvement_rate'] == 7/12

    assert user_2_stats['user_stats']['channels_joined'][-1]['num_channels_joined'] == 4
    assert user_2_stats['user_stats']['dms_joined'][-1]['num_dms_joined'] == 3
    assert user_2_stats['user_stats']['messages_sent'][-1]['num_messages_sent'] == 3
    assert user_2_stats['user_stats']['involvement_rate'] == 10/12

    assert user_3_stats['user_stats']['channels_joined'][-1]['num_channels_joined'] == 0
    assert user_3_stats['user_stats']['dms_joined'][-1]['num_dms_joined'] == 0
    assert user_3_stats['user_stats']['messages_sent'][-1]['num_messages_sent'] == 0
    assert user_3_stats['user_stats']['involvement_rate'] == 0
    
    users_stats = requests.get(f"{BASE_URL}/users/stats/v1", params = user_stats_request_2)
    assert users_stats.status_code == 200
    users_stats = users_stats.json()
    print(users_stats)
    
    assert users_stats['workspace_stats']['channels_exist'][-1]['num_channels_exist'] == 4
    assert users_stats['workspace_stats']['dms_exist'][-1]['num_dms_exist'] == 3
    assert users_stats['workspace_stats']['messages_exist'][-1]['num_messages_exist'] == 5
    assert users_stats['workspace_stats']['utilization_rate'] == 2/3
