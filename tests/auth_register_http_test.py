import pytest
import requests

BASE_URL = 'http://127.0.0.1:5000'


def test_http_register():
    register_param_1 = {
        'email': '11037@gmail.com',
        'password': 'Hope11037',
        'name_first': 'Hopeful',
        'name_last': 'Boy'
    }
    get_response = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1)
    response_data = get_response.json()
    assert "auth_user_id" in response_data
    assert "token" in response_data
