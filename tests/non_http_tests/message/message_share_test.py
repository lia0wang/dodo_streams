import pytest
from src.other import clear_v1
from src.auth import auth_register_v1
from src.channel import channel_invite_v1
from src.channels import channels_create_v1
from src.message import message_send_v1, message_senddm_v1, message_share_v1
from src.dm import dm_create_v1
from src.helper import create_jwt, create_session_id
from src.data_store import data_store
from src.error import InputError, AccessError

def test_share_channel_source_basic():
    clear_v1()
    session_id = create_session_id()
    
    msg_1 = ','
    msg_2 = ',,'
    
    user1 = auth_register_v1("AgentSmith@hotmail.com", "abcd1234", "Agent", "Smith")
    u_id_1 = user1['auth_user_id']
    token_1 = create_jwt(u_id_1, session_id)

    channel = channels_create_v1(u_id_1, 'comp1531', True)
    channel_id = channel["channel_id"]

    user2 = auth_register_v1("JohnSmith@hotmail.com", "abcd1234", "John", "Smith")
    u_id_2 = user2['auth_user_id']
    token_2 = create_jwt(u_id_2, session_id)
    channel_invite_v1(u_id_1, channel_id, u_id_2)

    og_msg_id = message_send_v1(token_1, channel_id, msg_1)['message_id']    

    user3 = auth_register_v1("AgentJohnson@hotmail.com", "abcd1234", "Agent", "Johnson")
    u_id_3 = user3['auth_user_id']
    u_ids = [u_id_2]
    dm_id = dm_create_v1(u_id_3,u_ids)['dm_id']
    
    message_share_v1(token_2, og_msg_id, msg_2, -1, dm_id)
    message_share_v1(token_2, og_msg_id, msg_2, channel_id, -1)

def test_share_dm_source_basic():
    clear_v1()
    session_id = create_session_id()
    
    msg_1 = ','
    msg_2 = ',,'
    
    user1 = auth_register_v1("AgentSmith@hotmail.com", "abcd1234", "Agent", "Smith")
    u_id_1 = user1['auth_user_id']

    channel = channels_create_v1(u_id_1, 'comp1531', True)
    channel_id = channel["channel_id"]

    user2 = auth_register_v1("JohnSmith@hotmail.com", "abcd1234", "John", "Smith")
    u_id_2 = user2['auth_user_id']
    token_2 = create_jwt(u_id_2, session_id)
    channel_invite_v1(u_id_1, channel_id, u_id_2)

    user3 = auth_register_v1("AgentJohnson@hotmail.com", "abcd1234", "Agent", "Johnson")
    u_id_3 = user3['auth_user_id']
    token_3 = create_jwt(u_id_2, session_id)
    u_ids = [u_id_2]
    dm_id = dm_create_v1(u_id_3,u_ids)['dm_id']
    og_msg_id = message_senddm_v1(token_3, dm_id, msg_1)['message_id']
    
    message_share_v1(token_2, og_msg_id, msg_2, channel_id, -1)  
    message_share_v1(token_2, og_msg_id, msg_2, -1, dm_id)    

def test_share_invalid_length():
    clear_v1()
    session_id = create_session_id()
    
    msg_1 = ','
    msg_2 = ','*1001
    
    user1 = auth_register_v1("AgentSmith@hotmail.com", "abcd1234", "Agent", "Smith")
    u_id_1 = user1['auth_user_id']

    channel = channels_create_v1(u_id_1, 'comp1531', True)
    channel_id = channel["channel_id"]

    user2 = auth_register_v1("JohnSmith@hotmail.com", "abcd1234", "John", "Smith")
    u_id_2 = user2['auth_user_id']
    token_2 = create_jwt(u_id_2, session_id)
    channel_invite_v1(u_id_1, channel_id, u_id_2)

    user3 = auth_register_v1("AgentJohnson@hotmail.com", "abcd1234", "Agent", "Johnson")
    u_id_3 = user3['auth_user_id']
    token_3 = create_jwt(u_id_3, session_id)
    u_ids = [u_id_2]
    dm_id = dm_create_v1(u_id_3,u_ids)['dm_id']
    og_msg_id = message_senddm_v1(token_3, dm_id, msg_1)['message_id']
    with pytest.raises(InputError):
        message_share_v1(token_2, og_msg_id, msg_2, channel_id, -1)  

def test_share_undirected_1():
    clear_v1()
    session_id = create_session_id()
    
    msg_1 = ','
    msg_2 = ',,'
    
    user1 = auth_register_v1("AgentSmith@hotmail.com", "abcd1234", "Agent", "Smith")
    u_id_1 = user1['auth_user_id']
    token_1 = create_jwt(u_id_1, session_id)
    channel = channels_create_v1(u_id_1, 'comp1531', True)
    channel_id = channel["channel_id"]
    og_msg_id = message_send_v1(token_1, channel_id, msg_1)['message_id']    

    with pytest.raises(InputError):
        message_share_v1(token_1, og_msg_id, msg_2, -1, -1)

def test_share_undirected_2():
    clear_v1()
    session_id = create_session_id()
    
    msg_1 = ','
    msg_2 = ',,'
    
    user1 = auth_register_v1("AgentSmith@hotmail.com", "abcd1234", "Agent", "Smith")
    u_id_1 = user1['auth_user_id']
    token_1 = create_jwt(u_id_1, session_id)

    channel = channels_create_v1(u_id_1, 'comp1531', True)
    channel_id = channel["channel_id"]

    user2 = auth_register_v1("JohnSmith@hotmail.com", "abcd1234", "John", "Smith")
    u_id_2 = user2['auth_user_id']

    og_msg_id = message_send_v1(token_1, channel_id, msg_1)['message_id']    

    user3 = auth_register_v1("AgentJohnson@hotmail.com", "abcd1234", "Agent", "Johnson")
    u_id_3 = user3['auth_user_id']
    u_ids = [u_id_2]
    dm_id = dm_create_v1(u_id_3,u_ids)['dm_id']
    
    with pytest.raises(InputError):    
        message_share_v1(token_1, og_msg_id, msg_2, channel_id, dm_id)

def test_share_not_source_channel_member():
    clear_v1()
    session_id = create_session_id()
    
    msg_1 = ','
    msg_2 = ',,'
    
    user1 = auth_register_v1("AgentSmith@hotmail.com", "abcd1234", "Agent", "Smith")
    u_id_1 = user1['auth_user_id']
    token_1 = create_jwt(u_id_1, session_id)

    channel = channels_create_v1(u_id_1, 'comp1531', True)
    channel_id = channel["channel_id"]

    user2 = auth_register_v1("JohnSmith@hotmail.com", "abcd1234", "John", "Smith")
    u_id_2 = user2['auth_user_id']
    channel_invite_v1(u_id_1, channel_id, u_id_2)
    og_msg_id = message_send_v1(token_1, channel_id, msg_1)['message_id']

    user3 = auth_register_v1("AgentJohnson@hotmail.com", "abcd1234", "Agent", "Johnson")
    u_id_3 = user3['auth_user_id']
    token_3 = create_jwt(u_id_3, session_id)
    u_ids = [u_id_2]
    dm_id = dm_create_v1(u_id_3,u_ids)['dm_id']
    
    with pytest.raises(InputError):
        message_share_v1(token_3, og_msg_id, msg_2, -1, dm_id)    

def test_share_not_source_dm_member():
    clear_v1()
    session_id = create_session_id()
    
    msg_1 = ','
    msg_2 = ',,'
    
    user1 = auth_register_v1("AgentSmith@hotmail.com", "abcd1234", "Agent", "Smith")
    u_id_1 = user1['auth_user_id']
    token_1 = create_jwt(u_id_1, session_id)

    channel = channels_create_v1(u_id_1, 'comp1531', True)
    channel_id = channel["channel_id"]

    user2 = auth_register_v1("JohnSmith@hotmail.com", "abcd1234", "John", "Smith")
    u_id_2 = user2['auth_user_id']
    channel_invite_v1(u_id_1, channel_id, u_id_2)

    user3 = auth_register_v1("AgentJohnson@hotmail.com", "abcd1234", "Agent", "Johnson")
    u_id_3 = user3['auth_user_id']
    token_3 = create_jwt(u_id_3, session_id)
    u_ids = [u_id_2]
    dm_id = dm_create_v1(u_id_3,u_ids)['dm_id']
    og_msg_id = message_senddm_v1(token_3, dm_id, msg_1)['message_id']
    
    with pytest.raises(InputError):
        message_share_v1(token_1, og_msg_id, msg_2, channel_id, -1)      
        
def test_share_not_target_channel_member():
    clear_v1()
    session_id = create_session_id()
    
    msg_1 = ','
    msg_2 = ',,'
    
    user1 = auth_register_v1("AgentSmith@hotmail.com", "abcd1234", "Agent", "Smith")
    u_id_1 = user1['auth_user_id']

    channel = channels_create_v1(u_id_1, 'comp1531', True)
    channel_id = channel["channel_id"]

    user2 = auth_register_v1("JohnSmith@hotmail.com", "abcd1234", "John", "Smith")
    u_id_2 = user2['auth_user_id']
    token_2 = create_jwt(u_id_2, session_id)


    user3 = auth_register_v1("AgentJohnson@hotmail.com", "abcd1234", "Agent", "Johnson")
    u_id_3 = user3['auth_user_id']
    token_3 = create_jwt(u_id_3, session_id)
    u_ids = [u_id_2]
    dm_id = dm_create_v1(u_id_3,u_ids)['dm_id']
    og_msg_id = message_senddm_v1(token_3, dm_id, msg_1)['message_id']
    
    with pytest.raises(AccessError):
        message_share_v1(token_2, og_msg_id, msg_2, channel_id, -1)

def test_share_not_target_dm_member():
    clear_v1()
    session_id = create_session_id()
    
    msg_1 = ','
    msg_2 = ',,'
    
    user1 = auth_register_v1("AgentSmith@hotmail.com", "abcd1234", "Agent", "Smith")
    u_id_1 = user1['auth_user_id']
    token_1 = create_jwt(u_id_1, session_id)

    channel = channels_create_v1(u_id_1, 'comp1531', True)
    channel_id = channel["channel_id"]
    og_msg_id = message_send_v1(token_1, channel_id, msg_1)['message_id']

    user2 = auth_register_v1("JohnSmith@hotmail.com", "abcd1234", "John", "Smith")
    u_id_2 = user2['auth_user_id']

    user3 = auth_register_v1("AgentJohnson@hotmail.com", "abcd1234", "Agent", "Johnson")
    u_id_3 = user3['auth_user_id']
    u_ids = [u_id_2]
    dm_id = dm_create_v1(u_id_3,u_ids)['dm_id']
    
    with pytest.raises(AccessError):
        message_share_v1(token_1, og_msg_id, msg_2, -1, dm_id)

def test_share_invalid_channel_id():
    clear_v1()
    session_id = create_session_id()
    
    msg_1 = ','
    msg_2 = ',,'
    
    user1 = auth_register_v1("AgentSmith@hotmail.com", "abcd1234", "Agent", "Smith")
    u_id_1 = user1['auth_user_id']

    channel = channels_create_v1(u_id_1, 'comp1531', True)
    channel_id = channel["channel_id"]
    invalid_channel_id = channel["channel_id"]+999

    user2 = auth_register_v1("JohnSmith@hotmail.com", "abcd1234", "John", "Smith")
    u_id_2 = user2['auth_user_id']
    token_2 = create_jwt(u_id_2, session_id)
    channel_invite_v1(u_id_1, channel_id, u_id_2)

    user3 = auth_register_v1("AgentJohnson@hotmail.com", "abcd1234", "Agent", "Johnson")
    u_id_3 = user3['auth_user_id']
    token_3 = create_jwt(u_id_2, session_id)
    u_ids = [u_id_2]
    dm_id = dm_create_v1(u_id_3,u_ids)['dm_id']
    og_msg_id = message_senddm_v1(token_3, dm_id, msg_1)['message_id']
    
    with pytest.raises(InputError):    
        message_share_v1(token_2, og_msg_id, msg_2, invalid_channel_id, -1)      

def test_share_invalid_dm_id():
    clear_v1()
    session_id = create_session_id()
    
    msg_1 = ','
    msg_2 = ',,'
    
    user1 = auth_register_v1("AgentSmith@hotmail.com", "abcd1234", "Agent", "Smith")
    u_id_1 = user1['auth_user_id']
    token_1 = create_jwt(u_id_1, session_id)

    channel = channels_create_v1(u_id_1, 'comp1531', True)
    channel_id = channel["channel_id"]

    user2 = auth_register_v1("JohnSmith@hotmail.com", "abcd1234", "John", "Smith")
    u_id_2 = user2['auth_user_id']
    token_2 = create_jwt(u_id_2, session_id)
    channel_invite_v1(u_id_1, channel_id, u_id_2)

    og_msg_id = message_send_v1(token_1, channel_id, msg_1)['message_id']    

    user3 = auth_register_v1("AgentJohnson@hotmail.com", "abcd1234", "Agent", "Johnson")
    u_id_3 = user3['auth_user_id']
    u_ids = [u_id_2]
    dm_id = dm_create_v1(u_id_3,u_ids)['dm_id']
    invalid_dm_id = dm_id + 999
    
    with pytest.raises(InputError):    
        message_share_v1(token_2, og_msg_id, msg_2, -1, invalid_dm_id)
    
