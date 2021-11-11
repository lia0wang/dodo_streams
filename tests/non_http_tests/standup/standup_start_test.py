import pytest
from src.error import AccessError, InputError
from src.other import clear_v1
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.channel import channel_messages_v1
from src.standup import standup_active_v1, standup_send_v1, standup_start_v1
from src.notifications import notifications_v1

def test_invalid_channel_id():
    '''
    Test when channel_id is invalid.
    '''
    clear_v1()
    user = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    channel = channels_create_v1(user['auth_user_id'], 'league', True)

    invalid_channel_id_1 = channel['channel_id'] + 999
    invalid_channel_id_2 = -1

    with pytest.raises(InputError):
        standup_start_v1(user['auth_user_id'], invalid_channel_id_1, 100)
    with pytest.raises(InputError):
        standup_start_v1(user['auth_user_id'], invalid_channel_id_2, 100)

def test_invalid_token():
    '''
    Test when the token is invalid.
    '''
    clear_v1()
    user = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    channel = channels_create_v1(user['auth_user_id'], 'league', True)

    invalid_auth_id = user['auth_user_id'] + 999
    with pytest.raises(AccessError):
        standup_start_v1(invalid_auth_id, channel['channel_id'], 100)

def test_length_negative():
    '''
    Test if the length is negative.
    '''
    clear_v1()
    user = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    channel = channels_create_v1(user['auth_user_id'], 'league', True)
    with pytest.raises(InputError):
        standup_start_v1(user['auth_user_id'], channel['channel_id'], -1)
    with pytest.raises(InputError):
        standup_start_v1(user['auth_user_id'], channel['channel_id'], -99)

def test_auth_not_member():
    '''
    Test when the auth user is not a member of the channel.
    '''
    clear_v1()
    user = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    channel = channels_create_v1(user['auth_user_id'], 'league', True)

    user_not_member = auth_register_v1('shifanchen@gmail.com', 'shifanchen0326', 'shifan', 'chen')

    with pytest.raises(AccessError):
        standup_start_v1(user_not_member['auth_user_id'], channel['channel_id'], 100)
    with pytest.raises(AccessError):
        standup_start_v1(user_not_member['auth_user_id'], channel['channel_id'], 100)

def test_standup_is_running():
    '''
    Test if the standup is running in the current chanenl.
    '''
    clear_v1()
    user = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    channel = channels_create_v1(user['auth_user_id'], 'league', True)

    standup_start_v1(user['auth_user_id'], channel['channel_id'], 1)
    with pytest.raises(InputError):
        standup_start_v1(user['auth_user_id'], channel['channel_id'], 3)


def test_standup_start_basic():
    '''
    Test if standup working properly
    '''
    clear_v1()
    user = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    channel = channels_create_v1(user['auth_user_id'], 'league', True)

    standup_start_v1(user['auth_user_id'], channel['channel_id'], 3)
    active_return = standup_active_v1(user['auth_user_id'], channel['channel_id'])
    
    assert active_return["is_active"] == True

