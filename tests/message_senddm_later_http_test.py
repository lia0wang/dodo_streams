import requests
from src import config
import time

BASE_URL = config.url

def test_dm_future():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    register_param_2 = {
        "email": "test2@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Smith"
    }
    user1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()
    
    register_param_3 = {
        "email": "test3@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Johnson"
    }
    user2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_3).json()

    u_id1 = user1['auth_user_id']
    u_id2 = user2['auth_user_id']
    u_ids = [u_id1,u_id2]

    dm_param = {
        'token': auth_user['token'],
        'u_ids': u_ids
    }
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_param)
    assert dm.status_code == 200
    dm_return = dm.json()
    
    future_time = time.time() + 1
    dm_send_program = {
        'token': auth_user['token'],
        'dm_id': dm_return['dm_id'],
        'message': "test",
        'time_sent': future_time
    }
    response = requests.post(f"{BASE_URL}/message/sendlaterdm/v1", json = dm_send_program)
    assert response.status_code == 200    
    msg_return = response.json()

    dm_messages = {
        'token': auth_user['token'],
        'dm_id': dm_return['dm_id'],
        'start': 0       
    }

    dm_msg_return = requests.get(f"{BASE_URL}/dm/messages/v1", params = dm_messages)

    msg_return = dm_msg_return.json()
    assert dm_msg_return.status_code == 200
    assert msg_return['start'] == 0
    assert msg_return['end'] == -1
    #empty because there isn't enough time elapsed for message to be sent in future
    assert msg_return['messages'] == []
    
    # time delay for 1 second, since time future is set 1 second in future
    time.sleep(1)

    dm_messages = {
        'token': auth_user['token'],
        'dm_id': dm_return['dm_id'],
        'start': 0       
    }
    dm_msg_return = requests.get(f"{BASE_URL}/dm/messages/v1", params = dm_messages)
    msg_return = dm_msg_return.json()
    assert msg_return['messages'][0]['message'] == "test"

def test_dm_invalid_length_too_long():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    register_param_2 = {
        "email": "test2@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Smith"
    }
    user1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()
    
    register_param_3 = {
        "email": "test3@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Johnson"
    }
    user2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_3).json()

    u_id1 = user1['auth_user_id']
    u_id2 = user2['auth_user_id']
    u_ids = [u_id1,u_id2]

    dm_param = {
        'token': auth_user['token'],
        'u_ids': u_ids
    }
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_param).json()
    
    invalid_msg = ',' * 1001
    future_time = time.time() + 1
    dm_send_program = {
        'token': auth_user['token'],
        'dm_id': dm['dm_id'],
        'message': invalid_msg,
        'time_sent': future_time
    }
    time.sleep(1)
    response = requests.post(f"{BASE_URL}/message/sendlaterdm/v1", json = dm_send_program)
    assert response.status_code == 400

def test_dm_invalid_length_too_short():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    register_param_2 = {
        "email": "test2@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Smith"
    }
    user1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()
    
    register_param_3 = {
        "email": "test3@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Johnson"
    }
    user2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_3).json()

    u_id1 = user1['auth_user_id']
    u_id2 = user2['auth_user_id']
    u_ids = [u_id1,u_id2]

    dm_param = {
        'token': auth_user['token'],
        'u_ids': u_ids
    }
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_param).json()
    
    invalid_msg = ''
    future_time = time.time() + 1
    dm_send_program = {
        'token': auth_user['token'],
        'dm_id': dm['dm_id'],
        'message': invalid_msg,
        'time_sent': future_time
    }

    response = requests.post(f"{BASE_URL}/message/sendlaterdm/v1", json = dm_send_program)
    assert response.status_code == 400
    time.sleep(1)

def test_dm__invalid_auth_id_http():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    user1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    register_param_2 = {
        "email": "test2@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Smith"
    }
    user2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()

    register_param_3 = {
        "email": "test3@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Johnson"
    }
    user3 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_3).json()

    u_id2 = user2['auth_user_id']

    u_ids = [u_id2]
    
    dm_param = {
        'token': user1['token'],
        'u_ids': u_ids
    }
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_param).json()
    
    msg = "test"
    future_time = time.time() + 1
    dm_send_program_1 = {
        'token': user2['token'],
        'dm_id': dm['dm_id'],
        'message': msg,
        'time_sent': future_time
    }

    response_1 = requests.post(f"{BASE_URL}/message/sendlaterdm/v1",json = dm_send_program_1)
    assert response_1.status_code == 200

    dm_send_program_2 = {
        'token': user3['token'],
        'dm_id': dm['dm_id'],
        'message': msg,
        'time_sent': future_time
    }

    response_2 = requests.post(f"{BASE_URL}/message/sendlaterdm/v1",json = dm_send_program_2)
    assert response_2.status_code == 403
    time.sleep(1)

def test_dm_invalid_dm_http():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    register_param_2 = {
        "email": "test2@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Smith"
    }
    user1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()
    
    register_param_3 = {
        "email": "test3@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Johnson"
    }
    user2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_3).json()

    u_id1 = user1['auth_user_id']
    u_id2 = user2['auth_user_id']
    u_ids = [u_id1,u_id2]

    dm_param = {
        'token': auth_user['token'],
        'u_ids': u_ids
    }
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_param)
    assert dm.status_code == 200
    dm_return = dm.json()
    
    future_time = time.time() + 1
    dm_send_program = {
        'token': auth_user['token'],
        'dm_id': dm_return['dm_id'],
        'message': "test",
        'time_sent': future_time
    }
    time.sleep(1)
    response = requests.post(f"{BASE_URL}/message/sendlaterdm/v1", json = dm_send_program)
    assert response.status_code == 400    

def test_time_sent_is_past():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    user1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    channel_param = {
        'token': user1['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json()
    
    future_time = time.time() - 1
    message_sendlater_program = {
        'token': user1['token'],
        'channel_id': channel['channel_id'],
        'message': "test",
        'time_sent': future_time
    }

    response = requests.post(f"{BASE_URL}/message/sendlater/v1",json = message_sendlater_program)
    assert response.status_code == 400