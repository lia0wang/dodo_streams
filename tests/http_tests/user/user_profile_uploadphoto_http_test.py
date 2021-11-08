import requests
import pytest
from src import config

BASE_URL = config.url

imgurl_jpg_3958x3030 = "http://cgi.cse.unsw.edu.au/~morri/morriphoto.jpg"
imgurl_png_159x200 = "http://www.cse.unsw.edu.au/~richardb/index_files/RichardBuckland-200.png"
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
        "img_url": imgurl_jpg_3958x3030,
        "x_start": 0,
        "y_start": 0,
        "x_end": 1000,
        "y_end": 1000
    }

def test_valid_photo_and_dimensions(user_json, uploadphoto_json):
    requests.delete(f"{BASE_URL}/clear/v1", json = {})

    user = requests.post(f"{BASE_URL}/auth/register/v2", json = user_json).json()

    uploadphoto_json["token"] = user["token"]
    uploadphoto_response = requests.post(f"{BASE_URL}user/profile/uploadphoto/v1", json = uploadphoto_json)
    assert uploadphoto_response.status_code == 200
    uploadphoto_json['x_end'] = 1
    uploadphoto_json['y_end'] = 1
    uploadphoto_response = requests.post(f"{BASE_URL}user/profile/uploadphoto/v1", json = uploadphoto_json)
    assert uploadphoto_response.status_code == 200
    uploadphoto_json['x_end'] = 3858
    uploadphoto_json['y_end'] = 3030
    uploadphoto_response = requests.post(f"{BASE_URL}user/profile/uploadphoto/v1", json = uploadphoto_json)
    assert uploadphoto_response.status_code == 200
    uploadphoto_json['x_start'] = 200
    uploadphoto_json['y_start'] = 200
    uploadphoto_response = requests.post(f"{BASE_URL}user/profile/uploadphoto/v1", json = uploadphoto_json)
    assert uploadphoto_response.status_code == 200


def test_invalid_imgurl(user_json, uploadphoto_json):
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = user_json).json()
    uploadphoto_json["token"] = user["token"]
    uploadphoto_json['img_url'] += "1"
    uploadphoto_response = requests.post(f"{BASE_URL}user/profile/uploadphoto/v1", json = uploadphoto_json)
    assert uploadphoto_response.status_code == 400
    uploadphoto_json['x_end'] = 100
    uploadphoto_json['y_end'] = 100
    uploadphoto_json['img_url'] = imgurl_png_159x200
    uploadphoto_response = requests.post(f"{BASE_URL}user/profile/uploadphoto/v1", json = uploadphoto_json)
    assert uploadphoto_response.status_code == 400



def test_invalid_img_dim_outside(user_json, uploadphoto_json):
    requests.delete(f"{BASE_URL}/clear/v1", json = {})

    user = requests.post(f"{BASE_URL}/auth/register/v2", json = user_json).json()

    uploadphoto_json["token"] = user["token"]
    uploadphoto_json['x_start'] = -1
    uploadphoto_response = requests.post(f"{BASE_URL}user/profile/uploadphoto/v1", json = uploadphoto_json)
    assert uploadphoto_response.status_code == 400  
    uploadphoto_json['x_start'] = 1
    uploadphoto_json['x_end'] = 3859
    uploadphoto_json['y_end'] = 3031
    uploadphoto_response = requests.post(f"{BASE_URL}user/profile/uploadphoto/v1", json = uploadphoto_json)
    assert uploadphoto_response.status_code == 400
    uploadphoto_json['x_end'] = 3858
    uploadphoto_json['y_end'] = 3030
    uploadphoto_json['y_start'] = -1
    uploadphoto_response = requests.post(f"{BASE_URL}user/profile/uploadphoto/v1", json = uploadphoto_json)
    assert uploadphoto_response.status_code == 400


def test_invalid_img_end_lessthan_last(user_json, uploadphoto_json):
    requests.delete(f"{BASE_URL}/clear/v1", json = {})

    user = requests.post(f"{BASE_URL}/auth/register/v2", json = user_json).json()

    uploadphoto_json["token"] = user["token"]
    uploadphoto_json['x_start'] = 1001
    uploadphoto_response = requests.post(f"{BASE_URL}user/profile/uploadphoto/v1", json = uploadphoto_json)
    assert uploadphoto_response.status_code == 400
    uploadphoto_json['x_start'] = 1000
    uploadphoto_json['y_start'] = 1001  
    uploadphoto_response = requests.post(f"{BASE_URL}user/profile/uploadphoto/v1", json = uploadphoto_json)
    assert uploadphoto_response.status_code == 400