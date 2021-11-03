import requests
from src import config

BASE_URL = config.url

def test_reset_error():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    register_param = {
        "email": "dumbymail11037@gmail.com",
        "password": "Hope11037",
        "name_first": "abcdefghijklmnop",
        "name_last": "qrstu"
    }
    requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()
    get_response = requests.post(f"{BASE_URL}/auth/passwordreset/request/v1", json = {register_param['email']})
    assert get_response.status_code == 200
    reset_body = {
        "reset_code": "??????",
        "new_password": "new_password"
    }
    get_response = requests.post(f"{BASE_URL}/auth/passwordreset/request/v1", json = reset_body)
    assert get_response.status_code == 400

def test_reset_short_password():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    register_param = {
        "email": "dumbymail11037@gmail.com",
        "password": "Hope11037",
        "name_first": "abcdefghijklmnop",
        "name_last": "qrstu"
    }
    requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()
    get_response = requests.post(f"{BASE_URL}/auth/passwordreset/request/v1", json = {register_param['email']})
    assert get_response.status_code == 200
    reset_body = {
        "reset_code": "ABCDE1",
        "new_password": "new"
    }
    get_response = requests.post(f"{BASE_URL}/auth/passwordreset/request/v1", json = reset_body)
    assert get_response.status_code == 400