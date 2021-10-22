import pytest
from src.other import clear_v1
from src.auth import auth_register_v1
from src.channel import channel_addowner_v1, channel_join_v1, channel_leave_v1, channel_details_v1
from src.channels import channels_create_v1
from src.error import InputError, AccessError

def test_invalid_channel_id():
    '''
    Test join a channel when channel_id is invalid.
    '''
    clear_v1()
    user = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    channel = channels_create_v1(user['auth_user_id'], 'league', True)
    user_2 = auth_register_v1('shifan@gmail.com', 'shifan0207', 'shifan', 'chen')
    channel_join_v1(user_2['auth_user_id'], channel['channel_id'])

    # the invalid_channel_id_1 does not exist
    # the invalid_channel_id_2 is negative
    invalid_channel_id_1 = channel['channel_id'] + 1
    invalid_channel_id_2 = -1

    with pytest.raises(InputError):
        channel_leave_v1(user_2['auth_user_id'], invalid_channel_id_1)
    with pytest.raises(InputError):
        channel_leave_v1(user['auth_user_id'], invalid_channel_id_2)

def test_invalid_token():
    '''
    Test when the user id is invalid
    '''
    clear_v1()
    user = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    channel = channels_create_v1(user['auth_user_id'], 'league', True)

    # The invalid user ID which is not existing.
    invalid_user = user['auth_user_id'] + 9999

    with pytest.raises(AccessError):
        channel_leave_v1(invalid_user, channel['channel_id'])
    with pytest.raises(AccessError):
        channel_leave_v1(-1, channel['channel_id'])

def test_user_is_not_member():
    '''
    Test when the user is not a member
    '''
    clear_v1()
    user = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    channel = channels_create_v1(user['auth_user_id'], 'league', True)

    user_2 = auth_register_v1('shifan@gmail.com', 'shifan0207', 'shifan', 'chen')
    channel_join_v1(user_2['auth_user_id'], channel['channel_id'])
    channel_leave_v1(user_2['auth_user_id'], channel['channel_id'])

    with pytest.raises(AccessError):
        channel_leave_v1(user_2['auth_user_id'], channel['channel_id'])

def test_owner_leave():
    '''
    Test when the owner leave, the owner should not be in
    both the all_members and owner_members list
    '''
    clear_v1()
    owner = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    channel = channels_create_v1(owner['auth_user_id'], 'league', True)

    assert owner['auth_user_id'] in [user['u_id'] for user in channel_details_v1(owner['auth_user_id'], channel['channel_id'])['owner_members']]
    assert owner['auth_user_id'] in [user['u_id'] for user in channel_details_v1(owner['auth_user_id'], channel['channel_id'])['all_members']]

    member = auth_register_v1('shifan@gmail.com', 'shifan0207', 'shifan', 'chen')
    channel_join_v1(member['auth_user_id'], channel['channel_id'])

    channel_leave_v1(owner['auth_user_id'], channel['channel_id'])

    assert owner['auth_user_id'] not in [user['u_id'] for user in channel_details_v1(member['auth_user_id'], channel['channel_id'])['owner_members']]
    assert owner['auth_user_id'] not in [user['u_id'] for user in channel_details_v1(member['auth_user_id'], channel['channel_id'])['all_members']]

def test_user_leave():
    '''
    Test when the owner leave, the owner should not be in the all_member list
    '''
    clear_v1()
    owner = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    channel = channels_create_v1(owner['auth_user_id'], 'league', True)

    member = auth_register_v1('shifan@gmail.com', 'shifan0207', 'shifan', 'chen')
    channel_join_v1(member['auth_user_id'], channel['channel_id'])

    assert member['auth_user_id'] not in [user['u_id'] for user in channel_details_v1(owner['auth_user_id'], channel['channel_id'])['owner_members']]
    assert member['auth_user_id'] in [user['u_id'] for user in channel_details_v1(owner['auth_user_id'], channel['channel_id'])['all_members']]

    channel_leave_v1(member['auth_user_id'], channel['channel_id'])
    
    assert member['auth_user_id'] not in [user['u_id'] for user in channel_details_v1(owner['auth_user_id'], channel['channel_id'])['owner_members']]
    assert member['auth_user_id'] not in [user['u_id'] for user in channel_details_v1(owner['auth_user_id'], channel['channel_id'])['all_members']]

def test_swap_and_leave_owner():
    '''
    Test to swap the owner of the channel
    '''
    clear_v1()
    owner = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    channel = channels_create_v1(owner['auth_user_id'], 'league', True)

    member = auth_register_v1('shifan@gmail.com', 'shifan0207', 'shifan', 'chen')
    channel_join_v1(member['auth_user_id'], channel['channel_id'])

    channel_addowner_v1(owner['auth_user_id'], channel['channel_id'], member['auth_user_id'])
    channel_leave_v1(owner['auth_user_id'], channel['channel_id'])

    assert member['auth_user_id'] in [user['u_id'] for user in channel_details_v1(member['auth_user_id'], channel['channel_id'])['owner_members']]
    assert member['auth_user_id'] in [user['u_id'] for user in channel_details_v1(member['auth_user_id'], channel['channel_id'])['all_members']]
    assert owner['auth_user_id'] not in [user['u_id'] for user in channel_details_v1(member['auth_user_id'], channel['channel_id'])['owner_members']]
    assert owner['auth_user_id'] not in [user['u_id'] for user in channel_details_v1(member['auth_user_id'], channel['channel_id'])['all_members']]