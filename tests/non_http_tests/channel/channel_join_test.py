import pytest
from src.other import clear_v1
from src.auth import auth_register_v1
from src.channel import channel_join_v1
from src.channels import channels_create_v1, channels_list_v1
from src.error import InputError, AccessError


def test_global_owner():
    '''
    Test if a global owner can join the private channel.
    '''
    clear_v1()
    global_owner = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    user_2 = auth_register_v1('shifan@gmail.com', 'shifan0207', 'shifan', 'chen')
    user_3 = auth_register_v1('jojo@gmail.com', 'jojo1234', 'jo', 'jo')

    channel = channels_create_v1(user_3['auth_user_id'], 'league', False)
    channel_join_v1(global_owner['auth_user_id'], channel['channel_id'])

    # the first created user is a global owner who can join the private channel.
    assert channels_list_v1(global_owner['auth_user_id']) == {'channels': [{'channel_id': 1, 'name': 'league'}]}
    
    # the user 2 is not a global owner nor a member so he cant join the private channel.
    with pytest.raises(AccessError):
        channel_join_v1(user_2['auth_user_id'], channel['channel_id'])
        
def test_none_existing_channel():
    clear_v1()
    user = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    with pytest.raises(InputError):
        channel_join_v1(user['auth_user_id'], 1)

def test_invalid_uid():
    '''
    Test when the user id is invalid
    '''
    clear_v1()
    user = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    channel = channels_create_v1(user['auth_user_id'], 'league', True)
    
    # The invalid user ID which is not existing.
    invalid_user = user['auth_user_id'] + 1
    
    with pytest.raises(AccessError):
        channel_join_v1(invalid_user, channel['channel_id'])
    with pytest.raises(AccessError):
        channel_join_v1(-1, channel['channel_id'])

def test_join_private_channel():
    '''
    Test when the channel is private and the user is not a channel member and a global owner.
    '''
    clear_v1()
    user_1 = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    
    # Create a private channel called channel_id with user_1 as its member and owner.
    channel = channels_create_v1(user_1['auth_user_id'], 'league', False)
    
    # Create another user who is not either a channel member or global owner.
    user_2 = auth_register_v1('shifan@gmail.com', 'shifan0207', 'shifan', 'chen')

    with pytest.raises(AccessError):
        channel_join_v1(user_2['auth_user_id'], channel['channel_id'])
    with pytest.raises(AccessError):
        channel_join_v1(-1, channel['channel_id'])

def test_duplicated_joins():
    '''
    Test join a channel when the authorised user is alredy a member of the channel.
    '''
    clear_v1()
    user = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    channel = channels_create_v1(user['auth_user_id'], 'league', True)
    
    # Now the user where the member in the created channel, try joining the channel again.
    with pytest.raises(InputError):
        channel_join_v1(user['auth_user_id'], channel['channel_id'])

def test_invalid_channel_id():
    '''
    Test join a channel when channel_id is invalid.
    '''
    clear_v1()
    user = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    channel = channels_create_v1(user['auth_user_id'], 'league', True)
    
    # the invalid_channel_id_1 does not exist
    # the invalid_channel_id_2 is negative
    invalid_channel_id_1 = channel['channel_id'] + 1
    invalid_channel_id_2 = -1

    with pytest.raises(InputError):
        channel_join_v1(user['auth_user_id'], invalid_channel_id_1)
    with pytest.raises(InputError):
        channel_join_v1(user['auth_user_id'], invalid_channel_id_2)
    
    
