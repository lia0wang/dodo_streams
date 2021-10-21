import pytest
import requests
import pytest
import json
from src.other import clear_v1
from src import config

BASE_URL = config.url


def test_register_logout():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    register_param = {
        "email": "JoJo@gmail.com", 
        "password": "HermitPurple",
        "name_first": "Joseph", 
        "name_last": "Joestar"
    }
    reg = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()
    
    register_param = {
        "token": reg['token']
    }
    
    logout = requests.post(f"{BASE_URL}/auth/logout/v1", json = register_param)
    assert logout.status_code == 200

def test_register_login_logout():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    register_param = {
        "email": "JoJo@gmail.com", 
        "password": "HermitPurple",
        "name_first": "Joseph", 
        "name_last": "Joestar"
    }
    reg = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param)
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

'''
def test_invalid_token_logout():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    register_param = {
        "email": "JoJo@gmail.com", 
        "password": "HermitPurple",
        "name_first": "Joseph", 
        "name_last": "Joestar"
    }
    reg = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()
    
    register_param = {
        "token": reg['token'] + 1
    }
    
    logout = requests.post(f"{BASE_URL}/auth/logout/v1", json = register_param)
    assert logout.status_code == 403

'''