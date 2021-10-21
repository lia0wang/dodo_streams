import requests
import pytest
from src import config

BASE_URL = config.url
    
    
def test_invalid_token():
    '''
    Checking output when the token is incorrect
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()
    
    token = {
        'token': user['token'] + '1' # Incorrect token
    }
    
    response = requests.get(f"{BASE_URL}/users/all/v1", json = token)
    
    assert response.status_code != 200
    
def test_single_user():
    '''
    Checking output with only one user
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()
    
    token = {
        'token': user['token']
    }
    
    response = requests.get(f"{BASE_URL}/users/all/v1", json = token)
    
    assert response.status_code == 200
    
    user_list = response.json()
    assert user_list == [{"u_id": 1,"email": "11037.666@gmail.com", "name_first": "Hopeful", 
                          "name_last": "Boyyy", "handle_str": "hopefulboyyy", "permission_id": 1}]
    
    
def test_multiple_users():
    '''
    Checking output with multiple users
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param_1 = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()


    register_param_2 = {
        "email": "bob123@gmail.com",
        "password": "qwerty",
        "name_first": "Bob",
        "name_last": "Marley"
    }
    requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()
    
    token = {
        'token': user_1['token']
    }
    
    response = requests.get(f"{BASE_URL}/users/all/v1", json = token)
    
    assert response.status_code == 200
    
    user_list = response.json()
    assert user_list == [{"u_id": 1,"email": "11037.666@gmail.com", "name_first": "Hopeful", 
                          "name_last": "Boyyy", "handle_str": "hopefulboyyy", "permission_id": 1},
                         {"u_id": 2,"email": "bob123@gmail.com", "name_first": "Bob", 
                          "name_last": "Marley", "handle_str": "bobmarley", "permission_id": 2}]