import pytest
from src.other import clear_v1
from src.auth import auth_register_v1
from src.channel import channel_join_v1
from src.channels import channels_create_v1
from src.error import InputError, AccessError

def test_join_private_channel():
    '''
    Test when the channel is private and the user is not a channel member and a global owner.
    '''
    clear_v1()
    u_id_1 = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    # Create a private channel called channel_id with u_id_1 as its member and owner.
    channel_id = channels_create_v1(u_id_1['auth_user_id'], 'league', False)

    # Create another user who is not either a channel member or global owner.
    u_id_2 = auth_register_v1('shifan@gmail.com', 'shifan0207', 'shifan', 'chen')

    with pytest.raises(AccessError):
        channel_join_v1(u_id_2['auth_user_id'], channel_id)

def test_duplicated_joins():
    '''
    Test join a channel when the authorised user is alredy a member of the channel.
    '''
    clear_v1()
    u_id = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    channel_id = channels_create_v1(u_id['auth_user_id'], 'league', True)
    
    # Now the u_id is the member in the created channel, try joining the channel again.
    with pytest.raises(InputError):
        channel_join_v1(u_id['auth_user_id'], channel_id)

def test_invalid_channel_id():
    '''
    Test join a channel when channel_id is invalid.
    '''
    clear_v1()
    u_id = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    channel_id = channels_create_v1(u_id['auth_user_id'], 'league', True)
    
    # the invalid_channel_id_1 does not exist
    invalid_channel_id_1 = channel_id['channel_id'] + 1
    # the invalid_channel_id_2 is negative
    invalid_channel_id_2 = -1

    with pytest.raises(InputError):
        channel_join_v1(u_id['auth_user_id'], invalid_channel_id_1)
    with pytest.raises(InputError):
        channel_join_v1(u_id['auth_user_id'], invalid_channel_id_2)
    
    
