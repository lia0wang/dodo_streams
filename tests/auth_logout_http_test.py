import pytest
import requests
import pytest
from src.other import clear_v1

BASE_URL = 'http://localhost:8080'

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
    login = requests.post(f"{BASE_URL}/auth/login/v2", json = login_data)
    assert login.status_code == 200
    
    token = {
        'token': reg['token']
    }

    logout = requests.post(f"{BASE_URL}/auth/logout/v1", json = token)
    assert logout.status_code == 200
    

def test_register_logout():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    register_param = {
        "email": "JoJo@gmail.com", 
        "password": "HermitPurple",
        "name_first": "Joseph", 
        "name_last": "Joestar"
    }
    reg = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param)
    assert reg.status_code == 200   
  
    token = {
        'token': reg['token']
    }
    
    logout = requests.post(f"{BASE_URL}/auth/logout/v1", json = token)
    assert logout.status_code == 200
