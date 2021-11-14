import requests
from src import config
import time

BASE_URL = config.url

def test_share_channel_source_basic_http():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    user_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_1).json()

    user_param_2 = {
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
        'token': user_1['token'],
        'channel_id': channel['channel_id'],
        'message': msg_1
    }
    msg_send = requests.post(f"{BASE_URL}/message/send/v1", json = message_send_program)
    assert msg_send.status_code == 200
    msg_return = msg_send.json()
    
    user_param_3 = {
        "email": "test3@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Johnson"
    }
    user_3 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_3).json()

    u_id_2 = user_2['auth_user_id']
    u_ids = [u_id_2]

    dm_param = {
        'token': user_3['token'],
        'u_ids': u_ids
    }
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_param)
    assert dm.status_code == 200
    dm_return = dm.json()

    msg_2 = 'share'
    message_share_param_1 = {
        'token': user_2['token'],
        'og_message_id': msg_return['message_id'],
        'message': msg_2,
        'channel_id': -1,
        'dm_id': dm_return['dm_id']
        }
    message_share_1 = requests.post(f"{BASE_URL}/message/share/v1", json = message_share_param_1)
    assert message_share_1.status_code == 200

    message_share_param_2 = {
        'token': user_2['token'],
        'og_message_id': msg_return['message_id'],
        'message': msg_2,
        'channel_id': channel['channel_id'],
        'dm_id': -1
        }
    message_share_2 = requests.post(f"{BASE_URL}/message/share/v1", json = message_share_param_2)
    assert message_share_2.status_code == 200

def test_share_source_dm_basic_http():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    user_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_1).json()

    user_param_2 = {
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
    
    user_param_3 = {
        "email": "test3@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Johnson"
    }
    user_3 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_3).json()

    u_id_2 = user_2['auth_user_id']
    u_ids = [u_id_2]

    dm_param = {
        'token': user_3['token'],
        'u_ids': u_ids
    }
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_param)
    assert dm.status_code == 200
    dm_return = dm.json()
        
    msg_1 = 'test'
    
    dm_send_program = {
        'token': user_3['token'],
        'dm_id': dm_return['dm_id'],
        'message': msg_1
    }
    dm_send = requests.post(f"{BASE_URL}/message/senddm/v1", json = dm_send_program)
    assert dm_send.status_code == 200
    senddm_return = dm_send.json()

    msg_2 = 'share'
    message_share_param_1 = {
        'token': user_2['token'],
        'og_message_id': senddm_return['message_id'],
        'message': msg_2,
        'channel_id': -1,
        'dm_id': dm_return['dm_id']
        }
    message_share_1 = requests.post(f"{BASE_URL}/message/share/v1", json = message_share_param_1)
    assert message_share_1.status_code == 200

    message_share_param_2 = {
        'token': user_2['token'],
        'og_message_id': senddm_return['message_id'],
        'message': msg_2,
        'channel_id': channel['channel_id'],
        'dm_id': -1
        }
    message_share_2 = requests.post(f"{BASE_URL}/message/share/v1", json = message_share_param_2)
    assert message_share_2.status_code == 200

def test_share_invalid_length():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    user_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_1).json()

    user_param_2 = {
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
    
    user_param_3 = {
        "email": "test3@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Johnson"
    }
    user_3 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_3).json()

    u_id_2 = user_2['auth_user_id']
    u_ids = [u_id_2]

    dm_param = {
        'token': user_3['token'],
        'u_ids': u_ids
    }
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_param)
    assert dm.status_code == 200
    dm_return = dm.json()
        
    msg_1 = 'test'
    
    dm_send_program = {
        'token': user_3['token'],
        'dm_id': dm_return['dm_id'],
        'message': msg_1
    }
    dm_send = requests.post(f"{BASE_URL}/message/senddm/v1", json = dm_send_program)
    assert dm_send.status_code == 200
    senddm_return = dm_send.json()

    msg_2 = ','*1001
    message_share_param = {
        'token': user_2['token'],
        'og_message_id': senddm_return['message_id'],
        'message': msg_2,
        'channel_id': channel['channel_id'],
        'dm_id': -1
        }
    message_share = requests.post(f"{BASE_URL}/message/share/v1", json = message_share_param)
    assert message_share.status_code == 400 

def test_share_undirected_1_http():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    user_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_1).json()

    user_param_2 = {
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
        'token': user_1['token'],
        'channel_id': channel['channel_id'],
        'message': msg_1
    }
    msg_send = requests.post(f"{BASE_URL}/message/send/v1", json = message_send_program)
    assert msg_send.status_code == 200
    msg_return = msg_send.json()
    
    user_param_3 = {
        "email": "test3@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Johnson"
    }
    user_3 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_3).json()

    u_id_2 = user_2['auth_user_id']
    u_ids = [u_id_2]

    dm_param = {
        'token': user_3['token'],
        'u_ids': u_ids
    }
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_param)
    assert dm.status_code == 200

    msg_2 = 'share'
    message_share_param = {
        'token': user_2['token'],
        'og_message_id': msg_return['message_id'],
        'message': msg_2,
        'channel_id': -1,
        'dm_id': -1
        }
    message_share = requests.post(f"{BASE_URL}/message/share/v1", json = message_share_param)
    assert message_share.status_code == 400

def test_share_undirected_2():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    user_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_1).json()

    user_param_2 = {
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
        'token': user_1['token'],
        'channel_id': channel['channel_id'],
        'message': msg_1
    }
    msg_send = requests.post(f"{BASE_URL}/message/send/v1", json = message_send_program)
    assert msg_send.status_code == 200
    msg_return = msg_send.json()
    
    user_param_3 = {
        "email": "test3@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Johnson"
    }
    user_3 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_3).json()

    u_id_2 = user_2['auth_user_id']
    u_ids = [u_id_2]

    dm_param = {
        'token': user_3['token'],
        'u_ids': u_ids
    }
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_param)
    assert dm.status_code == 200
    dm_return = dm.json()

    msg_2 = 'share'
    message_share_param = {
        'token': user_2['token'],
        'og_message_id': msg_return['message_id'],
        'message': msg_2,
        'channel_id': channel['channel_id'],
        'dm_id': dm_return['dm_id']
        }
    message_share = requests.post(f"{BASE_URL}/message/share/v1", json = message_share_param)
    assert message_share.status_code == 400

def test_share_not_source_channel_member_http():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    user_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_1).json()

    user_param_2 = {
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
        'token': user_1['token'],
        'channel_id': channel['channel_id'],
        'message': msg_1
    }
    msg_send = requests.post(f"{BASE_URL}/message/send/v1", json = message_send_program)
    assert msg_send.status_code == 200
    msg_return = msg_send.json()
    
    user_param_3 = {
        "email": "test3@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Johnson"
    }
    user_3 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_3).json()

    u_id_2 = user_2['auth_user_id']
    u_ids = [u_id_2]

    dm_param = {
        'token': user_3['token'],
        'u_ids': u_ids
    }
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_param)
    assert dm.status_code == 200
    dm_return = dm.json()

    msg_2 = 'share'
    message_share_param = {
        'token': user_3['token'],
        'og_message_id': msg_return['message_id'],
        'message': msg_2,
        'channel_id': -1,
        'dm_id': dm_return['dm_id']
        }
    message_share = requests.post(f"{BASE_URL}/message/share/v1", json = message_share_param)
    assert message_share.status_code == 400

def test_share_not_source_dm_member_http():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    user_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_1).json()

    user_param_2 = {
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
    
    user_param_3 = {
        "email": "test3@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Johnson"
    }
    user_3 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_3).json()

    u_id_2 = user_2['auth_user_id']
    u_ids = [u_id_2]

    dm_param = {
        'token': user_3['token'],
        'u_ids': u_ids
    }
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_param)
    assert dm.status_code == 200
    dm_return = dm.json()
        
    msg_1 = 'test'
    
    dm_send_program = {
        'token': user_3['token'],
        'dm_id': dm_return['dm_id'],
        'message': msg_1
    }
    dm_send = requests.post(f"{BASE_URL}/message/senddm/v1", json = dm_send_program)
    assert dm_send.status_code == 200
    senddm_return = dm_send.json()

    msg_2 = 'share'
    message_share_param = {
        'token': user_1['token'],
        'og_message_id': senddm_return['message_id'],
        'message': msg_2,
        'channel_id': channel['channel_id'],
        'dm_id': -1
        }
    message_share = requests.post(f"{BASE_URL}/message/share/v1", json = message_share_param)
    assert message_share.status_code == 400     

def test_share_not_target_channel_member_http():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    user_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_1).json()

    user_param_2 = {
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
    
    user_param_3 = {
        "email": "test3@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Johnson"
    }
    user_3 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_3).json()

    u_id_2 = user_2['auth_user_id']
    u_ids = [u_id_2]

    dm_param = {
        'token': user_3['token'],
        'u_ids': u_ids
    }
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_param)
    assert dm.status_code == 200
    dm_return = dm.json()
        
    msg_1 = 'test'
    
    dm_send_program = {
        'token': user_3['token'],
        'dm_id': dm_return['dm_id'],
        'message': msg_1
    }
    dm_send = requests.post(f"{BASE_URL}/message/senddm/v1", json = dm_send_program)
    assert dm_send.status_code == 200
    senddm_return = dm_send.json()

    msg_2 = 'share'
    message_share_param = {
        'token': user_2['token'],
        'og_message_id': senddm_return['message_id'],
        'message': msg_2,
        'channel_id': channel['channel_id'],
        'dm_id': -1
        }
    message_share = requests.post(f"{BASE_URL}/message/share/v1", json = message_share_param)
    assert message_share.status_code == 403   

def test_share_not_target_dm_member_http():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    user_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_1).json()

    user_param_2 = {
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
        'token': user_1['token'],
        'channel_id': channel['channel_id'],
        'message': msg_1
    }
    msg_send = requests.post(f"{BASE_URL}/message/send/v1", json = message_send_program)
    assert msg_send.status_code == 200
    msg_return = msg_send.json()
    
    user_param_3 = {
        "email": "test3@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Johnson"
    }
    user_3 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_3).json()

    u_id_2 = user_2['auth_user_id']
    u_ids = [u_id_2]

    dm_param = {
        'token': user_3['token'],
        'u_ids': u_ids
    }
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_param)
    assert dm.status_code == 200
    dm_return = dm.json()

    msg_2 = 'share'
    message_share_param = {
        'token': user_1['token'],
        'og_message_id': msg_return['message_id'],
        'message': msg_2,
        'channel_id': -1,
        'dm_id': dm_return['dm_id']
        }
    message_share = requests.post(f"{BASE_URL}/message/share/v1", json = message_share_param)
    assert message_share.status_code == 403

def test_share_invalid_channel_id_http():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    user_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_1).json()

    user_param_2 = {
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
    
    user_param_3 = {
        "email": "test3@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Johnson"
    }
    user_3 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_3).json()

    u_id_2 = user_2['auth_user_id']
    u_ids = [u_id_2]

    dm_param = {
        'token': user_3['token'],
        'u_ids': u_ids
    }
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_param)
    assert dm.status_code == 200
    dm_return = dm.json()
        
    msg_1 = 'test'
    
    dm_send_program = {
        'token': user_3['token'],
        'dm_id': dm_return['dm_id'],
        'message': msg_1
    }
    dm_send = requests.post(f"{BASE_URL}/message/senddm/v1", json = dm_send_program)
    assert dm_send.status_code == 200
    senddm_return = dm_send.json()

    msg_2 = 'share'
    message_share_param = {
        'token': user_2['token'],
        'og_message_id': senddm_return['message_id'],
        'message': msg_2,
        'channel_id': channel['channel_id']+999,
        'dm_id': -1
        }
    message_share = requests.post(f"{BASE_URL}/message/share/v1", json = message_share_param)
    assert message_share.status_code == 400

def test_share_invalid_dm_id_http():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    user_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_1).json()

    user_param_2 = {
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
        'token': user_1['token'],
        'channel_id': channel['channel_id'],
        'message': msg_1
    }
    msg_send = requests.post(f"{BASE_URL}/message/send/v1", json = message_send_program)
    assert msg_send.status_code == 200
    msg_return = msg_send.json()
    
    user_param_3 = {
        "email": "test3@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Johnson"
    }
    user_3 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_3).json()

    u_id_2 = user_2['auth_user_id']
    u_ids = [u_id_2]

    dm_param = {
        'token': user_3['token'],
        'u_ids': u_ids
    }
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_param)
    assert dm.status_code == 200
    dm_return = dm.json()

    msg_2 = 'share'
    message_share_param = {
        'token': user_2['token'],
        'og_message_id': msg_return['message_id'],
        'message': msg_2,
        'channel_id': -1,
        'dm_id': dm_return['dm_id']+999
        }
    message_share = requests.post(f"{BASE_URL}/message/share/v1", json = message_share_param)
    assert message_share.status_code == 400
