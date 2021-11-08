import pytest
from src.error import AccessError, InputError
from src.other import clear_v1
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.standup import standup_send_v1

def test_invalid_channel_id():
    '''
    Test when channel_id is invalid.
    '''
    clear_v1()
    user = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    channel = channels_create_v1(user['auth_user_id'], 'league', True)
    message = "backend alot fun?"

    invalid_channel_id_1 = channel['channel_id'] + 999
    invalid_channel_id_2 = -1

    with pytest.raises(InputError):
        standup_send_v1(user['auth_user_id'], invalid_channel_id_1, message)
    with pytest.raises(InputError):
        standup_send_v1(user['auth_user_id'], invalid_channel_id_2, message)

def test_invalid_msg():
    ''''
    Test when the msg is too long.
    '''
    clear_v1()
    user = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    channel = channels_create_v1(user['auth_user_id'], 'league', True)
    message = "backend alot fun?" * 200
    with pytest.raises(InputError):
        standup_send_v1(user['auth_user_id'], channel['channel_id'], message)

def test_invalid_token():
    '''
    Test when the token is invalid.
    '''
    clear_v1()
    user = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    channel = channels_create_v1(user['auth_user_id'], 'league', True)
    message = "backend alot fun?"

    invalid_auth_id = user['auth_user_id'] + 999
    with pytest.raises(AccessError):
        standup_send_v1(invalid_auth_id, channel['channel_id'], message)

def test_auth_not_member():
    '''
    Test when the auth user is not a member of the channel.
    '''
    clear_v1()
    user = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    channel = channels_create_v1(user['auth_user_id'], 'league', True)
    message = "backend alot fun?"

    user_not_member = auth_register_v1('shifanchen@gmail.com', 'shifanchen0326', 'shifan', 'chen')

    with pytest.raises(AccessError):
        standup_send_v1(user_not_member['auth_user_id'], channel['channel_id'], message)
    with pytest.raises(AccessError):
        standup_send_v1(user_not_member['auth_user_id'], channel['channel_id'], message)

def test_standup_active():
    '''
    Test if the standup is running in the currently channel.
    '''
    clear_v1()
    user = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    channel = channels_create_v1(user['auth_user_id'], 'league', True)
    message = "backend alot fun?"

    with pytest.raises(InputError):
        standup_send_v1(user['auth_user_id'], channel['channel_id'], message)