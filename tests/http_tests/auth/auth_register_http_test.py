import pytest
import requests
import pytest
from src.other import clear_v1

from src import config

BASE_URL = config.url

def test_http_register_basic():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    register_param = {
        "email": "11037@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    get_response =  requests.post(f"{BASE_URL}/auth/register/v2", json = register_param)
    assert get_response.status_code == 200
    

def test_http_register_basic2():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    register_param = {
        "email": "11037@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    get_response =  requests.post(f"{BASE_URL}/auth/register/v2", json = register_param)
    assert get_response.status_code == 200

def test_http_invalid_email():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})

    register_param = {
        "email": "11037.666@gmail&.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    get_response = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param)
    assert get_response.status_code == 400
    register_param['email'] = "@xample.com"
    get_response = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param)
    assert get_response.status_code == 400

def test_http_duplicate_email():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    register_param = {
        "email": "11037@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    get_response1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param)
    assert get_response1.status_code == 200
    get_response = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param)    
    assert get_response.status_code == 400
    


def test_http_password_short():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    register_param = {
        "email": "11037@gmail.com",
        "password": "12345",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    get_response = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param)
    assert get_response.status_code == 400

def test_http_name_first_long():

    requests.delete(f"{BASE_URL}/clear/v1", json = {})

    register_param = {
        "email": "11037@gmail.com",
        "password": "Hope11037",
        "name_first": "MynameisYoshikageKiraIm33yearsoldMyhouseisinthenort",
        "name_last": "Boyyy"
    }
    get_response = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param)
    assert get_response.status_code == 400

def test_http_name_last_long():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})

    register_param = {
        "email": "11037@gmail.com",
        "password": "Hope11037",
        "name_first": "Mynameis",
        "name_last": "MynameisYoshikageKiraIm33yearsoldMyhouseisinthenort"
    }
    get_response = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param)
    assert get_response.status_code == 400

def test_http_name_first_short():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})

    register_param = {
        "email": "11037@gmail.com",
        "password": "Hope11037",
        "name_first": "",
        "name_last": "Boyyy"
    }
    get_response = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param)
    assert get_response.status_code == 400

def test_http_name_last_short():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})

    register_param = {
        "email": "11037@gmail.com",
        "password": "Hope11037",
        "name_first": "Mynameis",
        "name_last": ""
    }
    get_response = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param)
    assert get_response.status_code == 400

def test_handle_length_greater_than_20():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    register_param = {
        "email": "11037@gmail.com",
        "password": "Hope11037",
        "name_first": "abcdefghijklmnop",
        "name_last": "qrstu"
    }
    get_response = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()
    register_param = {
        "email": "1103@gmail.com",
        "password": "Hope11037",
        "name_first": "abcdefghijklmnop",
        "name_last": "qrstu"
    }
    get_response1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()
    profile_param1 = {
        "u_id": get_response["auth_user_id"],
        "token": get_response["token"]
    }
    profile_param2 = {
        "u_id": get_response1["auth_user_id"],
        "token": get_response1["token"]
    }
    profile_return1 = requests.get(f"{BASE_URL}/user/profile/v1", params = profile_param1).json()
    profile_return2 = requests.get(f"{BASE_URL}/user/profile/v1", params = profile_param2).json()

    assert profile_return1["user"]['handle_str'] == "abcdefghijklmnopqrst"
    assert profile_return2["user"]['handle_str'] == "abcdefghijklmnopqrst0"