import requests
import pytest
from src import config

BASE_URL = config.url

imgurl_3958x3030 = "http://cgi.cse.unsw.edu.au/~morri/morriphoto.jpg"

@pytest.fixture
def user_json():
    return {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }

@pytest.fixture
def uploadphoto_json():
    return {
        "token": "",
        "img_url": imgurl_3958x3030,
        "x_start": 0,
        "y_start": 0,
        "x_end": 1000,
        "y_end": 1000
    }

@pytest.fixture
def uploadphoto_json_dim_max(upload_photo_json):
    upload_photo_json['x_end'] = 3858
    upload_photo_json['y_end'] = 3030
    return upload_photo_json

@pytest.fixture
def uploadphoto_json_dim_min(upload_photo_json):
    upload_photo_json['x_end'] = 1
    upload_photo_json['y_end'] = 1
    return upload_photo_json

@pytest.fixture
def uploadphoto_json_invalid_url(upload_photo_json):
    upload_photo_json['img_url'] += "1"
    return upload_photo_json

@pytest.fixture
def uploadphoto_json_dim_outside_01(upload_photo_json):
    upload_photo_json['x_end'] = 3859
    upload_photo_json['y_end'] = 3031
    return upload_photo_json

@pytest.fixture
def uploadphoto_json_dim_outside_02(upload_photo_json):
    upload_photo_json['x_start'] = 3859
    upload_photo_json['y_start'] = 3031
    return upload_photo_json

@pytest.fixture
def uploadphoto_json_end_less_start_01(upload_photo_json):
    upload_photo_json['x_end'] = 999
    upload_photo_json['x_start'] = 1000
    return upload_photo_json

@pytest.fixture
def uploadphoto_json_end_less_start_02(upload_photo_json):
    upload_photo_json['y_end'] = 999
    upload_photo_json['y_start'] = 1000
    return upload_photo_json

def test_valid_photo_and_dimensions(uploadphoto_json, uploadphoto_json_dim_min, uploadphoto_json_dim_max):
    requests.delete(f"{BASE_URL}/clear/v1", json = {})

    user = requests.post(f"{BASE_URL}/auth/register/v2", json = user_json).json()

    uploadphoto_json["token"] = user["token"]
    uploadphoto_json_dim_min["token"] = user["token"]
    uploadphoto_json_dim_max["token"] = user["token"]

    uploadphoto_response = requests.post(f"{BASE_URL}user/profile/uploadphoto/v1", json = uploadphoto_json)
    uploadphoto_response.status_code == 200
    uploadphoto_response = requests.post(f"{BASE_URL}user/profile/uploadphoto/v1", json = uploadphoto_json_dim_min)
    uploadphoto_response.status_code == 200
    uploadphoto_response = requests.post(f"{BASE_URL}user/profile/uploadphoto/v1", json = uploadphoto_json_dim_max)
    uploadphoto_response.status_code == 200

def test_invalid_imgurl(uploadphoto_json_invalid_url):
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
   
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = user_json).json()
    uploadphoto_json_invalid_url["token"] = user["token"]
    uploadphoto_response = requests.post(f"{BASE_URL}user/profile/uploadphoto/v1", json = uploadphoto_json_invalid_url)
    uploadphoto_response.status_code == 400

def test_invalid_img_dim_outside(uploadphoto_json_dim_outside_01, uploadphoto_json_dim_outside_02):
    requests.delete(f"{BASE_URL}/clear/v1", json = {})

    user = requests.post(f"{BASE_URL}/auth/register/v2", json = user_json).json()

    uploadphoto_json_dim_outside_01["token"] = user["token"]
    uploadphoto_json_dim_outside_02["token"] = user["token"]

    uploadphoto_response = requests.post(f"{BASE_URL}user/profile/uploadphoto/v1", json = uploadphoto_json_dim_outside_01)
    uploadphoto_response.status_code == 400
    uploadphoto_response = requests.post(f"{BASE_URL}user/profile/uploadphoto/v1", json = uploadphoto_json_dim_outside_02)
    uploadphoto_response.status_code == 400


def test_invalid_img_end_lessthan_last(uploadphoto_json_end_less_start_01, uploadphoto_json_end_less_start_02 ):
    requests.delete(f"{BASE_URL}/clear/v1", json = {})

    user = requests.post(f"{BASE_URL}/auth/register/v2", json = user_json).json()

    uploadphoto_json_end_less_start_01["token"] = user["token"]
    uploadphoto_json_end_less_start_02["token"] = user["token"]

    uploadphoto_response = requests.post(f"{BASE_URL}user/profile/uploadphoto/v1", json = uploadphoto_json_end_less_start_01)
    uploadphoto_response.status_code == 400
    uploadphoto_response = requests.post(f"{BASE_URL}user/profile/uploadphoto/v1", json = uploadphoto_json_end_less_start_02)
    uploadphoto_response.status_code == 400