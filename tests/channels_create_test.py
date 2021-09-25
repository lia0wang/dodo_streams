import pytest
from src.other import clear_v1
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.error import InputError

def test_invalid_length_short():
    clear_v1()
    user = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    # Raise an InputError when the channel's name
    # is less than 1 char
    with pytest.raises(InputError):
        channels_create_v1(user, "", True)
    with pytest.raises(InputError):
        channels_create_v1(user, "", False)

def test_invalid_length_long():
    # Raise an InputError when the channel's name
    # is more than 20 char
    clear_v1()
    user = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    with pytest.raises(InputError):
        channels_create_v1(user, "aaaabbbbccccddddeeee1", True)
    with pytest.raises(InputError):
        channels_create_v1(user, "1234567890??????????????", False)
