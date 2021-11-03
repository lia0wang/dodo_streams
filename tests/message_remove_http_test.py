import requests
import pytest
import json
from src import config

BASE_URL = config.url

def test_cannot_remove_deleted_message_http():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    message_1 = "dsdaada"
    
    register_param_1 = {
        "email": "test@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    auth_user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()
    
    channel_param_1 = {
        'token': auth_user_1['token'],
        'name': 'league',
        'is_public': True
    }
    channel_1 = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param_1).json()
    
    message_send_program_1 = {
        'token': auth_user_1['token'],
        'channel_id': channel_1['channel_id'],
        'message': message_1
    }

    msg_id_1 = requests.post(f"{BASE_URL}/message/send/v1",json = message_send_program_1).json()

    message_remove_program_1 = {
        'token': auth_user_1['token'],
        'message_id': msg_id_1['message_id']
    }

    dm_remove_1 = requests.delete(f"{BASE_URL}/message/remove/v1", json = message_remove_program_1)
    assert dm_remove_1.status_code == 200  
    dm_remove_2 = requests.delete(f"{BASE_URL}/message/remove/v1", json = message_remove_program_1)
    assert dm_remove_2.status_code == 400      


def test_msg_remove_invalid_msg_id_1_http():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    message_1 = "dsdaada"
    message_2 = "pojno"
    
    register_param_1 = {
        "email": "test@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    auth_user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()
    
    channel_param_1 = {
        'token': auth_user_1['token'],
        'name': 'league',
        'is_public': True
    }
    channel_1 = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param_1).json()
    
    message_send_program_1 = {
        'token': auth_user_1['token'],
        'channel_id': channel_1['channel_id'],
        'message': message_1
    }

    msg_id_1 = requests.post(f"{BASE_URL}/message/send/v1",json = message_send_program_1).json()

    register_param_2 = {
        "email": "tset@gmail.com",
        "password": "abcd1234",
        "name_first": "Smith",
        "name_last": "John"
    }
    auth_user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()
    
    channel_param_2 = {
        'token': auth_user_2['token'],
        'name': 'league',
        'is_public': True
    }
    channel_2 = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param_2).json()
    
    message_send_program_2 = {
        'token': auth_user_2['token'],
        'channel_id': channel_2['channel_id'],
        'message': message_2
    }

    msg_id_2 = requests.post(f"{BASE_URL}/message/send/v1",json = message_send_program_2).json()
 

    message_remove_program_1 = {
        'token': auth_user_1['token'],
        'message_id': msg_id_2['message_id']
    }
    message_remove_program_2 = {
        'token': auth_user_2['token'],
        'message_id': msg_id_1['message_id']
    }

    dm_remove_1 = requests.delete(f"{BASE_URL}/message/remove/v1", json = message_remove_program_1)
    assert dm_remove_1.status_code == 200
    dm_remove_2 = requests.delete(f"{BASE_URL}/message/remove/v1", json = message_remove_program_2)
    assert dm_remove_2.status_code == 403 

def test_msg_remove_invalid_msg_id_2_http():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    message_1 = "dsdaada"
    
    register_param_1 = {
        "email": "test@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    auth_user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()
    
    channel_param_1 = {
        'token': auth_user_1['token'],
        'name': 'league',
        'is_public': True
    }
    channel_1 = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param_1).json()
    
    message_send_program_1 = {
        'token': auth_user_1['token'],
        'channel_id': channel_1['channel_id'],
        'message': message_1
    }

    msg_id_1 = requests.post(f"{BASE_URL}/message/send/v1",json = message_send_program_1).json()

    msg_id_1['message_id'] +=99
    
    message_remove_program_1 = {
        'token': auth_user_1['token'],
        'message_id': msg_id_1['message_id']
    }

    dm_remove_1 = requests.delete(f"{BASE_URL}/message/remove/v1", json = message_remove_program_1)
    assert dm_remove_1.status_code == 400  

def test_global_owner_can_remove_members_message_channel_http():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()
    
    channel_param = {
        'token': user_1['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json()

    register_param_2 = {
        "email": "test2@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Smith"
    }
    user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()


    channel_invites_param = {
        'token': user_1['token'],
        'channel_id': channel['channel_id'],
        'u_id': user_2['auth_user_id']
    }
    
    requests.post(f"{BASE_URL}/channel/invite/v2", json = channel_invites_param)

    msg = "test"
    message_send_program = {
        'token': user_2['token'],
        'channel_id': channel['channel_id'],
        'message': msg
    }
    
    target_message = requests.post(f"{BASE_URL}/message/send/v1",json = message_send_program)
    assert target_message.status_code == 200
    target_message = target_message.json()

    message_remove_program = {
        'token': user_1['token'],
        'message_id': target_message['message_id'],
    }

    response = requests.delete(f"{BASE_URL}/message/remove/v1",json = message_remove_program)

    assert response.status_code == 200

def test_owner_can_remove_members_message_channel_http():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    register_param_2 = {
        "email": "test2@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Smith"
    }
    user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()

    register_param_3 = {
        "email": "test3@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Johnson"
    }
    user_3 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_3).json()    

    channel_param = {
        'token': user_1['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json()
    '''
    channel_invites_param_1 = {
        'token': user_1['token'],
        'channel_id': channel['channel_id'],
        'u_id': user_2['auth_user_id']
    }
    requests.post(f"{BASE_URL}/channel/invite/v2", json = channel_invites_param_1)
    
    channel_invites_param_2 = {
        'token': user_1['token'],
        'channel_id': channel['channel_id'],
        'u_id': user_3['auth_user_id']
    }
    
    requests.post(f"{BASE_URL}/channel/invite/v2", json = channel_invites_param_2)
    '''
    channel_join_param = {
        'token': user_2['token'],
        'channel_id': channel['channel_id']
    }
    response = requests.post(f"{BASE_URL}/channel/join/v2", json = channel_join_param)

    channel_join_param = {
        'token': user_3['token'],
        'channel_id': channel['channel_id']
    }
    response = requests.post(f"{BASE_URL}/channel/join/v2", json = channel_join_param)
    
    channel_addowner_param = {
        'token': user_1['token'],
        'channel_id': channel['channel_id'],
        'u_id': user_2['auth_user_id']
    }
    response = requests.post(f"{BASE_URL}/channel/addowner/v1", json = channel_addowner_param)
    
    msg = "test"
    message_send_program = {
        'token': user_3['token'],
        'channel_id': channel['channel_id'],
        'message': msg
    }
    
    target_message = requests.post(f"{BASE_URL}/message/send/v1",json = message_send_program)
    assert target_message.status_code == 200
    target_message = target_message.json()
    '''
    ch_join_param = {
        "token": user_1["token"], 
        "channel_id": channel["channel_id"]
    }
    get_request = requests.get(f"{BASE_URL}/channel/details/v2", params = ch_join_param)
    assert get_request.status_code == 200
    request_data = get_request.json()
    print(request_data["owner_members"])
    '''
    message_remove_program = {
        'token': user_2['token'],
        'message_id': target_message['message_id'],
    }

    response = requests.delete(f"{BASE_URL}/message/remove/v1",json = message_remove_program)

    assert response.status_code == 200    

def test_original_poster_can_remove_message_channel_http():    
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    register_param_2 = {
        "email": "test2@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Smith"
    }
    user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()

    channel_param = {
        'token': user_1['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json()

    channel_join_param = {
        'token': user_2['token'],
        'channel_id': channel['channel_id']
    }
    response = requests.post(f"{BASE_URL}/channel/join/v2", json = channel_join_param)
    
    msg = "test"
    message_send_program = {
        'token': user_2['token'],
        'channel_id': channel['channel_id'],
        'message': msg
    }
    
    target_message = requests.post(f"{BASE_URL}/message/send/v1",json = message_send_program).json()

    message_remove_program = {
        'token': user_2['token'],
        'message_id': target_message['message_id'],
    }

    response = requests.delete(f"{BASE_URL}/message/remove/v1",json = message_remove_program)

    assert response.status_code == 200

def test_nonowner_nonposter_cant_remove_http():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    register_param_2 = {
        "email": "test2@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Smith"
    }
    user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()

    register_param_3 = {
        "email": "test4@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Johnson"
    }
    user_3 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_3).json()

    channel_param = {
        'token': user_1['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json()

    channel_join_param_1 = {
        'token': user_2['token'],
        'channel_id': channel['channel_id']
    }
    response = requests.post(f"{BASE_URL}/channel/join/v2", json = channel_join_param_1)

    channel_join_param_2 = {
        'token': user_3['token'],
        'channel_id': channel['channel_id']
    }
    response = requests.post(f"{BASE_URL}/channel/join/v2", json = channel_join_param_2)
    
    msg = "test"
    message_send_program = {
        'token': user_2['token'],
        'channel_id': channel['channel_id'],
        'message': msg
    }
    
    target_message = requests.post(f"{BASE_URL}/message/send/v1",json = message_send_program).json()

    message_remove_program = {
        'token': user_3['token'],
        'message_id': target_message['message_id'],
    }

    response = requests.delete(f"{BASE_URL}/message/remove/v1",json = message_remove_program)

    assert response.status_code == 403

def test_original_poster_can_remove_message_dm_http():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    register_param_2 = {
        "email": "test2@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Smith"
    }
    user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()

    register_param_3 = {
        "email": "test4@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Johnson"
    }
    user_3 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_3).json()

    u_id1 = user_1['auth_user_id']
    u_id2 = user_2['auth_user_id']
    u_ids = [u_id1,u_id2]

    dm_param = {
        'token': user_3['token'],
        'u_ids': u_ids
    }
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_param).json()
    
    msg = "test"
    
    dm_send_program = {
        'token': user_3['token'],
        'dm_id': dm['dm_id'],
        'message': msg
    }
    
    target_dm = requests.post(f"{BASE_URL}/message/senddm/v1",json = dm_send_program).json()

    dm_remove_program = {
        'token': user_3['token'],
        'message_id': target_dm['message_id'],
    }

    response = requests.delete(f"{BASE_URL}/message/remove/v1",json = dm_remove_program)

    assert response.status_code == 200

def test_global_owner_cant_remove_members_message_dm_http():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json() #permission_id = 1

    register_param_2 = {
        "email": "test2@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Smith"
    }
    user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()

    register_param_3 = {
        "email": "test4@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Johnson"
    }
    user_3 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_3).json()

    u_id1 = user_1['auth_user_id']
    u_id2 = user_2['auth_user_id']
    u_ids = [u_id1,u_id2]

    dm_param = {
        'token': user_3['token'],
        'u_ids': u_ids
    }
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_param).json()
    
    msg = "test"
    
    dm_send_program = {
        'token': user_3['token'],
        'dm_id': dm['dm_id'],
        'message': msg
    }
    
    target_dm = requests.post(f"{BASE_URL}/message/senddm/v1",json = dm_send_program).json()

    dm_remove_program = {
        'token': user_1['token'],
        'message_id': target_dm['message_id'],
    }

    response = requests.delete(f"{BASE_URL}/message/remove/v1",json = dm_remove_program)

    assert response.status_code == 403

def test_owner_can_remove_members_message_dm_http():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json() #permission_id = 1

    register_param_2 = {
        "email": "test2@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Smith"
    }
    user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()

    register_param_3 = {
        "email": "test4@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Johnson"
    }
    user_3 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_3).json()

    u_id1 = user_1['auth_user_id']
    u_id2 = user_2['auth_user_id']
    u_ids = [u_id1,u_id2]

    dm_param = {
        'token': user_3['token'],
        'u_ids': u_ids
    }
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_param).json()
    
    msg = "test"
    
    dm_send_program = {
        'token': user_2['token'],
        'dm_id': dm['dm_id'],
        'message': msg
    }
    
    target_dm = requests.post(f"{BASE_URL}/message/senddm/v1",json = dm_send_program).json()

    dm_remove_program = {
        'token': user_3['token'],
        'message_id': target_dm['message_id'],
    }

    response = requests.delete(f"{BASE_URL}/message/remove/v1",json = dm_remove_program)

    assert response.status_code == 200
