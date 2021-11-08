import requests
from src import config
BASE_URL = config.url

def test_successful_dm_removal_http():
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

    u_id_1 = user_1['auth_user_id']
    u_id_2 = user_2['auth_user_id']
    u_ids = [u_id_1,u_id_2]

    dm_param = {
        'token': user_3['token'],
        'u_ids': u_ids
    }
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_param).json()

    dm_remove_program = {
        'token': user_3['token'],
        'dm_id': dm['dm_id'],
    } 
    dm_remove = requests.delete(f"{BASE_URL}/dm/remove/v1", json = dm_remove_program)
    assert dm_remove.status_code == 200   
    

def test_nonowner_cannot_remove_dm():
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

    u_id_1 = user_1['auth_user_id']
    u_id_2 = user_1['auth_user_id']
    u_ids = [u_id_1,u_id_2]

    dm_param = {
        'token': user_3['token'],
        'u_ids': u_ids
    }
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_param).json() #Owner is user 3
    
    dm_remove_program = {
        'token': user_2['token'],
        'dm_id': dm['dm_id'],
    } 
    dm_remove = requests.delete(f"{BASE_URL}/dm/remove/v1", json = dm_remove_program)
    assert dm_remove.status_code == 403

def test_dm_remove_invalid_dm_id():
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

    u_id_1 = user_1['auth_user_id']
    u_id_2 = user_2['auth_user_id']
    u_ids = [u_id_1,u_id_2]

    dm_param = {
        'token': user_3['token'],
        'u_ids': u_ids
    }
    requests.post(f"{BASE_URL}/dm/create/v1", json = dm_param).json() #Owner is user 3
    
    dm_remove_program = {
        'token': user_3['token'],
        'dm_id': -1,
    } 
    dm_remove = requests.delete(f"{BASE_URL}/dm/remove/v1", json = dm_remove_program)
    assert dm_remove.status_code == 400

def test_dm_remove_invalid_token():
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

    u_id_1 = user_1['auth_user_id']
    u_ids = [u_id_1]

    dm_param = {
        'token': user_3['token'],
        'u_ids': u_ids
    }
    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_param).json() #Owner is user 3
    
    dm_remove_program = {
        'token': user_2['token'],
        'dm_id': dm['dm_id'],
    } 
    dm_remove = requests.delete(f"{BASE_URL}/dm/remove/v1", json = dm_remove_program)
    assert dm_remove.status_code == 403
