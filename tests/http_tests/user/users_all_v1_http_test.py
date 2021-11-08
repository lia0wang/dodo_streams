import requests
import pytest
from src import config

BASE_URL = config.url
OK = 200
ACCESS_ERROR = 403    
    
def test_invalid_token():
    '''
    Checking output when the token is incorrect
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
    requests.post(f"{BASE_URL}/auth/register/v2", json = user_1_json).json()
    
    token_params = {
        'token': invalid['token'] # Incorrect token
    }
    
    response = requests.get(f"{BASE_URL}/users/all/v1", params = token_params)
    
    assert response.status_code == ACCESS_ERROR
    
def test_single_user():
    '''
    Checking output with only one user
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    user_json = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = user_json).json()
    
    token_params = {
        'token': user['token']
    }
    
    response = requests.get(f"{BASE_URL}/users/all/v1", params = token_params)
    
    assert response.status_code == OK
    
    user_list = response.json()
    assert user_list["users"][0]['u_id'] == user['auth_user_id']
    assert user_list["users"][0]['email'] == "11037.666@gmail.com"
    assert user_list["users"][0]['name_first'] == "Hopeful"
    assert user_list["users"][0]['name_last'] == "Boyyy"
    assert user_list["users"][0]['handle_str'] == "hopefulboyyy"
    
    
def test_multiple_users():
    '''
    Checking output with multiple users
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    user_1_json = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_1_json).json()


    user_2_json = {
        "email": "bob123@gmail.com",
        "password": "qwerty",
        "name_first": "Bob",
        "name_last": "Marley"
    }
<<<<<<< HEAD:tests/users_all_v1_http_test.py
    user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()
=======
    requests.post(f"{BASE_URL}/auth/register/v2", json = user_2_json).json()
>>>>>>> master:tests/http_tests/user/users_all_v1_http_test.py
    
    token_params = {
        'token': user_1['token']
    }
    
    response = requests.get(f"{BASE_URL}/users/all/v1", params = token_params)
    
    assert response.status_code == OK
    
    user_list = response.json()

    assert user_list["users"][0]['u_id'] == user_1['auth_user_id']
    assert user_list["users"][0]['email'] == "11037.666@gmail.com"
    assert user_list["users"][0]['name_first'] == "Hopeful"
    assert user_list["users"][0]['name_last'] == "Boyyy"
    assert user_list["users"][0]['handle_str'] == "hopefulboyyy"

    assert user_list["users"][1]['u_id'] == user_2['auth_user_id']
    assert user_list["users"][1]['email'] == "bob123@gmail.com"
    assert user_list["users"][1]['name_first'] == "Bob"
    assert user_list["users"][1]['name_last'] == "Marley"
    assert user_list["users"][1]['handle_str'] == "bobmarley"