import requests
from src import config

BASE_URL = config.url

def test_one_reset_request():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    register_param = {
        "email": "dumbymail11037@gmail.com",
        "password": "Hope11037",
        "name_first": "abcdefghijklmnop",
        "name_last": "qrstu"
    }
    resetrequest_body = {
        "email": "dumbymail11037@gmail.com"
    }
    requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()
    get_response = requests.post(f"{BASE_URL}/auth/passwordreset/request/v1", json = resetrequest_body)
    assert get_response.status_code == 200
'''
def test_multiple_reset_request():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    register_param = {
        "email": "dumbymail11037@gmail.com",
        "password": "Hope11037",
        "name_first": "abcdefghijklmnop",
        "name_last": "qrstu"
    }
    resetrequest_body = {
        "email": "dumbymail11037@gmail.com"
    }
    requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()
    get_response = requests.post(f"{BASE_URL}/auth/passwordreset/request/v1", json = resetrequest_body)
    assert get_response.status_code == 200
    get_response = requests.post(f"{BASE_URL}/auth/passwordreset/request/v1", json = resetrequest_body)
    assert get_response.status_code == 200
'''
def test_reset_request_logged_out():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    register_param = {
        "email": "dumbymail11037@gmail.com",
        "password": "Hope11037",
        "name_first": "abcdefghijklmnop",
        "name_last": "qrstu"
    }
    resetrequest_body = {
        "email": "dumbymail11037@gmail.com"
    }
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()
    get_response = requests.post(f"{BASE_URL}/auth/passwordreset/request/v1", json = resetrequest_body)
    assert get_response.status_code == 200

    channel_param = {
        'token': user['token'],
        'name': 'league',
        'is_public': True
    }
    create = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param)
    assert create.status_code == 403

def test_no_error_when_invalid_email():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    register_param = {
        "email": "dumbymail11037@gmail.com",
        "password": "Hope11037",
        "name_first": "abcdefghijklmnop",
        "name_last": "qrstu"
    }
    resetrequest_body = {
        "email": "dumbymail@gmail.com"
    }
    requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()
    get_response = requests.post(f"{BASE_URL}/auth/passwordreset/request/v1", json = resetrequest_body)
    assert get_response.status_code == 200