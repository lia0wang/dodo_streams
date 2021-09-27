import pytest

from src.other import clear_v1
from src.data_store import data_store
from src.auth import auth_register_v1
from src.channels import channels_create_v1, channels_list_v1
from src.channel import channel_invite_v1
from src.error import InputError

# Entered auth_u_id is incorrect
def test_nonexistent_auth_uid():
    clear_v1()
    assert channels_list_v1(35) == {}

# No channels are created
def test_no_channels():
    clear_v1()
    auth_user_id = auth_register_v1("bob123@gmail.com", "qwerty", "Bob", "Marley")
    # Need to check this
    assert channels_list_v1(auth_user_id) == {}


# No channels the auth_u_id is part of
def test_no_channels_for_user():
    clear_v1()
    auth_user_id0 = auth_register_v1("bob123@gmail.com", "qwerty", "Bob", "Marley")
    auth_user_id1 = auth_register_v1("bill123@gmail.com", "asdfgh", "Bill", "Gates")
    channels_create_v1(auth_user_id1, False)
    assert channels_list_v1(auth_user_id0) == {}



# No members except auth_u_id in channels
def test_no_members_of_channel():
    clear_v1()
    auth_user_id0 = auth_register_v1("bob123@gmail.com", "qwerty", "Bob", "Marley")
    channel_id = channels_create_v1(auth_user_id0, "test_channel", False)
    assert channels_list_v1(auth_user_id0) == {'channels': [{'channel_id': channel_id, 'name': "test_channel"}]}


# Public channel with many users
def test_many_users_in_channel():
    clear_v1()
    auth_user_id0 = auth_register_v1("bob123@gmail.com", "qwerty", "Bob", "Marley")
    channel_id = channels_create_v1(auth_user_id0, "test_channel", True)
    auth_user_id1 = auth_register_v1("bill123@gmail.com", "asdfgh", "Bill", "Gates")
    auth_user_id2 = auth_register_v1("tardis@gmail.com", "thedoctor", "John", "Smith")
    auth_user_id3 = auth_register_v1("sauron@gmail.com", "theshire", "Frodo", "Baggins")
    channel_invite_v1(auth_u_id0, channel_id, auth_user_id1)
    channel_invite_v1(auth_u_id0, channel_id, auth_user_id2)
    channel_invite_v1(auth_u_id0, channel_id, auth_user_id3)
    assert channels_list_v1(auth_u_id0) == {'channels': [{'channel_id': channel_id, 'name': "test_channel"}]}



# Private channel with auth_u_id
def test_private_channels():
    clear_v1()
    auth_user_id0 = auth_register_v1("bob123@gmail.com", "qwerty", "Bob", "Marley")
    channel_id = channels_create_v1(auth_user_id0, "test_channel", False)
    auth_user_id1 = auth_register_v1("bill123@gmail.com", "asdfgh", "Bill", "Gates")
    auth_user_id2 = auth_register_v1("tardis@gmail.com", "thedoctor", "John", "Smith")
    auth_user_id3 = auth_register_v1("sauron@gmail.com", "theshire", "Frodo", "Baggins")
    channel_invite_v1(auth_u_id0, channel_id, auth_user_id1)
    channel_invite_v1(auth_u_id0, channel_id, auth_user_id2)
    channel_invite_v1(auth_u_id0, channel_id, auth_user_id3)
    assert channels_list_v1(auth_u_id0) == {'channels': [{'channel_id': channel_id, 'name': "test_channel"}]}