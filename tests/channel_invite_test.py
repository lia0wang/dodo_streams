import pytest
from src.other import clear_v1
from src.auth import auth_register_v1
from src.channel import channel_join_v1
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
    auth_id1 = user1['auth_user_id']
    auth_id2 = user2['auth_user_id']
    channel = channels_create_v1(auth_id1, 'comp1531', True)
    channel_id = channel["channel_id"]
    channel_invite_v1(auth_id1,channel_id,auth_id2)

    channel_test_id = channels_listall_v1(auth_id2)
    output = channel_test_id['channels'][0]['channel_id']
    
    assert output == 1


