import requests

from src import config

BASE_URL = config.url

def test_dm_owner_leave():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param = {
        "email": "standuser@gmail.com",
        "password": "djkadldjsa21",
        "name_first": "Jotoro",
        "name_last": "Josuke"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    register_param_1 = {
        "email": "avatar@gmail.com",
        "password": "Hope11037",
        "name_first": "ang",
        "name_last": "airbender"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    register_param_2 = {
        "email": "z5361945@gmail.com",
        "password": "DarrenH123",
        "name_first": "Darren",
        "name_last": "Huo"
    }
    user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()

    dm_create_param = {
        "token": auth_user["token"],
        "u_ids": [user_1["auth_user_id"], user_2["auth_user_id"]]
    }

    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_create_param).json()

    dm_leave_param = {
        "token": auth_user["token"], 
        "dm_id": dm["dm_id"]
    }
    dm_leave = requests.post(f"{BASE_URL}/dm/leave/v1", json = dm_leave_param)
    assert dm_leave.status_code == 200

def test_dm_not_owner_leave():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param = {
        "email": "standuser@gmail.com",
        "password": "djkadldjsa21",
        "name_first": "Jotoro",
        "name_last": "Josuke"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    register_param_1 = {
        "email": "avatar@gmail.com",
        "password": "Hope11037",
        "name_first": "ang",
        "name_last": "airbender"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    register_param_2 = {
        "email": "z5361945@gmail.com",
        "password": "DarrenH123",
        "name_first": "Darren",
        "name_last": "Huo"
    }
    user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()

    dm_create_param = {
        "token": auth_user["token"],
        "u_ids": [user_1["auth_user_id"], user_2["auth_user_id"]]
    }

    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_create_param).json()

    dm_leave_param = {
        "token": user_1["token"], 
        "dm_id": dm["dm_id"]
    }
    dm_leave = requests.post(f"{BASE_URL}/dm/leave/v1", json = dm_leave_param)
    assert dm_leave.status_code == 200    

    dm_leave_param1 = {
        "token": user_2["token"], 
        "dm_id": dm["dm_id"]
    }
    dm_leave1 = requests.post(f"{BASE_URL}/dm/leave/v1", json = dm_leave_param1)
    assert dm_leave1.status_code == 200    

def test_dm_everyone_leave():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param = {
        "email": "standuser@gmail.com",
        "password": "djkadldjsa21",
        "name_first": "Jotoro",
        "name_last": "Josuke"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    register_param_1 = {
        "email": "avatar@gmail.com",
        "password": "Hope11037",
        "name_first": "ang",
        "name_last": "airbender"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    register_param_2 = {
        "email": "z5361945@gmail.com",
        "password": "DarrenH123",
        "name_first": "Darren",
        "name_last": "Huo"
    }
    user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()

    dm_create_param = {
        "token": auth_user["token"],
        "u_ids": [user_1["auth_user_id"], user_2["auth_user_id"]]
    }

    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_create_param).json()

    dm_leave_param = {
        "token": auth_user["token"], 
        "dm_id": dm["dm_id"]
    }
    dm_leave_param1 = {
        "token": user_1["token"], 
        "dm_id": dm["dm_id"]
    }
    dm_leave_param2 = {
        "token": user_2["token"], 
        "dm_id": dm["dm_id"]
    }
    dm_leave = requests.post(f"{BASE_URL}/dm/leave/v1", json = dm_leave_param)
    assert dm_leave.status_code == 200    

    dm_leave1 = requests.post(f"{BASE_URL}/dm/leave/v1", json = dm_leave_param1)
    assert dm_leave1.status_code == 200    

    dm_leave2 = requests.post(f"{BASE_URL}/dm/leave/v1", json = dm_leave_param2)
    assert dm_leave2.status_code == 200    

def test_dm_leave_invalid_user():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param = {
        "email": "standuser@gmail.com",
        "password": "djkadldjsa21",
        "name_first": "Jotoro",
        "name_last": "Josuke"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    register_param_1 = {
        "email": "avatar@gmail.com",
        "password": "Hope11037",
        "name_first": "ang",
        "name_last": "airbender"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    register_param_2 = {
        "email": "z5361945@gmail.com",
        "password": "DarrenH123",
        "name_first": "Darren",
        "name_last": "Huo"
    }
    user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()

    dm_create_param = {
        "token": auth_user["token"],
        "u_ids": [user_1["auth_user_id"]]
    }

    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_create_param).json()

    dm_leave_param = {
        "token": auth_user["token"], 
        "dm_id": dm["dm_id"]
    }
    dm_leave_param2 = {
        "token": user_2["token"], 
        "dm_id": dm["dm_id"]
    }
    dm_leave = requests.post(f"{BASE_URL}/dm/leave/v1", json = dm_leave_param)
    assert dm_leave.status_code == 200    

    dm_leave2 = requests.post(f"{BASE_URL}/dm/leave/v1", json = dm_leave_param2)
    assert dm_leave2.status_code == 403    

def test_dm_leave_invalid_dm_id():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param = {
        "email": "standuser@gmail.com",
        "password": "djkadldjsa21",
        "name_first": "Jotoro",
        "name_last": "Josuke"
    }
    auth_user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    register_param_1 = {
        "email": "avatar@gmail.com",
        "password": "Hope11037",
        "name_first": "ang",
        "name_last": "airbender"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    register_param_2 = {
        "email": "z5361945@gmail.com",
        "password": "DarrenH123",
        "name_first": "Darren",
        "name_last": "Huo"
    }
    user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()

    dm_create_param = {
        "token": auth_user["token"],
        "u_ids": [user_1["auth_user_id"], user_2["auth_user_id"]]
    }

    dm = requests.post(f"{BASE_URL}/dm/create/v1", json = dm_create_param).json()

    dm_leave_param = {
        "token": auth_user["token"], 
        "dm_id": dm["dm_id"] + 1
    }
    dm_leave_param1 = {
        "token": user_1["token"], 
        "dm_id": dm["dm_id"]
    }
    dm_leave_param2 = {
        "token": user_2["token"], 
        "dm_id": dm["dm_id"]
    }
    dm_leave = requests.post(f"{BASE_URL}/dm/leave/v1", json = dm_leave_param)
    assert dm_leave.status_code == 400    

    dm_leave1 = requests.post(f"{BASE_URL}/dm/leave/v1", json = dm_leave_param1)
    assert dm_leave1.status_code == 200    

    dm_leave2 = requests.post(f"{BASE_URL}/dm/leave/v1", json = dm_leave_param2)
    assert dm_leave2.status_code == 200    