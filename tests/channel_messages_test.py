import pytest
from src.auth import auth_register_v1
from src.channel import channel_messages_v1
from src.channels import channels_create_v1
from src.error import InputError, AccessError
from src.other import clear_v1

def test_start_more_than_total_messages():
    '''
    When start is more than total messsages it returns input error
    '''
    clear_v1()
    user = auth_register_v1(
        "JoJo@gmail.com", "HermitPurple", "Joseph", "Joestar")
    channel = channels_create_v1(user['auth_user_id'], 'league', True)
    start = 1

    with pytest.raises(InputError):
        channel_messages_v1(user['auth_user_id'], channel['channel_id'], start)

def test_channel_id_not_valid():
    '''
    When a channel id does not exist/not created
    '''
    clear_v1()
    user = auth_register_v1(
        "JoJo@gmail.com", "HermitPurple", "Joseph", "Joestar")
    channel = channels_create_v1(user['auth_user_id'], 'league', True)
    start = 0
    invalid_channel_id_1 = channel['channel_id'] + 1
    invalid_channel_id_2 = -1

    # the invalid_channel_id_1 does not exist
    # the invalid_channel_id_2 is negative

    with pytest.raises(InputError):
        channel_messages_v1(user['auth_user_id'], invalid_channel_id_1, start)
    with pytest.raises(InputError):
        channel_messages_v1(user['auth_user_id'], invalid_channel_id_2, start)


def test_auth_user_id_not_member_of_channel():
    '''
    Tests when auth_user_id is not a member of a channel
    first case: is_public ->true
    second case: is_public ->false

    '''
    clear_v1()
    user_1 = auth_register_v1(
        "JoJo@gmail.com", "HermitPurple", "Joseph", "Joestar")
    invalid_user_id = user_1['auth_user_id'] + 1
    start = 0

    channel_id = channels_create_v1(user_1['auth_user_id'], 'league', True)
    channel_id2 = channels_create_v1(user_1['auth_user_id'], 'league2', False)

    with pytest.raises(AccessError):
        channel_messages_v1(invalid_user_id, channel_id['channel_id'], start)

    with pytest.raises(AccessError):
        channel_messages_v1(invalid_user_id, channel_id2['channel_id'], start)


def test_channel_id_and_auth_user_id_invalid():
    '''
    Tests when auth_user_id is not a member of a channel and channel id
    is not valid.
    '''
    clear_v1()
    user = auth_register_v1(
        "JoJo@gmail.com", "HermitPurple", "Joseph", "Joestar")
    invalid_user_id = user['auth_user_id'] + 1

    channel = channels_create_v1(user['auth_user_id'], 'league', True)
    start = 0
    invalid_channel_id_1 = channel['channel_id'] + 1

    with pytest.raises(InputError):
        channel_messages_v1(invalid_user_id, invalid_channel_id_1, start)

