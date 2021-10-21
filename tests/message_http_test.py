import requests

from src.message import send_v1, senddm_v1

BASE_URL = 'http://localhost:8080'

def invalid_length_too_long():
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
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param)
    invalid_msg = ',' * 1001

    message_send_program = {
        'token': auth_user['token'],
        'channel_id': channel['channel_id']
        'message': invalid_msg
    }
   response = requests.post(f"{BASE_URL}/message/send/v1", json = message_send_program)
   

   assert response.status_code == 400

def invalid_length_too_short():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param = {
        "email": "test@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()
    
    channel_param = {
        'token': user['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param)
    
    invalid_msg = ''

    message_send_program = {
        'token': auth_user['token'],
        'channel_id': channel['channel_id']
        'message': invalid_msg
    }
   response = requests.post(f"{BASE_URL}/message/send/v1", json = message_send_program)
   assert response.status_code == 400

   def invalid_length_dm_too_short():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    register_param_2 = {
        "email": "test2@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Smith"
    }
    user1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()
    
    register_param_3 = {
        "email": "test3@gmail.com",
        "password": "abcd1234",
        "name_first": "Agent",
        "name_last": "Johnson"
    }
    user2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    u_id1 = user2['auth_user_id']
    u_id2 = user3['auth_user_id']
    u_ids = [u_id1,u_id2]
    
    dm_param = {
        'dm_id': dm_id,
        'dm_name': dm_name,
        'auth_user_id': auth_user_id,
        'u_ids': u_ids,
        'messages': []
    }
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = channel_param)
    
    invalid_msg = ''

    dm_send_program = {
        'token': auth_user['token'],
        'dm_id': dm['dm_id']
        'message': invalid_msg
    }
   response = requests.post(f"{BASE_URL}/message/senddm/v1", json = dm_send_program)
   assert response.status_code == 400
