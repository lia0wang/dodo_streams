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
    channels_list_v1()

# No channels are created
def test_no_channels():
    clear_v1()


# No channels the auth_u_id is part of
def test_no_channels_for_user():
    clear_v1()


# No members except auth_u_id in channels
def test_no_members_of_channel():
    clear_v1()


# Public channel with many users
def test_many_users_in_channel():
    clear_v1()


# Private channel with auth_u_id
def test_private_channels():
    clear_v1()