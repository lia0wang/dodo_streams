import pytest
from src.other import clear_v1
from src.auth import auth_register_v1, auth_login_v1
from src.channel import channel_join_v1, channel_messages_v1
from src.channels import channels_listall_v1, channels_create_v1
from src.error import InputError, AccessError

def test_return_type():
    """ 
    Test if the ruturn type for clear_v1 is {}
    """
    assert clear_v1() == {}

def test_clear_user():
    """ 
    Test if clear_v1 successfully clear the user
    """
    clear_v1()
    user = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    clear_v1()

    with pytest.raises(InputError):
        auth_login_v1('wangliao@gmail.com', 'liaowang0207')

def test_clear_channel():
    """ 
    Test if clear_v1 successfully clear the channel
    """
    clear_v1()
    user_1 = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    channel_1 = channels_create_v1(user_1['auth_user_id'], 'league', True)
    user_2 = auth_register_v1('shifan@gmail.com', 'shifan0207', 'shifan', 'chen')
    channel_2 = channels_create_v1(user_2['auth_user_id'], 'legend', True)
    
    channel_join_v1(user_2['auth_user_id'], channel_1['channel_id'])
    channel_join_v1(user_1['auth_user_id'], channel_2['channel_id'])
    
    clear_v1()
        
    with pytest.raises(AccessError):
        channels_listall_v1(user_1['auth_user_id'])
        channels_listall_v1(user_2['auth_user_id'])

def test_clear_message():
    """ 
    Test if clear_v1 successfully clear the channel
    """
    clear_v1()
    user_1 = auth_register_v1('JohnSmith@hotmail.com', 'abcd1234', 'John', 'Smith')
    user_2 = auth_register_v1('AgentSmith@gmail.com', 'abcd1234', 'Agent', 'Smith')
    channel_1 = channels_create_v1(user_1['auth_user_id'], 'matrix', True)
    channel_2 = channels_create_v1(user_2['auth_user_id'], 'matrix', True)
    start_1 = 1
    start_2 = 50
    clear_v1()
        
    with pytest.raises(InputError):
        channel_messages_v1(user_1['auth_user_id'], channel_1['channel_id'], start_1)
        channel_messages_v1(user_2['auth_user_id'], channel_2['channel_id'], start_2)
