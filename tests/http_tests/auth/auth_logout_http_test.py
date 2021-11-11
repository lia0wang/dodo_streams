import pytest
import requests
import pytest
import json


from src import config

BASE_URL = config.url

def test_register_logout():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    register_body = {
        "email": "JoJo@gmail.com", 
        "password": "HermitPurple",
        "name_first": "Joseph", 
        "name_last": "Joestar"
    }
    reg = requests.post(f"{BASE_URL}/auth/register/v2", json = register_body).json()
    
    register_body = {
        "token": reg['token']
    }
    
    logout = requests.post(f"{BASE_URL}/auth/logout/v1", json = register_body)
    assert logout.status_code == 200

def test_register_login_logout():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    register_body = {
        "email": "JoJo@gmail.com", 
        "password": "HermitPurple",
        "name_first": "Joseph", 
        "name_last": "Joestar"
    }
    reg = requests.post(f"{BASE_URL}/auth/register/v2", json = register_body)
    assert reg.status_code == 200

    login_data = {
        "email": "JoJo@gmail.com", 
        "password": "HermitPurple"
    }
    login = requests.post(f"{BASE_URL}/auth/login/v2", json = login_data).json()
    
    token = {
        "token": login['token']
    }

    logout = requests.post(f"{BASE_URL}/auth/logout/v1", json = token)
    assert logout.status_code == 200

def test_function_use_after_logout():
    '''
    Test if the http channels/create/v2 function working properly
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_body = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_body).json()
    token = {
        "token": user['token']
    }
    channel_body = {
        'token': user['token'],
        'name': 'league',
        'is_public': True
    }
    create1 = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_body).json()
    ch_body = {
        "channel_id": create1["channel_id"],
        "token": user['token']
    }
    # log user out
    requests.post(f"{BASE_URL}/auth/logout/v1", json = token)
    # have user create channel
    create = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_body)
    assert create.status_code == 403
    # have user request channel details
    details = requests.get(f"{BASE_URL}/channel/details/v2", params = ch_body)
    assert details.status_code == 403
    # have user change name
    setname_body = {
        "token": user['token'],
        "name_first": "yodude",
        "name_last": "wowzer"
    }
    setname = requests.put(f"{BASE_URL}/user/profile/setname/v1", json = setname_body)
    assert setname.status_code == 403

def test_session_leftover_after_logout():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    register_body1 = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    register =  requests.post(f"{BASE_URL}/auth/register/v2", json = register_body1).json()

    login_data1 = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037"        
    }
    login_1 =  requests.post(f"{BASE_URL}/auth/login/v2", json = login_data1).json()
    token = {
        "token": register['token']
    }
    requests.post(f"{BASE_URL}/auth/logout/v1", json = token)
    channel_body = {
        'token': register['token'],
        'name': 'league',
        'is_public': True
    }
    create = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_body)
    assert create.status_code == 403
    channel_body['token'] = login_1['token']
    create = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_body)
    assert create.status_code == 200

def test_token_not_jwt():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    register_body = {
        "email": "JoJo@gmail.com", 
        "password": "HermitPurple",
        "name_first": "Joseph", 
        "name_last": "Joestar"
    }
    reg = requests.post(f"{BASE_URL}/auth/register/v2", json = register_body).json()
    
    register_body = {
        "token": reg['token'] + "1"
    }
    
    logout = requests.post(f"{BASE_URL}/auth/logout/v1", json = register_body)
    assert logout.status_code == 403

