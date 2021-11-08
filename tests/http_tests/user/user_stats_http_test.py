import requests
import pytest
from src import config
BASE_URL = config.url

def test_zero_activities():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    user_param_1 = {
        "email": "test1@gmail.com",
        "password": "abcd1234",
        "name_first": "John",
        "name_last": "Smith"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = user_param_1).json()

    user_stats_request = {
        'token': user_1['token']
        }
    user_1_stats = requests.get(f"{BASE_URL}/user/stats/v1", json = user_stats_request)
    assert user_1_stats.status_code == 200
    user_1_stats = user_1_stats.json()
    print(user_1_stats)
    assert user_1_stats['involvement_rate'] == 0
