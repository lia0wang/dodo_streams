import pytest
import requests
import pytest
from src.other import clear_v1

BASE_URL = 'http://localhost:8080'

def test_http_valid_login1():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    register_param1 = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    reg1 =  requests.post(f"{BASE_URL}/auth/register/v2", json = register_param1)
    assert reg1.status_code == 200

    #login 
    login_data1 = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037"        
    }
    login_1 =  requests.post(f"{BASE_URL}/auth/login/v2", json = login_data1)
    assert login_1.status_code == 200


def test_http_valid_login2():
    register_param2 = {
        "email": "JoJo@gmail.com", 
        "password": "HermitPurple",
        "name_first": "Joseph", 
        "name_last": "Joestar"
    }
    reg2 =  requests.post(f"{BASE_URL}/auth/register/v2", json = register_param2)
    assert reg2.status_code == 200

    login_data2 = {
        "email": "JoJo@gmail.com", 
        "password": "HermitPurple"
    }
    login_2 =  requests.post(f"{BASE_URL}/auth/login/v2", json = login_data2)
    assert login_2.status_code == 200
    

def test_invalid_email1():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    register_param1 = {
        "email": "JoJo@gmail.com",
        "password": "HermitPurple",
        "name_first": "Joseph",
        "name_last": "Joestar"
    }
    reg1 =  requests.post(f"{BASE_URL}/auth/register/v2", json = register_param1)
    assert reg1.status_code == 200

    login_data1 = {
        "email": "jojo@gmail.com",
        "password": "HermitPurple"        
    }
    login_1 =  requests.post(f"{BASE_URL}/auth/login/v2", json = login_data1)
    assert login_1.status_code == 400

def test_invalid_email2():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    register_param1 = {
        "email": "JoJo@gmail.com",
        "password": "HermitPurple",
        "name_first": "Joseph",
        "name_last": "Joestar"
    }
    reg1 =  requests.post(f"{BASE_URL}/auth/register/v2", json = register_param1)
    assert reg1.status_code == 200

    login_data1 = {
        "email": "jojossds@gmail.com",
        "password": "HermitPurple"        
    }
    login_1 =  requests.post(f"{BASE_URL}/auth/login/v2", json = login_data1)
    assert login_1.status_code == 400

def test_invalid_password():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    register_param1 = {
        "email": "JoJo@gmail.com",
        "password": "HermitPurple",
        "name_first": "Joseph",
        "name_last": "Joestar"
    }
    reg1 =  requests.post(f"{BASE_URL}/auth/register/v2", json = register_param1)
    assert reg1.status_code == 200

    login_data1 = {
        "email": "JoJo@gmail.com",
        "password": "WrongPassword"        
    }
    login_1 =  requests.post(f"{BASE_URL}/auth/login/v2", json = login_data1)
    assert login_1.status_code == 400    
