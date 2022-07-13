import requests
from src import config

BASE_URL = config.url

def test_http_invalid_channel_id():
    '''
    Test when the channel_id is invalid
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})

    register_param = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    owner = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    channel_param = {
        'token': owner['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json() 

    register_param_1 = {
        "email": "liaowang@gmail.com",
        "password": "liaowang0207",
        "name_first": "wang",
        "name_last": "liao"
    }
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    channel_join_param = {
        'token': user['token'],
        'channel_id': channel['channel_id']
    }
    requests.post(f"{BASE_URL}/channel/join/v2", json = channel_join_param)

    channel_addowner_param = {
        'token': owner['token'],
        'channel_id': channel['channel_id'],
        'u_id': user['auth_user_id']
    }
    requests.post(f"{BASE_URL}/channel/addowner/v1", json = channel_addowner_param)

    channel_removeowner_praram = {
        'token': owner['token'],
        'channel_id': channel['channel_id'] + 999,
        'u_id': user['auth_user_id']
    }
    response = requests.post(f"{BASE_URL}/channel/removeowner/v1", json = channel_removeowner_praram)
    assert response.status_code == 400

def test_invalid_user_id():
    '''
    Test when the user id is invalid
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})

    register_param = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    owner = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    channel_param = {
        'token': owner['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json() 

    register_param_1 = {
        "email": "liaowang@gmail.com",
        "password": "liaowang0207",
        "name_first": "wang",
        "name_last": "liao"
    }
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    channel_join_param = {
        'token': user['token'],
        'channel_id': channel['channel_id']
    }
    requests.post(f"{BASE_URL}/channel/join/v2", json = channel_join_param)

    channel_addowner_param = {
        'token': owner['token'],
        'channel_id': channel['channel_id'],
        'u_id': user['auth_user_id']
    }
    requests.post(f"{BASE_URL}/channel/addowner/v1", json = channel_addowner_param)

    channel_removeowner_praram = {
        'token': owner['token'],
        'channel_id': channel['channel_id'],
        'u_id': user['auth_user_id'] + 999
    }
    response = requests.post(f"{BASE_URL}/channel/removeowner/v1", json = channel_removeowner_praram)
    assert response.status_code == 400

def test_http_non_exist_user():
    '''
    Test when the user who is not an owner of the channel
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})

    register_param = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    owner = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    channel_param = {
        'token': owner['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json() 

    register_param_1 = {
        "email": "liaowang@gmail.com",
        "password": "liaowang0207",
        "name_first": "wang",
        "name_last": "liao"
    }
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    channel_join_param = {
        'token': user['token'],
        'channel_id': channel['channel_id']
    }
    requests.post(f"{BASE_URL}/channel/join/v2", json = channel_join_param)

    channel_removeowner_praram = {
        'token': owner['token'],
        'channel_id': channel['channel_id'],
        'u_id': user['auth_user_id']
    }
    response = requests.post(f"{BASE_URL}/channel/removeowner/v1", json = channel_removeowner_praram)
    assert response.status_code == 400

def test_http_remove_only_owner():
    '''
    Test when the user is the only owner of the channel
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})

    register_param = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    owner = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    channel_param = {
        'token': owner['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json() 

    register_param_1 = {
        "email": "liaowang@gmail.com",
        "password": "liaowang0207",
        "name_first": "wang",
        "name_last": "liao"
    }
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    channel_join_param = {
        'token': user['token'],
        'channel_id': channel['channel_id']
    }
    requests.post(f"{BASE_URL}/channel/join/v2", json = channel_join_param)

    channel_addowner_praram = {
        'token': owner['token'],
        'channel_id': channel['channel_id'],
        'u_id': user['auth_user_id']
    }
    requests.post(f"{BASE_URL}/channel/addowner/v1", json = channel_addowner_praram)

    channel_removeowner_praram = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'u_id': owner['auth_user_id']
    }
    requests.post(f"{BASE_URL}/channel/removeowner/v1", json = channel_removeowner_praram)

    channel_removeowner_praram_1 = {
        'token': owner['token'],
        'channel_id': channel['channel_id'],
        'u_id': user['auth_user_id']
    }
    response = requests.post(f"{BASE_URL}/channel/removeowner/v1", json = channel_removeowner_praram_1)
    assert response.status_code == 400

    channel_removeowner_praram_2 = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'u_id': user['auth_user_id']
    }
    response = requests.post(f"{BASE_URL}/channel/removeowner/v1", json = channel_removeowner_praram_2)
    assert response.status_code  == 400

def test_http_no_permission():
    '''
    Test when the auth user has no owner permission
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})

    register_param = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    owner = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    channel_param = {
        'token': owner['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json() 

    register_param_1 = {
        "email": "liaowang@gmail.com",
        "password": "liaowang0207",
        "name_first": "wang",
        "name_last": "liao"
    }
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    channel_join_param = {
        'token': user['token'],
        'channel_id': channel['channel_id']
    }
    requests.post(f"{BASE_URL}/channel/join/v2", json = channel_join_param)

    register_param_2 = {
        "email": "fsbkahj@gmail.com",
        "password": "flkansfkn2ou31",
        "name_first": "haha",
        "name_last": "haha"
    }
    new_user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()

    channel_join_param_1 = {
        'token': new_user['token'],
        'channel_id': channel['channel_id']
    }
    requests.post(f"{BASE_URL}/channel/join/v2", json = channel_join_param_1)

    channel_addowner_praram = {
        'token': owner['token'],
        'channel_id': channel['channel_id'],
        'u_id': new_user['auth_user_id']
    }
    requests.post(f"{BASE_URL}/channel/addowner/v1", json = channel_addowner_praram)

    channel_removeowner_praram = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'u_id': new_user['auth_user_id']
    }
    response = requests.post(f"{BASE_URL}/channel/removeowner/v1", json = channel_removeowner_praram)
    assert response.status_code  == 403

def test_http_channel_removeowner_basic():
    '''
    Test if channel/removeowner/v1 working properly
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})

    register_param = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    owner = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    channel_param = {
        'token': owner['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json() 

    register_param_1 = {
        "email": "liaowang@gmail.com",
        "password": "liaowang0207",
        "name_first": "wang",
        "name_last": "liao"
    }
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    channel_param2 = {
        'token': user['token'],
        'name': 'league',
        'is_public': True
    }
    channel2 = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param2).json() 
    
    channel_join_param = {
        'token': owner['token'],
        'channel_id': channel2['channel_id']
    }
    requests.post(f"{BASE_URL}/channel/join/v2", json = channel_join_param)

    channel_addowner_praram_1 = {
        'token': user['token'],
        'channel_id': channel2['channel_id'],
        'u_id': owner['auth_user_id']
    }
    requests.post(f"{BASE_URL}/channel/addowner/v1", json = channel_addowner_praram_1)

    channel_removeowner_praram_1 = {
        'token': user['token'],
        'channel_id': channel2['channel_id'],
        'u_id': owner['auth_user_id']
    }
    response = requests.post(f"{BASE_URL}/channel/removeowner/v1", json = channel_removeowner_praram_1)
    assert response.status_code  == 200

    channel_join_param = {
        'token': user['token'],
        'channel_id': channel['channel_id']
    }
    requests.post(f"{BASE_URL}/channel/join/v2", json = channel_join_param)

    register_param_2 = {
        "email": "fsbkahj@gmail.com",
        "password": "flkansfkn2ou31",
        "name_first": "haha",
        "name_last": "haha"
    }
    new_user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()

    channel_join_param_1 = {
        'token': new_user['token'],
        'channel_id': channel['channel_id']
    }
    requests.post(f"{BASE_URL}/channel/join/v2", json = channel_join_param_1)

    channel_addowner_praram_1 = {
        'token': owner['token'],
        'channel_id': channel['channel_id'],
        'u_id': user['auth_user_id']
    }
    requests.post(f"{BASE_URL}/channel/addowner/v1", json = channel_addowner_praram_1)

    channel_addowner_praram_2 = {
        'token': owner['token'],
        'channel_id': channel['channel_id'],
        'u_id': new_user['auth_user_id']
    }
    requests.post(f"{BASE_URL}/channel/addowner/v1", json = channel_addowner_praram_2)

    channel_removeowner_praram_1 = {
        'token': owner['token'],
        'channel_id': channel['channel_id'],
        'u_id': user['auth_user_id']
    }
    response = requests.post(f"{BASE_URL}/channel/removeowner/v1", json = channel_removeowner_praram_1)
    assert response.status_code  == 200

    channel_removeowner_praram_2 = {
        'token': owner['token'],
        'channel_id': channel['channel_id'],
        'u_id': new_user['auth_user_id']
    }
    response = requests.post(f"{BASE_URL}/channel/removeowner/v1", json = channel_removeowner_praram_2)
    assert response.status_code  == 200

def test_http_invalid_token():
    '''
    Testing whether the v2 function can identify incorrect tokens
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    invalid_user_json = {
        "email": "bob123@gmail.com",
        "password": "bobahe",
        "name_first": "Bob",
        "name_last": "Marley"
    }
    
    invalid = requests.post(f"{BASE_URL}/auth/register/v2", json = invalid_user_json).json()
    
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    user_1_json = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = user_1_json).json()

    channel_json = {
        'token': user['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_json).json()
    
    channel_removeowner_praram = {
        'token': invalid['token'],
        'channel_id': channel['channel_id'],
        'u_id': user['auth_user_id']
    }
    response = requests.post(f"{BASE_URL}/channel/removeowner/v1", json = channel_removeowner_praram)

    assert response.status_code == 403

def test_http_non_member_auth():
    '''
    Test if the auth user who is a member of the channel
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})

    register_param = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    owner = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    channel_param = {
        'token': owner['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json() 

    register_param_1 = {
        "email": "liaowang@gmail.com",
        "password": "liaowang0207",
        "name_first": "wang",
        "name_last": "liao"
    }
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    channel_removeowner_praram = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'u_id': user['auth_user_id']
    }
    response = requests.post(f"{BASE_URL}/channel/removeowner/v1", json = channel_removeowner_praram)
    assert response.status_code == 403
