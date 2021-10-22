import requests
import pytest
from src import config

BASE_URL = config.url

def test_basic_message_return():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    channel_param = {
        'token': user['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param)
    channel_return = channel.json()

    # 1 user sends 124 messages
    i = 0
    while i < 124:
        msg = 'Hi'
        message_send_program = {
            'token': user['token'],
            'channel_id': channel_return['channel_id'],
            'message': msg
        }
        i+=1
        eg = requests.post(f"{BASE_URL}/message/send/v1",json = message_send_program)
    # running once
        assert eg.status_code == 200

    channel_messages = {
        'token': user['token'],
        'channel_id': channel_return['channel_id'],
        'start': 0       
    }
    chan_msg_return = requests.get(f"{BASE_URL}/channel/messages/v2",json = channel_messages)
    msg_return = chan_msg_return.json()
    assert chan_msg_return.status_code == 200
    assert msg_return['start'] == 0
    assert msg_return['end'] == 50

    # running second for batch 2 of 50 messages
    channel_messages2 = {
        'token': user['token'],
        'channel_id': channel_return['channel_id'],
        'start': 50       
    }
    chan_msg_return2 = requests.get(f"{BASE_URL}/channel/messages/v2",json = channel_messages2)
    msg_return2 = chan_msg_return2.json()
    assert chan_msg_return.status_code == 200
    assert msg_return2['start'] == 50
    assert msg_return2['end'] == 100

    # running second for batch 3 of 50 messages
    channel_messages3 = {
        'token': user['token'],
        'channel_id': channel_return['channel_id'],
        'start': 100      
    }
    chan_msg_return3 = requests.get(f"{BASE_URL}/channel/messages/v2",json = channel_messages3)
    msg_return3 = chan_msg_return3.json()
    assert chan_msg_return.status_code == 200
    assert msg_return3['start'] == 100
    assert msg_return3['index'] == 124
    assert msg_return3['total_msg'] == 124
    assert msg_return3['end'] == -1

def test_total_messages_is_zero():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    channel_param = {
        'token': user['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param)
    channel_return = channel.json()

    channel_messages = {
        'token': user['token'],
        'channel_id': channel_return['channel_id'],
        'start': 0       
    }
    chan_msg_return = requests.get(f"{BASE_URL}/channel/messages/v2",json = channel_messages)
    assert chan_msg_return.status_code == 200
    msg_return = chan_msg_return.json()
    assert chan_msg_return.status_code == 200
    assert msg_return['start'] == 0
    assert msg_return['end'] == -1

def test_total_messages_is_less_than_50():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    channel_param = {
        'token': user['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param)
    channel_return = channel.json()

    channel_messages = {
        'token': user['token'],
        'channel_id': channel_return['channel_id'],
        'start': 0       
    }

    # 1 user sends 49 messages
    i = 0
    while i < 40:
        msg = 'Hi'
        message_send_program = {
            'token': user['token'],
            'channel_id': channel_return['channel_id'],
            'message': msg
        }
        i+=1
        requests.post(f"{BASE_URL}/message/send/v1",json = message_send_program)

    chan_msg_return = requests.get(f"{BASE_URL}/channel/messages/v2",json = channel_messages)
    msg_return = chan_msg_return.json()
    assert chan_msg_return.status_code == 200
    assert msg_return['start'] == 0
    assert msg_return['end'] == -1

def test_total_messages_is_50():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    channel_param = {
        'token': user['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param)
    channel_return = channel.json()

    channel_messages = {
        'token': user['token'],
        'channel_id': channel_return['channel_id'],
        'start': 0       
    }

    # 1 user sends 50 messages
    i = 0
    while i < 50:
        msg = 'Hi'
        message_send_program = {
            'token': user['token'],
            'channel_id': channel_return['channel_id'],
            'message': msg
        }
        i+=1
        requests.post(f"{BASE_URL}/message/send/v1",json = message_send_program)

    chan_msg_return = requests.get(f"{BASE_URL}/channel/messages/v2",json = channel_messages)
    msg_return = chan_msg_return.json()
    assert chan_msg_return.status_code == 200
    assert msg_return['start'] == 0
    assert msg_return['end'] == -1

def test_invalid_channel_id():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    channel_param = {
        'token': user['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param)
    channel_return = channel.json()

    # 1 user sends 124 messages
    i = 0
    while i < 124:
        msg = 'Hi'
        message_send_program = {
            'token': user['token'],
            'channel_id': channel_return['channel_id'],
            'message': msg
        }
        i+=1
        send_msg = requests.post(f"{BASE_URL}/message/send/v1",json = message_send_program)
    # running once
        assert send_msg.status_code == 200

    channel_messages = {
        'token': user['token'],
        'channel_id': channel_return['channel_id'] + 1,
        'start': 0       
    }
    chan_msg_return = requests.get(f"{BASE_URL}/channel/messages/v2",json = channel_messages)
    assert chan_msg_return.status_code == 400

def test_start_more_than_total_messages():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    channel_param = {
        'token': user['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param)
    channel_return = channel.json()

    channel_messages = {
        'token': user['token'],
        'channel_id': channel_return['channel_id'],
        'start': 1       
    }
    chan_msg_return = requests.get(f"{BASE_URL}/channel/messages/v2",json = channel_messages)
    assert chan_msg_return.status_code == 400

def test_channel_id_and_auth_user_id_invalid():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    channel_param = {
        'token': user['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param)
    channel_return = channel.json()

    # logout to make token invalid
    register_param = {
        'token': user['token']
    }
    requests.post(f"{BASE_URL}/auth/logout/v1", json = register_param)

    channel_messages = {
        'token': user['token'],
        'channel_id': channel_return['channel_id'] + 1,
        'start': 1       
    }
    chan_msg_return = requests.get(f"{BASE_URL}/channel/messages/v2",json = channel_messages)
    assert chan_msg_return.status_code == 403

def test_auth_user_id_not_member_of_channel():

    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    channel_param = {
        'token': user['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param)
    channel_return = channel.json()

    # logout to make token invalid
    register_param = {
        'token': user['token']
    }
    requests.post(f"{BASE_URL}/auth/logout/v1", json = register_param)

    channel_messages = {
        'token': user['token'],
        'channel_id': channel_return['channel_id'],
        'start': 1       
    }
    chan_msg_return = requests.get(f"{BASE_URL}/channel/messages/v2",json = channel_messages)
    assert chan_msg_return.status_code == 403
