import pytest
from src.other import clear_v1
from src.auth import auth_register_v1
from src.channel import channel_invite_v1
from src.channels import channels_create_v1
from src.message import message_send_v1, message_senddm_v1
from src.dm import dm_create_v1
from src.user import user_stats_v1
from src.helper import create_jwt, create_session_id
from src.data_store import data_store
from src.error import InputError, AccessError
'''
def test_one_hundred_percent():
    clear_v1()
    session_id = create_session_id()
    
    user1 = auth_register_v1("AgentSmith@hotmail.com", "abcd1234", "Agent", "Smith")
    u_id_1 = user1['auth_user_id']
    token_1 = create_jwt(u_id_1, session_id)
    
    channel = channels_create_v1(u_id_1, 'comp1531', True)
    channel_id = channel["channel_id"]

    user2 = auth_register_v1("JohnSmith@hotmail.com", "abcd1234", "John", "Smith")
    u_id_2 = user2['auth_user_id']
    u_ids = [u_id_2]
    dm_id = dm_create_v1(u_id_1,u_ids)['dm_id']

    msg_1 = ','
    message_send_v1(token_1, channel_id, msg_1)['message_id']
    message_senddm_v1(token_1, dm_id, msg_1)
    
    assert user_stats_v1(token_1)['involvement_rate'][0] == 1
'''
