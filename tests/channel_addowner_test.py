from types import new_class
import pytest
from src.other import clear_v1
from src.auth import auth_register_v1
from src.channel import channel_join_v1, channel_details_v1, channel_addowner_v1
from src.channels import channels_create_v1
from src.error import InputError, AccessError

def test_invalid_channel_id():
    '''
    Test when the channel_id is invalid
    '''
    clear_v1()
    owner = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    channel = channels_create_v1(owner['auth_user_id'], 'league', True)
    invalid_channel_id_1 = channel['channel_id'] + 1
    invalid_channel_id_2 = -1

    user = auth_register_v1('chenshifan@gmail.com', 'chenshifan0207', 'shifan', 'chen')

    with pytest.raises(InputError):
        channel_addowner_v1(owner['auth_user_id'], invalid_channel_id_1, user['auth_user_id'])
    with pytest.raises(InputError):
        channel_addowner_v1(owner['auth_user_id'], invalid_channel_id_2, user['auth_user_id'])
    
def test_invalid_user_id():
    '''
    Test when the user id is invalid
    '''
    clear_v1()
    owner = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    channel = channels_create_v1(owner['auth_user_id'], 'league', True)

    user = auth_register_v1('chenshifan@gmail.com', 'chenshifan0207', 'shifan', 'chen')

    with pytest.raises(InputError):
        channel_addowner_v1(owner['auth_user_id'], channel['channel_id'], user['auth_user_id'] + 999)
    with pytest.raises(InputError):
        channel_addowner_v1(owner['auth_user_id'], channel['channel_id'], -1)

def test_invalid_auth_user_id():
    '''
    Test when the auth user id is invalid
    '''
    clear_v1()
    owner = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    channel = channels_create_v1(owner['auth_user_id'], 'league', True)

    user = auth_register_v1('chenshifan@gmail.com', 'chenshifan0207', 'shifan', 'chen')

    with pytest.raises(AccessError):
        channel_addowner_v1(owner['auth_user_id'] + 999, channel['channel_id'], user['auth_user_id'])
    with pytest.raises(AccessError):
        channel_addowner_v1(-1, channel['channel_id'], user['auth_user_id'])

def test_non_exist_user():
    '''
    Test when the user is not a member of the channel
    '''
    clear_v1()
    owner = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    channel = channels_create_v1(owner['auth_user_id'], 'league', True)

    user = auth_register_v1('chenshifan@gmail.com', 'chenshifan0207', 'shifan', 'chen')
    
    with pytest.raises(InputError):
        channel_addowner_v1(owner['auth_user_id'], channel['channel_id'], user['auth_user_id'])

def test_add_exist_owner():
    '''
    Test when the user is already a owner of the chanenl
    '''
    clear_v1()
    owner = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    channel = channels_create_v1(owner['auth_user_id'], 'league', True)
    
    user = auth_register_v1('chenshifan@gmail.com', 'chenshifan0207', 'shifan', 'chen')
    channel_join_v1(user['auth_user_id'], channel['channel_id'])
    channel_addowner_v1(owner['auth_user_id'], channel['channel_id'], user['auth_user_id'])

    assert user['auth_user_id'] in [user['u_id'] for user in channel_details_v1(owner['auth_user_id'], channel['channel_id'])['owner_members']]
    assert user['auth_user_id'] in [user['u_id'] for user in channel_details_v1(owner['auth_user_id'], channel['channel_id'])['all_members']]

    with pytest.raises(InputError):
        channel_addowner_v1(owner['auth_user_id'], channel['channel_id'], user['auth_user_id'])

def test_no_permission():
    '''
    Test when the auth user has no owner permission
    '''
    clear_v1()
    owner = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    channel = channels_create_v1(owner['auth_user_id'], 'league', True)

    assert owner['auth_user_id'] in [user['u_id'] for user in channel_details_v1(owner['auth_user_id'], channel['channel_id'])['owner_members']]

    user = auth_register_v1('chenshifan@gmail.com', 'chenshifan0207', 'shifan', 'chen')
    channel_join_v1(user['auth_user_id'], channel['channel_id'])

    assert user['auth_user_id'] in [user['u_id'] for user in channel_details_v1(owner['auth_user_id'], channel['channel_id'])['all_members']]
    assert user['auth_user_id'] not in [user['u_id'] for user in channel_details_v1(owner['auth_user_id'], channel['channel_id'])['owner_members']]

    new_user = auth_register_v1('haha@gmail.com', 'haha0207', 'ha', 'ha')
    channel_join_v1(new_user['auth_user_id'], channel['channel_id'])

    with pytest.raises(AccessError):
        channel_addowner_v1(user['auth_user_id'], channel['channel_id'], new_user['auth_user_id'])

def test_channel_addowner_basic():
    '''
    Test if channel/addowner/v1 working properly
    '''
    clear_v1()
    owner = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    channel = channels_create_v1(owner['auth_user_id'], 'league', True)

    user = auth_register_v1('chenshifan@gmail.com', 'chenshifan0207', 'shifan', 'chen')
    channel_join_v1(user['auth_user_id'], channel['channel_id'])
    new_user = auth_register_v1('haha@gmail.com', 'haha0207', 'ha', 'ha')
    channel_join_v1(new_user['auth_user_id'], channel['channel_id'])

    channel_addowner_v1(owner['auth_user_id'], channel['channel_id'], user['auth_user_id'])
    channel_addowner_v1(owner['auth_user_id'], channel['channel_id'], new_user['auth_user_id'])

    assert user['auth_user_id'] in [user['u_id'] for user in channel_details_v1(owner['auth_user_id'], channel['channel_id'])['owner_members']]
    assert user['auth_user_id'] in [user['u_id'] for user in channel_details_v1(owner['auth_user_id'], channel['channel_id'])['owner_members']]
