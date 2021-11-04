import requests
import pytest
from src import config
import time

BASE_URL = config.url

def test_msg_future():
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

    future_time = time.time() + 1
    message_sendlater_program = {
        'token': auth_user['token'],
        'channel_id': channel['channel_id'],
        'message': "test",
        'time_sent': future_time
    }

    response = requests.post(f"{BASE_URL}/message/sendlater/v1",json = message_sendlater_program)
    assert response.status_code == 200
    msg_return = response.json()
    
    channel_messages = {
        'token': auth_user['token'],
        'channel_id': channel['channel_id'],
        'start': 0       
    }
    chan_msg_return = requests.get(f"{BASE_URL}/channel/messages/v2",params = channel_messages)
    msg_return = chan_msg_return.json()
    assert chan_msg_return.status_code == 200
    assert msg_return['start'] == 0
    assert msg_return['end'] == -1
    #empty because there isn't enough time elapsed for message to be sent in future
    assert msg_return['messages'] == []
    
    # time delay for 1 second, since time future is set 1 second in future
    time.sleep(1)

    channel_messages = {
        'token': auth_user['token'],
        'channel_id': channel['channel_id'],
        'start': 0       
    }
    chan_msg_return = requests.get(f"{BASE_URL}/channel/messages/v2",params = channel_messages)
    msg_return = chan_msg_return.json()
    assert msg_return['messages'][0]['message'] == "test"

def test_msg_invalid_length_too_long():
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
    invalid_msg = ',' * 1001

    future_time = time.time() + 1
    message_sendlater_program = {
        'token': auth_user['token'],
        'channel_id': channel['channel_id'],
        'message': invalid_msg,
        'time_sent': future_time
    }

    response = requests.post(f"{BASE_URL}/message/sendlater/v1",json = message_sendlater_program)
    assert response.status_code == 400

def test_msg_invalid_length_too_short():
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
    invalid_msg = ''

    future_time = time.time() + 1
    message_sendlater_program = {
        'token': auth_user['token'],
        'channel_id': channel['channel_id'],
        'message': invalid_msg,
        'time_sent': future_time
    }

    response = requests.post(f"{BASE_URL}/message/sendlater/v1",json = message_sendlater_program)
    assert response.status_code == 400

def test_msg__invalid_auth_id_http():
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

    channel_param = {
        'token': user1['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json()
    
    future_time = time.time() + 1
    message_sendlater_program = {
        'token': user2['token'],
        'channel_id': channel['channel_id'],
        'message': "test",
        'time_sent': future_time
    }

    response = requests.post(f"{BASE_URL}/message/sendlater/v1",json = message_sendlater_program)
    assert response.status_code == 403
    
def test_msg_invalid_channel_id():
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
    
    invalid_chan_id = channel['channel_id'] + 1

    future_time = time.time() + 1
    message_sendlater_program = {
        'token': user1['token'],
        'channel_id': invalid_chan_id,
        'message': "test",
        'time_sent': future_time
    }

    response = requests.post(f"{BASE_URL}/message/sendlater/v1",json = message_sendlater_program)
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
