import requests
import pytest
import json

from src import config

BASE_URL = config.url

def test_msg_edit_basics():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param = {
        "email": "test@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()
    
    channel_param = {
        'token': auth_user['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json()
    msg = "test"

    message_send_program = {
        'token': auth_user['token'],
        'channel_id': channel['channel_id'],
        'message': msg
    }
    
    msg2 = "edit"
    target_message = requests.post(f"{BASE_URL}/message/send/v1",json = message_send_program)
    assert target_message.status_code == 200
    target_message = target_message.json()
    
    message_edit_program = {
        'token': auth_user['token'],
        'message_id': target_message['message_id'],
        'message': msg2
    }

    response = requests.put(f"{BASE_URL}/message/edit/v1",json = message_edit_program)

    assert response.status_code == 200
    
def test_msg_edit_redirection():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param = {
        "email": "test@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()
    
    channel_param = {
        'token': auth_user['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json()
    msg = "test"

    message_send_program = {
        'token': auth_user['token'],
        'channel_id': channel['channel_id'],
        'message': msg
    }
    
    msg2 = ''
    
    target_message = requests.post(f"{BASE_URL}/message/send/v1",json = message_send_program)
    assert target_message.status_code == 200
    target_message = target_message.json()
    
    message_edit_program = {
        'token': auth_user['token'],
        'message_id': target_message['message_id'],
        'message': msg2
    }

    response = requests.put(f"{BASE_URL}/message/edit/v1",json = message_edit_program)

    assert response.status_code == 200
    
def test_msg_edit_invalid_input():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param = {
        "email": "test@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()
    
    channel_param = {
        'token': auth_user['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json()

    msg = "test"
    message_send_program = {
        'token': auth_user['token'],
        'channel_id': channel['channel_id'],
        'message': msg
    }
    
    target_message = requests.post(f"{BASE_URL}/message/send/v1",json = message_send_program)
    assert target_message.status_code == 200
    target_message = target_message.json()

    msg2 = "1"*1001     
    message_edit_program = {
        'token': auth_user['token'],
        'message_id': target_message['message_id'],
        'message': msg2
    }

    response = requests.put(f"{BASE_URL}/message/edit/v1",json = message_edit_program)

    assert response.status_code == 400
    
def test_msg_edit_invalid_msg_id():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param = {
        "email": "test@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()
    
    channel_param = {
        'token': auth_user['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json()
    msg = "test"

    message_send_program = {
        'token': auth_user['token'],
        'channel_id': channel['channel_id'],
        'message': msg
    }
    
    msg2 = "edit"
    target_message = requests.post(f"{BASE_URL}/message/send/v1",json = message_send_program)
    assert target_message.status_code == 200
    target_message = target_message.json()
    
    message_edit_program = {
        'token': auth_user['token'],
        'message_id': -1,
        'message': msg2
    }

    response = requests.put(f"{BASE_URL}/message/edit/v1",json = message_edit_program)

    assert response.status_code == 400

def test_global_owner_can_edit_members_message_channel_http():
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

    msg2 = "edit"
    message_edit_program = {
        'token': user_1['token'],
        'message_id': target_message['message_id'],
        'message': msg2
    }

    response = requests.put(f"{BASE_URL}/message/edit/v1",json = message_edit_program)

    assert response.status_code == 200

def test_original_poster_can_edit_message_channel_http():
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

    msg2 = "edit"
    message_edit_program = {
        'token': user_2['token'],
        'message_id': target_message['message_id'],
        'message': msg2
    }

    response = requests.put(f"{BASE_URL}/message/edit/v1",json = message_edit_program)

    assert response.status_code == 200

def test_nonowner_nonposter_cant_edit_http():
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


    channel_invites_param_1 = {
        'token': user_1['token'],
        'channel_id': channel['channel_id'],
        'u_id': user_2['auth_user_id']
    }
    
    requests.post(f"{BASE_URL}/channel/invite/v2", json = channel_invites_param_1)

    msg = "test"
    message_send_program = {
        'token': user_2['token'],
        'channel_id': channel['channel_id'],
        'message': msg
    }
    
    target_message = requests.post(f"{BASE_URL}/message/send/v1",json = message_send_program)
    assert target_message.status_code == 200
    target_message = target_message.json()
    
    register_param_3 = {
        "email": "test3@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Johnson"
    }
    user_3 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_3).json()
    
    channel_invites_param_2 = {
        'token': user_1['token'],
        'channel_id': channel['channel_id'],
        'u_id': user_3['auth_user_id']
    }
    
    requests.post(f"{BASE_URL}/channel/invite/v2", json = channel_invites_param_2)

    msg2 = "edit"
    message_edit_program = {
        'token': user_3['token'],
        'message_id': target_message['message_id'],
        'message': msg2
    }

    response = requests.put(f"{BASE_URL}/message/edit/v1",json = message_edit_program)

    assert response.status_code == 403

def test_original_poster_can_edit_message_dm_http():
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
    
    msg_1 = "test"
    msg_2 = "edit"
    
    dm_send_program = {
        'token': user_2['token'],
        'dm_id': dm['dm_id'],
        'message': msg_1
    }
    target_dm = requests.post(f"{BASE_URL}/message/senddm/v1",json = dm_send_program).json()

    dm_edit_program = {
        'token': user_2['token'],
        'message_id': target_dm['message_id'],
        'message': msg_2
    }

    response = requests.put(f"{BASE_URL}/message/edit/v1",json = dm_edit_program)

    assert response.status_code == 200
    
def test_global_owner_cant_edit_members_message_dm_http():
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
    
    msg_1 = "test"
    msg_2 = "edit"
    
    dm_send_program = {
        'token': user_3['token'],
        'dm_id': dm['dm_id'],
        'message': msg_1
    }
    
    target_dm = requests.post(f"{BASE_URL}/message/senddm/v1",json = dm_send_program).json()

    dm_edit_program = {
        'token': user_1['token'],
        'message_id': target_dm['message_id'],
        'message': msg_2
    }

    response = requests.put(f"{BASE_URL}/message/edit/v1",json = dm_edit_program)

    assert response.status_code == 403

def test_owner_can_edit_members_message_dm_http():    
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
    
    msg_1 = "test"
    msg_2 = "edit"
    
    dm_send_program = {
        'token': user_2['token'],
        'dm_id': dm['dm_id'],
        'message': msg_1
    }
    
    target_dm = requests.post(f"{BASE_URL}/message/senddm/v1",json = dm_send_program).json()

    dm_edit_program = {
        'token': user_3['token'],
        'message_id': target_dm['message_id'],
        'message': msg_2
    }

    response = requests.put(f"{BASE_URL}/message/edit/v1",json = dm_edit_program)

    assert response.status_code == 200
    
def test_edit_invalid_dm_id_http():
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
    
    msg_1 = "test"
    msg_2 = "edit"
    
    dm_send_program = {
        'token': user_2['token'],
        'dm_id': dm['dm_id'],
        'message': msg_1
    }
    
    requests.post(f"{BASE_URL}/message/senddm/v1",json = dm_send_program).json()

    dm_edit_program = {
        'token': user_3['token'],
        'message_id': -1,
        'message': msg_2
    }

    response = requests.put(f"{BASE_URL}/message/edit/v1",json = dm_edit_program)

    assert response.status_code == 400  

