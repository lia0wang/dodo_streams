import pytest
from src.other import clear_v1
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.error import InputError

def test_channel_type():
    '''
    Test if the channel_id type is dictionary.
    '''
    clear_v1()
    u_id = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    channel_id = channels_create_v1(u_id['auth_user_id'], 'league', True)
    
    # isinstance returns true when the type of 2 parameters are equal.
    assert(isinstance(channel_id, dict) == True)
    assert(isinstance(u_id, dict) == True) 
    assert(isinstance(u_id['auth_user_id'], int) == True) 

def test_multiple_channels():
    '''
    Test when create multipel channels with unique channel_id.
    '''
    clear_v1()
    u_id1 = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    u_id2 = auth_register_v1('liaowang@gmail.com', 'liaowang0207', 'wang', 'liao')
    channel_id_1 = channels_create_v1(u_id1['auth_user_id'], 'league', True)
    channel_id_2 = channels_create_v1(u_id2['auth_user_id'], 'league', False)
    
    assert(channel_id_1['channel_id'] == 1)
    assert(channel_id_2['channel_id'] == 2)
    
def test_no_channel_name():
    '''
    Test when the channel name is empty
    '''
    clear_v1()
    u_id = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')

    with pytest.raises(InputError):
        channels_create_v1(u_id['auth_user_id'], "", True)

def channel_invalid_user_id():
    '''
    Test create the channels with invalid user ID.
    '''
    clear_v1()
    invalid_u_id1 = 0
    invalid_u_id2 = -1

    with pytest.raises(InputError):
        channels_create_v1(invalid_u_id1, "name", True)
    with pytest.raises(InputError):
        channels_create_v1(invalid_u_id2, "name", False)
    
def test_invalid_channel_name_short():
    '''
    Test when the length of channel name is less than 1 char.
    '''
    clear_v1()
    u_id = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    
    with pytest.raises(InputError):
        channels_create_v1(u_id['auth_user_id'], "", True)
    with pytest.raises(InputError):
        channels_create_v1(u_id['auth_user_id'], "", False)

def test_invalid_channel_name_long():
    '''
    Test when the length of channel name is more than 20 char.
    '''
    clear_v1()
    u_id = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    
    with pytest.raises(InputError):
        channels_create_v1(u_id['auth_user_id'], "aaaabbbbccccddddeeee1", True)
    with pytest.raises(InputError):
        channels_create_v1(u_id['auth_user_id'], "1234567890??????????????", False)
