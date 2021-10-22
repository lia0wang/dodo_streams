import requests
import pytest
from src import config

BASE_URL = config.url

def test_invalid_token():
    '''
    Checking if the function can identify an invalid token
    '''
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param_1 = {
        "email": "shifanchen@gmail.com",
        "password": "djkadldjsa21",
        "name_first": "shifan",
        "name_last": "chen"
    }
    user_0 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    register_param_2 = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()
    
    delete_info = {
        'token': user_1['token'] + '1', # Invalid token
        'u_id': user_0['auth_user_id']
    }
    
    response = requests.delete(f"{BASE_URL}/admin/user/remove/v1", json = delete_info)
    
    assert response.status_code != 200
    
def test_invalid_uid():
    '''
    Checking if the function identifies invalid u_ids
    '''
    
def test_last_global():
    '''
    Checking if the function identifies if the u_id is the only global owner
    '''
    
def test_token_not_global():
    '''
    Checking if the function identifies if the token's u_id is not global
    '''
    
def test_basic():
    '''
    Checking if the function works normally
    '''