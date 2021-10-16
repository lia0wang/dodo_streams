import pytest
import requests
import pytest
from src.error import AccessError, InputError

BASE_URL = 'http://localhost:8080'


def test_http_invalid_email():
    register_param = {
        "email": "11037.666@gmail&.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    with pytest.raises(InputError):
         requests.post(f"{BASE_URL}/auth/register/v2", json = register_param)
    register_param['email'] = "@xample.com"
    with pytest.raises(InputError):
         requests.post(f"{BASE_URL}/auth/register/v2", json = register_param)

def test_http_duplicate_email():
    register_param = {
        "email": "11037@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    requests.post(f"{BASE_URL}/auth/register/v2", json = register_param)
    with pytest.raises(InputError):
        requests.post(f"{BASE_URL}/auth/register/v2", json = register_param)


def test_http_password_short():
    register_param = {
        "email": "11037@gmail.com",
        "password": "12345",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    with pytest.raises(InputError):
        requests.post(f"{BASE_URL}/auth/register/v2", json = register_param)

def test_http_name_first_long():
    register_param = {
        "email": "11037@gmail.com",
        "password": "Hope11037",
        "name_first": "MynameisYoshikageKiraIm33yearsoldMyhouseisinthenort",
        "name_last": "Boyyy"
    }
    with pytest.raises(InputError):
        requests.post(f"{BASE_URL}/auth/register/v2", json = register_param)

def test_http_name_last_long():
    register_param = {
        "email": "11037@gmail.com",
        "password": "Hope11037",
        "name_first": "Mynameis",
        "name_last": "MynameisYoshikageKiraIm33yearsoldMyhouseisinthenort"
    }
    with pytest.raises(InputError):
        requests.post(f"{BASE_URL}/auth/register/v2", json = register_param)


def test_http_name_first_short():
    register_param = {
        "email": "11037@gmail.com",
        "password": "Hope11037",
        "name_first": "",
        "name_last": "Boyyy"
    }
    with pytest.raises(InputError):
        requests.post(f"{BASE_URL}/auth/register/v2", json = register_param)

def test_http_name_last_short():
    register_param = {
        "email": "11037@gmail.com",
        "password": "Hope11037",
        "name_first": "Mynameis",
        "name_last": ""
    }
    with pytest.raises(InputError):
        requests.post(f"{BASE_URL}/auth/register/v2", json = register_param)



