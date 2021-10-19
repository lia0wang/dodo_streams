import pytest
import requests
import pytest
from src.other import clear_v1

BASE_URL = 'http://localhost:8080'

def register_login_logout_test():
    clear_v1()
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


    

def register_logout_test():
    clear_v1()
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
