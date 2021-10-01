import pytest

from src.other import clear_v1
from src.auth import auth_register_v1
from src.channels import channels_create_v1, channels_list_v1
from src.channel import channel_invite_v1
from src.error import InputError


def test_nonexistent_auth_uid():
    clear_v1()
    with pytest.raises(InputError):
        channels_list_v1(35)

def test_no_channels():
    clear_v1()
    auth_user_id = auth_register_v1("bob123@gmail.com", "qwerty", "Bob", "Marley")
    assert channels_list_v1(auth_user_id['auth_user_id']) == {'channels': []}


def test_no_channels_for_user():
    clear_v1()
    auth_user_id0 = auth_register_v1("bob123@gmail.com", "qwerty", "Bob", "Marley")
    auth_user_id1 = auth_register_v1("bill123@gmail.com", "asdfgh", "Bill", "Gates")
    channels_create_v1(auth_user_id1['auth_user_id'], "test_channel", False)
    assert channels_list_v1(auth_user_id0['auth_user_id']) == {'channels': []}


def test_single_channel():
    clear_v1()
    auth_user_id0 = auth_register_v1("bob123@gmail.com", "qwerty", "Bob", "Marley")
    channel_id = channels_create_v1(auth_user_id0['auth_user_id'], "test_channel", False)
    assert channels_list_v1(auth_user_id0['auth_user_id']) == {'channels': [{'channel_id': channel_id['channel_id'], 
    'name': "test_channel"}]}


def test_multiple_channels():
    clear_v1()
    auth_user_id0 = auth_register_v1("bob123@gmail.com", "qwerty", "Bob", "Marley")
    auth_user_id1 = auth_register_v1("bill123@gmail.com", "asdfgh", "Bill", "Gates")
    auth_user_id2 = auth_register_v1("tardis@gmail.com", "thedoctor", "John", "Smith")
    auth_user_id3 = auth_register_v1("sauron@gmail.com", "theshire", "Frodo", "Baggins")
    channel_id1 = channels_create_v1(auth_user_id0['auth_user_id'], "test_channel1", True)
    channel_id2 = channels_create_v1(auth_user_id0['auth_user_id'], "test_channel2", True)
    channel_id3 = channels_create_v1(auth_user_id0['auth_user_id'], "test_channel3", True)
    channel_invite_v1(auth_user_id0['auth_user_id'], channel_id1['channel_id'], auth_user_id1['auth_user_id'])
    channel_invite_v1(auth_user_id0['auth_user_id'], channel_id2['channel_id'], auth_user_id2['auth_user_id'])
    channel_invite_v1(auth_user_id0['auth_user_id'], channel_id3['channel_id'], auth_user_id3['auth_user_id'])
    assert channels_list_v1(auth_user_id0['auth_user_id']) == {'channels': [{'channel_id': channel_id1['channel_id'], 'name': "test_channel1"},
    {'channel_id': channel_id2['channel_id'], 'name': "test_channel2"}, {'channel_id': channel_id3['channel_id'], 'name': "test_channel3"}]}