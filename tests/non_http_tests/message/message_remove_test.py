import pytest
from src.other import clear_v1
from src.auth import auth_register_v1
from src.channel import channel_invite_v1, channel_addowner_v1, channel_join_v1
from src.channels import channels_create_v1, channels_list_v1
from src.message import message_send_v1, message_remove_v1, message_senddm_v1
from src.dm import dm_create_v1
from src.helper import create_jwt, create_session_id, check_valid_token
from src.error import InputError, AccessError
from src.data_store import data_store


def test_msg_cannot_remove_deleted_message():
    clear_v1()
    session_id = create_session_id()
    
    msg1 = "Something"
    msg2 = "dsds"
    user1 = auth_register_v1("AgentSmith@hotmail.com", "abcd1234", "Agent", "Smith")
    user2 = auth_register_v1("JohnSmith@hotmail.com", "abcd1234", "John", "Smith")

    auth_id = user1['auth_user_id']
    token1 = create_jwt(auth_id, session_id)

    u_id1 = user2['auth_user_id']
    token2 = create_jwt(u_id1, session_id)

    channel1 = channels_create_v1(auth_id, 'groupA', True)
    channel2 = channels_create_v1(u_id1, 'channelC', True)

    invalid_msg_id_1 = message_send_v1(token1, channel1['channel_id'], msg1)
    invalid_msg_id_2 = message_send_v1(token2, channel2['channel_id'], msg2)
    
    message_remove_v1(token1, invalid_msg_id_1['message_id'])
    

    with pytest.raises(InputError):
        message_remove_v1(token1, invalid_msg_id_1['message_id'])
        
    message_remove_v1(token2, invalid_msg_id_2['message_id'])

    with pytest.raises(InputError):
        message_remove_v1(token2, invalid_msg_id_2['message_id'])

def test_msg_remove_invalid_msg_id_1():
    clear_v1()
    session_id = create_session_id()
    
    msg1 = "Something"
    msg2 = "dsds"
    user1 = auth_register_v1("AgentSmith@hotmail.com", "abcd1234", "Agent", "Smith")
    user2 = auth_register_v1("JohnSmith@hotmail.com", "abcd1234", "John", "Smith")

    auth_id = user1['auth_user_id']
    token1 = create_jwt(auth_id, session_id)

    u_id1 = user2['auth_user_id']
    token2 = create_jwt(u_id1, session_id)

    channel1 = channels_create_v1(auth_id, 'groupA', True)
    channel2 = channels_create_v1(u_id1, 'channelC', True)

    invalid_msg_id_1 = message_send_v1(token1, channel1['channel_id'], msg1)
    invalid_msg_id_2 = message_send_v1(token2, channel2['channel_id'], msg2)

    #permission id = 1, # should succeed 
    message_remove_v1(token1, invalid_msg_id_2['message_id'])
    
    with pytest.raises(AccessError):
        message_remove_v1(token2, invalid_msg_id_1['message_id'])
         
def test_msg_remove_invalid_msg_id_2():
    clear_v1()
    session_id = create_session_id()
    
    msg1 = "Something"
    user1 = auth_register_v1("AgentSmith@hotmail.com", "abcd1234", "Agent", "Smith")

    auth_id = user1['auth_user_id']
    token1 = create_jwt(auth_id, session_id)

    channel1 = channels_create_v1(auth_id, 'groupA', True)

    invalid_msg_id_1 = message_send_v1(token1, channel1['channel_id'], msg1)
    invalid_msg_id_1['message_id']+=999
    
    with pytest.raises(InputError):
        message_remove_v1(token1, invalid_msg_id_1['message_id'])

def test_global_owner_can_remove_members_message_channel():
    clear_v1()
    session_id = create_session_id()
    
    msg_1 = 'test' 

    user1 = auth_register_v1("AgentSmith@hotmail.com", "abcd1234", "Agent", "Smith")
    auth_id = user1['auth_user_id']
    #permission_id = 1
    token_1 = create_jwt(auth_id, session_id)
    channel = channels_create_v1(auth_id, 'comp1531', True)
    channel_id = channel["channel_id"]
    
    user2 = auth_register_v1("JohnSmith@hotmail.com", "abcd1234", "John", "Smith")
    u_id = user2['auth_user_id']
    token_2 = create_jwt(u_id, session_id)
    channel_invite_v1(auth_id, channel_id, u_id)
    
    msg_id = message_send_v1(token_2, channel_id, msg_1)['message_id']
    
    message_remove_v1(token_1, msg_id)

def test_owner_can_remove_members_message_channel():
    clear_v1()
    session_id = create_session_id()
    
    msg_1 = ',' 

    user1 = auth_register_v1("AgentSmith@hotmail.com", "abcd1234", "Agent", "Smith")
    u_id_1 = user1['auth_user_id'] #permission_id = 1
  
    user2 = auth_register_v1("JohnSmith@hotmail.com", "abcd1234", "John", "Smith")
    u_id_2 = user2['auth_user_id']
    token_2 = create_jwt(u_id_2, session_id)

    user3 = auth_register_v1("AgentJohnson@hotmail.com", "abcd1234", "Agent", "Johnson")
    u_id_3 = user3['auth_user_id']
    token_3 = create_jwt(u_id_3, session_id)
    
    channel = channels_create_v1(u_id_1, 'comp1531', True)
    channel_id = channel["channel_id"]
    channel_join_v1(u_id_2, channel_id)
    channel_join_v1(u_id_3, channel_id)
    channel_addowner_v1(u_id_1, channel_id, u_id_2)
    
    msg_id = message_send_v1(token_3, channel_id, msg_1)['message_id']
    
    message_remove_v1(token_2, msg_id)

def test_original_poster_can_remove_message_channel():
    clear_v1()
    session_id = create_session_id()
    
    msg_1 = '!,'
    
    user1 = auth_register_v1("AgentSmith@hotmail.com", "abcd1234", "Agent", "Smith")
    u_id_1 = user1['auth_user_id']
    channel = channels_create_v1(u_id_1, 'comp1531', True)
    channel_id = channel["channel_id"]

    user2 = auth_register_v1("JohnSmith@hotmail.com", "abcd1234", "John", "Smith")
    u_id_2 = user2['auth_user_id']
    token_2 = create_jwt(u_id_2, session_id)
    channel_invite_v1(u_id_1, channel_id, u_id_2)

    
    msg_id = message_send_v1(token_2, channel_id, msg_1)['message_id']
    message_remove_v1(token_2, msg_id)

def test_nonowner_nonposter_cant_remove():
    clear_v1()
    session_id = create_session_id()
    
    msg_1 = ',' 

    user1 = auth_register_v1("AgentSmith@hotmail.com", "abcd1234", "Agent", "Smith")
    u_id_1 = user1['auth_user_id']
    token_1 = create_jwt(u_id_1, session_id)
    channel = channels_create_v1(u_id_1, 'comp1531', True)
    channel_id = channel["channel_id"]
    
    user2 = auth_register_v1("JohnSmith@hotmail.com", "abcd1234", "John", "Smith")
    u_id_2 = user2['auth_user_id']
    
    channel_invite_v1(u_id_1, channel_id, u_id_2)
    channel_addowner_v1(u_id_1, channel_id, u_id_2)

    user3 = auth_register_v1("AgentJohnson@hotmail.com", "abcd1234", "Agent", "Johnson")
    u_id_3 = user3['auth_user_id']
    token_3 = create_jwt(u_id_3, session_id)
    channel_invite_v1(u_id_1, channel_id, u_id_3)
    
    msg_id = message_send_v1(token_1, channel_id, msg_1)['message_id']
    
    with pytest.raises(AccessError):
        message_remove_v1(token_3, msg_id)
        
def test_original_poster_can_remove_message_dm():
    clear_v1()
    session_id = create_session_id()

    msg_1 = "Something"
    
    user1 = auth_register_v1("AgentSmith@hotmail.com", "abcd1234", "Agent", "Smith")
    user2 = auth_register_v1("JohnSmith@hotmail.com", "abcd1234", "John", "Smith")
    user3 = auth_register_v1("AgentJohnson@hotmail.com", "abcd1234", "Agent", "Johnson")
    
    u_id1 = user1['auth_user_id']      
    u_id2 = user2['auth_user_id']
    u_id3 = user3['auth_user_id']

    token = create_jwt(u_id3, session_id)
    u_ids = [u_id1,u_id2]
    dm_id = dm_create_v1(u_id3,u_ids)['dm_id']
    msg_id = message_senddm_v1(token, dm_id, msg_1)['message_id']
    message_remove_v1(token, msg_id)

def test_global_owner_cant_remove_members_message_dm():
    clear_v1()
    session_id = create_session_id()

    msg_1 = "Something"
    
    user1 = auth_register_v1("AgentSmith@hotmail.com", "abcd1234", "Agent", "Smith")
    #permission_id = 1
    user2 = auth_register_v1("JohnSmith@hotmail.com", "abcd1234", "John", "Smith")
    user3 = auth_register_v1("AgentJohnson@hotmail.com", "abcd1234", "Agent", "Johnson")
    
    u_id1 = user1['auth_user_id']      
    u_id2 = user2['auth_user_id']
    u_id3 = user3['auth_user_id']

    token_1 = create_jwt(u_id3, session_id)
    token_2 = create_jwt(u_id1, session_id)
    u_ids = [u_id1,u_id2]
    dm_id = dm_create_v1(u_id3,u_ids)['dm_id']
    msg_id = message_senddm_v1(token_1, dm_id, msg_1)['message_id']
    with pytest.raises(AccessError):
        message_remove_v1(token_2, msg_id)    

def test_owner_can_remove_members_message_dm():
    clear_v1()
    session_id = create_session_id()

    msg_1 = "Something"
    
    user1 = auth_register_v1("AgentSmith@hotmail.com", "abcd1234", "Agent", "Smith")
    #permission_id = 1
    user2 = auth_register_v1("JohnSmith@hotmail.com", "abcd1234", "John", "Smith")
    user3 = auth_register_v1("AgentJohnson@hotmail.com", "abcd1234", "Agent", "Johnson")
    
    u_id1 = user1['auth_user_id']      
    u_id2 = user2['auth_user_id']
    u_id3 = user3['auth_user_id']

    token_1 = create_jwt(u_id3, session_id)
    token_2 = create_jwt(u_id2, session_id)
    u_ids = [u_id1,u_id2]
    dm_id = dm_create_v1(u_id3,u_ids)['dm_id'] #Owner is user3
    msg_id = message_senddm_v1(token_2, dm_id, msg_1)['message_id']
    
    message_remove_v1(token_1, msg_id) 
