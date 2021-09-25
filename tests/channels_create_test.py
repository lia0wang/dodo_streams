import pytest
from src.other import clear_v1
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.error import InputError

def test_channel_is_dict():
    clear_v1()
    u_id = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    channel_id = channels_create_v1(u_id, 'league', True)
    
    # isinstance returns true when the type of 2 parameters are equal.
    assert(isinstance(channel_id, dict) == True) 

def test_multiple_channels_id():
    clear_v1()
    u_id1 = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    u_id2 = auth_register_v1('liaowang@gmail.com', 'liaowang0207', 'wang', 'liao')
    channel_id_1 = channels_create_v1(u_id1, 'league', True)
    channel_id_2 = channels_create_v1(u_id2, 'league', False)
    
    assert(channel_id_1['channel_id'] == 1)
    assert(channel_id_2['channel_id'] == 2)

def test_no_channel_name():
    clear_v1()
    u_id = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')

    with pytest.raises(InputError):
        channels_create_v1(u_id, "", True)

def channel_invalid_user_id():
    clear_v1()
    invalid_u_id1 = 0
    invalid_u_id2 = -1

    with pytest.raises(InputError):
        channels_create_v1(invalid_u_id1, "name", True)
    with pytest.raises(InputError):
        channels_create_v1(invalid_u_id2, "name", False)
    
def test_invalid_channel_name_short():
    # Raise an InputError when the channel's name
    # is less than 1 char
    clear_v1()
    u_id = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    
    with pytest.raises(InputError):
        channels_create_v1(u_id, "", True)
    with pytest.raises(InputError):
        channels_create_v1(u_id, "", False)

def test_invalid_channel_name_long():
    # Raise an InputError when the channel's name
    # is more than 20 char
    clear_v1()
    u_id = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    
    with pytest.raises(InputError):
        channels_create_v1(u_id, "aaaabbbbccccddddeeee1", True)
    with pytest.raises(InputError):
        channels_create_v1(u_id, "1234567890??????????????", False)
