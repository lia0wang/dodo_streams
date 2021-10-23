import pytest
from src.other import clear_v1
from src.auth import auth_register_v1
from src.channel import channel_join_v1, channel_leave_v1
from src.channel import channel_invite_v1
from src.channels import channels_create_v1
from src.channels import channels_listall_v1
from src.error import InputError, AccessError
from src.data_store import data_store

def test_valid_input():
    '''tests for valid channel_invite_v1 implementation'''
    clear_v1()
    user1 = auth_register_v1("AgentSmith@hotmail.com", "abcd1234", "Agent", "Smith")
    user2 = auth_register_v1("JohnSmith@hotmail.com", "abcd1234", "John", "Smith")
    auth_id = user1['auth_user_id']
    u_id = user2['auth_user_id']
    channel = channels_create_v1(auth_id, 'comp1531', True)
    channel_id = channel["channel_id"]
    channel_invite_v1(auth_id,channel_id,u_id)

    channel_test_id = channels_listall_v1(u_id)
    output = channel_test_id['channels'][0]['channel_id']
    
    assert output == 1

'''Input Error Testing Module'''

def test_invalid_channel():
    '''tests for valid channel_invite_v1 with invalid channel_id'''
    clear_v1()
    user1 = auth_register_v1("AgentSmith@hotmail.com", "abcd1234", "Agent", "Smith")
    user2 = auth_register_v1("JohnSmith@hotmail.com", "abcd1234", "John", "Smith")
    auth_id = user1['auth_user_id']
    u_id = user2['auth_user_id']
    channel = channels_create_v1(auth_id, 'comp1531', True)
    channel_id = channel["channel_id"]
    channel_invite_v1(auth_id,channel_id,u_id)
    invalid_channel1 = channel_id + 999
    invalid_channel2 = -1
    
    with pytest.raises(InputError):
        channel_invite_v1(auth_id, invalid_channel1, u_id)
    with pytest.raises(InputError):
        channel_invite_v1(auth_id, invalid_channel2, u_id)

def test_invalid_user():
    '''tests for valid channel_invite_v1 with invalid auth_user_id or u_id'''
    clear_v1()
    user1 = auth_register_v1("AgentSmith@hotmail.com", "abcd1234", "Agent", "Smith")
    user2 = auth_register_v1("JohnSmith@hotmail.com", "abcd1234", "John", "Smith")
    auth_id = user1['auth_user_id']
    u_id = user2['auth_user_id']
    invalid_auth_id = auth_id + 999
    invalid_u_id = u_id + 888
    channel = channels_create_v1(auth_id, 'comp1531', True)
    channel_id = channel["channel_id"]
    
    with pytest.raises(AccessError):
        channel_invite_v1(invalid_auth_id, channel_id, u_id)

    with pytest.raises(InputError):
        channel_invite_v1(auth_id, channel_id, invalid_u_id)

def test_repeated_user():
    '''tests for valid channel_invite_v1 with a user is already a member of the channel'''
    clear_v1()
    user1 = auth_register_v1("AgentSmith@hotmail.com", "abcd1234", "Agent", "Smith")
    user2 = auth_register_v1("JohnSmith@hotmail.com", "abcd1234", "John", "Smith")
    auth_id = user1['auth_user_id']
    u_id = user2['auth_user_id']
    channel = channels_create_v1(auth_id, 'comp1531', True)
    channel_id = channel["channel_id"]
    channel_invite_v1(auth_id, channel_id, u_id)

    with pytest.raises(InputError):
        channel_invite_v1(auth_id, channel_id, u_id)
    with pytest.raises(InputError):
        channel_invite_v1(auth_id, channel_id, auth_id)

def test_unauthorised_user():
    '''
    Tests for channel_id is valid and the authorised user
    is not a member of the channel
    '''
    clear_v1()
    owner = auth_register_v1("AgentSmith@hotmail.com", "abcd1234", "Agent", "Smith")
    user1 = auth_register_v1("JohnSmith@hotmail.com", "abcd1234", "John", "Smith")
    user2 = auth_register_v1("AgentJohnson@hotmail.com", "abcd1234", "Agent", "Johnson")

    channel = channels_create_v1(owner['auth_user_id'], 'comp1531', True)
    channel_invite_v1(owner['auth_user_id'], channel["channel_id"], user1['auth_user_id'])
    channel_leave_v1(owner['auth_user_id'], channel["channel_id"])

    with pytest.raises(AccessError):
        channel_invite_v1(owner['auth_user_id'], channel["channel_id"], user2['auth_user_id'])
