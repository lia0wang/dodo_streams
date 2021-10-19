import pytest
import requests
import pytest
from src.other import clear_v1

BASE_URL = 'http://localhost:8080'

def test_http_register_basic():
    clear_v1()
    register_param = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    get_response =  requests.post(f"{BASE_URL}/auth/register/v2", json = register_param)
    assert get_response.status_code == 200


def test_http_invalid_email():
    clear_v1()
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
    clear_v1()
    register_param = {
        "email": "11037@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    requests.post(f"{BASE_URL}/auth/register/v2", json = register_param)
    get_response = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param)
    assert get_response.status_code == 400


def test_http_password_short():
    clear_v1()
    register_param = {
        "email": "11037@gmail.com",
        "password": "12345",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    get_response = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param)
    assert get_response.status_code == 400

def test_http_name_first_long():
    clear_v1()
    register_param = {
        "email": "11037@gmail.com",
        "password": "Hope11037",
        "name_first": "MynameisYoshikageKiraIm33yearsoldMyhouseisinthenort",
        "name_last": "Boyyy"
    }
    get_response = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param)
    assert get_response.status_code == 400

def test_http_name_last_long():
    clear_v1()
    register_param = {
        "email": "11037@gmail.com",
        "password": "Hope11037",
        "name_first": "Mynameis",
        "name_last": "MynameisYoshikageKiraIm33yearsoldMyhouseisinthenort"
    }
    get_response = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param)
    assert get_response.status_code == 400

def test_http_name_first_short():
    clear_v1()
    register_param = {
        "email": "11037@gmail.com",
        "password": "Hope11037",
        "name_first": "",
        "name_last": "Boyyy"
    }
    get_response = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param)
    assert get_response.status_code == 400

def test_http_name_last_short():
    clear_v1()
    register_param = {
        "email": "11037@gmail.com",
        "password": "Hope11037",
        "name_first": "Mynameis",
        "name_last": ""
    }
    get_response = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param)
    assert get_response.status_code == 400
