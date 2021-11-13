import requests
import time
from src import config

BASE_URL = config.url

def test_channel_invite_notif():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})

    register_param_1 = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    channel_param = {
        'token': user_1['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json() 

    register_param_2 = {
        "email": "z5306312@gmail.com",
        "password": "LeonLiao123",
        "name_first": "Leon",
        "name_last": "Liao"
    }
    user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()
    
    channel_invites_param = {
        'token': user_1['token'],
        'channel_id': channel['channel_id'],
        'u_id': user_2['auth_user_id']
    }
    response = requests.post(f"{BASE_URL}/channel/invite/v2", json = channel_invites_param)
    assert response.status_code == 200

    token = {
        'token': user_2['token']
    }
    
    response = requests.get(f"{BASE_URL}/notifications/get/v1", params = token)
    assert response.status_code == 200
    notif = response.json()
    assert notif['notifications'][0]['channel_id'] == 1
    assert notif['notifications'][0]['dm_id'] == -1
    assert notif['notifications'][0]['notification_message'] == \
        'added to a channel/DM: hopefulboyyy added you to league'

def test_dm_create_notif():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param = {
        "email": "shifanchen@gmail.com",
        "password": "djkadldjsa21",
        "name_first": "shifan",
        "name_last": "chen"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    register_param_1 = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    register_param_2 = {
        "email": "z5306312@gmail.com",
        "password": "LeonLiao123",
        "name_first": "Leon",
        "name_last": "Liao"
    }
    user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()

    dm_create_param = {
        "token": auth_user["token"],
        "u_ids": [user_1["auth_user_id"], user_2["auth_user_id"]]
    }

    requests.post(f"{BASE_URL}/dm/create/v1", json = dm_create_param)


    token = {
        'token': user_2['token']
    }

    response = requests.get(f"{BASE_URL}/notifications/get/v1", params = token)
    assert response.status_code == 200
    notif = response.json()
    assert notif['notifications'][0]['channel_id'] == -1
    assert notif['notifications'][0]['dm_id'] == 1
    assert notif['notifications'][0]['notification_message'] == \
        'added to a channel/DM: shifanchen added you to hopefulboyyy, leonliao, shifanchen'

def test_react_notif():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    # Creating users
    user_json_1 = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = user_json_1).json()

    user_json_2 = {
        "email": "bob123@gmail.com",
        "password": "bobahe",
        "name_first": "Bob",
        "name_last": "Marley"
    }
    user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_json_2).json()
    
    # Creating and joining channel
    channel_json_1 = {
        'token': auth_user['token'],
        'name': 'league1',
        'is_public': True
    }
    channel_1 = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_json_1).json()
    
    join_json = {
        'token': user_2['token'],
        'channel_id': channel_1['channel_id']
    }
    requests.post(f"{BASE_URL}/channel/join/v2", json = join_json)

    # Sending message
    message_info_json = {
        'token': auth_user['token'],
        'channel_id': channel_1['channel_id'],
        'message': "Hello"
    }
    message = requests.post(f"{BASE_URL}/message/send/v1", json = message_info_json).json()

    # Reacting to message and checking if reacted to
    message_react_json = {
        'token': auth_user['token'],
        'message_id': message['message_id'],
        'react_id': 1,
    }
    response = requests.post(f"{BASE_URL}/message/react/v1", json = message_react_json)

    token = {
        'token': auth_user['token']
    }

    response = requests.get(f"{BASE_URL}/notifications/get/v1", params = token)
    assert response.status_code == 200
    notif = response.json()
    assert notif['notifications'][0]['channel_id'] == 1
    assert notif['notifications'][0]['dm_id'] == -1
    assert notif['notifications'][0]['notification_message'] == \
        'hopefulboyyy reacted to your message in league1'

def test_msg_normal_notif():
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
    msg = "hi @johnsmith, how are @johnsmith, you@johnsmith"

    message_send_program = {
        'token': auth_user['token'],
        'channel_id': channel['channel_id'],
        'message': msg
    }

    response = requests.post(f"{BASE_URL}/message/send/v1",json = message_send_program)
    assert response.status_code == 200    

    token = {
        'token': auth_user['token']
    }

    response = requests.get(f"{BASE_URL}/notifications/get/v1", params = token)
    assert response.status_code == 200
    notif = response.json()
    assert notif['notifications'][0]['channel_id'] == 1
    assert notif['notifications'][0]['dm_id'] == -1
    assert notif['notifications'][0]['notification_message'] == \
        'johnsmith tagged you in league: hi @johnsmith, how a'

def test_dm_normal_notif():
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
    
    msg = "@agentsmith"

    dm_send_program = {
        'token': auth_user['token'],
        'dm_id': dm['dm_id'],
        'message': msg
    }
    response = requests.post(f"{BASE_URL}/message/senddm/v1", json = dm_send_program)
    assert response.status_code == 200  

    token = {
        'token': user1['token']
    }

    response = requests.get(f"{BASE_URL}/notifications/get/v1", params = token)
    assert response.status_code == 200
    notif = response.json()
    assert notif['notifications'][0]['channel_id'] == -1
    assert notif['notifications'][0]['dm_id'] == 1
    assert notif['notifications'][0]['notification_message'] == \
        'johnsmith tagged you in agentjohnson, agentsmith, johnsmith: @agentsmith'

def test_msg_edit_basics_channel_notif():
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
    
    msg2 = "@johnsmith"
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

    token = {
        'token': auth_user['token']
    }

    response = requests.get(f"{BASE_URL}/notifications/get/v1", params = token)
    assert response.status_code == 200
    notif = response.json()
    assert notif['notifications'][0]['channel_id'] == 1
    assert notif['notifications'][0]['dm_id'] == -1
    assert notif['notifications'][0]['notification_message'] == \
        'johnsmith tagged you in league: @johnsmith'

def test_msg_edit_basics_dms_notif():
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
    msg_2 = "edited @agentjohnson hi"
    
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

    token = {
        'token': user_3['token']
    }

    response = requests.get(f"{BASE_URL}/notifications/get/v1", params = token)
    assert response.status_code == 200
    notif = response.json()
    assert notif['notifications'][0]['channel_id'] == -1
    assert notif['notifications'][0]['dm_id'] == 1
    assert notif['notifications'][0]['notification_message'] == \
        'agentsmith tagged you in agentjohnson, agentsmith, johnsmith: edited @agentjohnson'

def test_dm_future_notif():
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
    
    future_time = time.time() + 0.1
    dm_send_program = {
        'token': auth_user['token'],
        'dm_id': dm_return['dm_id'],
        'message': "@agentsmith well done my brother",
        'time_sent': future_time
    }
    response = requests.post(f"{BASE_URL}/message/sendlaterdm/v1", json = dm_send_program)
    assert response.status_code == 200    

    # time delay for 1 second, since time future is set 1 second in future
    time.sleep(0.1)

    token = {
        'token': user1['token']
    }

    response = requests.get(f"{BASE_URL}/notifications/get/v1", params = token)
    assert response.status_code == 200
    notif = response.json()
    assert notif['notifications'][0]['channel_id'] == -1
    assert notif['notifications'][0]['dm_id'] == 1
    assert notif['notifications'][0]['notification_message'] == \
        'johnsmith tagged you in agentjohnson, agentsmith, johnsmith: @agentsmith well don'

def test_msg_future_notif():
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

    future_time = time.time() + 0.1
    message_sendlater_program = {
        'token': auth_user['token'],
        'channel_id': channel['channel_id'],
        'message': "@johnsmith do u know dae waay?",
        'time_sent': future_time
    }

    response = requests.post(f"{BASE_URL}/message/sendlater/v1",json = message_sendlater_program)
    assert response.status_code == 200
    
    # time delay for 1 second, since time future is set 1 second in future
    time.sleep(0.1)

    token = {
        'token': auth_user['token']
    }

    response = requests.get(f"{BASE_URL}/notifications/get/v1", params = token)
    assert response.status_code == 200
    notif = response.json()
    assert notif['notifications'][0]['channel_id'] == 1
    assert notif['notifications'][0]['dm_id'] == -1
    assert notif['notifications'][0]['notification_message'] == \
        'johnsmith tagged you in league: @johnsmith do u know'
