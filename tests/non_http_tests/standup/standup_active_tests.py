import pytest
from src.error import AccessError, InputError
from src.other import clear_v1
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.standup import standup_active_v1

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
        standup_active_v1(user['auth_user_id'], invalid_channel_id_1)
    with pytest.raises(InputError):
        standup_active_v1(user['auth_user_id'], invalid_channel_id_2)

def test_invalid_token():
    '''
    Test when the token is invalid.
    '''
    clear_v1()
    user = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    channel = channels_create_v1(user['auth_user_id'], 'league', True)

    invalid_auth_id = user['auth_user_id'] + 999
    with pytest.raises(AccessError):
        standup_active_v1(invalid_auth_id, channel['channel_id'])

def test_auth_not_member():
    '''
    Test when the auth user is not a member of the channel.
    '''
    clear_v1()
    user = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    channel = channels_create_v1(user['auth_user_id'], 'league', True)

    user_not_member = auth_register_v1('shifanchen@gmail.com', 'shifanchen0326', 'shifan', 'chen')

    with pytest.raises(AccessError):
        standup_active_v1(user_not_member['auth_user_id'], channel['channel_id'])
    with pytest.raises(AccessError):
        standup_active_v1(user_not_member['auth_user_id'], channel['channel_id'])

def test_standup_inactive():
    '''
    Test if the standup is inactive
    '''
    clear_v1()
    user = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    channel = channels_create_v1(user['auth_user_id'], 'league', True)
    
    standup_data = standup_active_v1(user['auth_user_id'], channel['channel_id'])
    assert standup_data['is_active'] == False
    assert standup_data['time_finish'] == None