import pytest
import requests
import pytest
from src.other import clear_v1

from src import config

BASE_URL = config.url

@pytest.fixture
def user_json():
    return {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }

def test_http_register_basic(user_json):
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    get_response =  requests.post(f"{BASE_URL}/auth/register/v2", json = user_json)
    assert get_response.status_code == 200
    

def test_http_invalid_email(user_json):
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    user_json['email'] = "11037.666@gmail&.com"
    get_response = requests.post(f"{BASE_URL}/auth/register/v2", json = user_json)
    assert get_response.status_code == 400
    user_json['email'] = "@xample.com"
    get_response = requests.post(f"{BASE_URL}/auth/register/v2", json = user_json)
    assert get_response.status_code == 400

def test_http_duplicate_email(user_json):
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    get_response1 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_json)
    assert get_response1.status_code == 200
    get_response = requests.post(f"{BASE_URL}/auth/register/v2", json = user_json)    
    assert get_response.status_code == 400
    
def test_http_password_short(user_json):
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    user_json["password"] = "12345" 
    get_response = requests.post(f"{BASE_URL}/auth/register/v2", json = user_json)
    assert get_response.status_code == 400

def test_http_name_first_long(user_json):
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    user_json["name_first"] = "MynameisYoshikageKiraIm33yearsoldMyhouseisinthenort"
    get_response = requests.post(f"{BASE_URL}/auth/register/v2", json = user_json)
    assert get_response.status_code == 400

def test_http_name_last_long(user_json):
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    user_json["name_last"] = "MynameisYoshikageKiraIm33yearsoldMyhouseisinthenort"
    get_response = requests.post(f"{BASE_URL}/auth/register/v2", json = user_json)
    assert get_response.status_code == 400

def test_http_name_first_short(user_json):
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    user_json["name_first"] = ""
    get_response = requests.post(f"{BASE_URL}/auth/register/v2", json = user_json)
    assert get_response.status_code == 400

def test_http_name_last_short(user_json):
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    user_json["name_last"] = ""
    get_response = requests.post(f"{BASE_URL}/auth/register/v2", json = user_json)
    assert get_response.status_code == 400

def test_handle_length_greater_than_20(user_json):
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    user_json["name_first"] = "abcdefghijklmnop"
    user_json["name_last"] = "qrstu"
    get_response = requests.post(f"{BASE_URL}/auth/register/v2", json = user_json).json()
    user_json["email"] = "1103@gmail.com"
    get_response1 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_json).json()
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