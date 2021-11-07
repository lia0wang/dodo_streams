
import pytest
from src.other import clear_v1
from src.auth import auth_register_v1
from src.channel import channel_invite_v1, channel_addowner_v1
from src.channels import channels_create_v1
from src.message import message_send_v1, message_edit_v1, message_remove_v1, message_senddm_v1
from src.dm import dm_create_v1
from src.helper import create_jwt, create_session_id, check_valid_token
from src.data_store import data_store
from src.error import InputError, AccessError


def test_msg_edit_invalid_input_length():
    clear_v1()
    session_id = create_session_id()
    
    msg_1 = ','
    invalid_msg_1 = ','* 1001
    
    user1 = auth_register_v1("AgentSmith@hotmail.com", "abcd1234", "Agent", "Smith")
    auth_id = user1['auth_user_id']
    token = create_jwt(auth_id, session_id)
    channel = channels_create_v1(auth_id, 'comp1531', True)
    channel_id = channel["channel_id"]
    msg_id = message_send_v1(token, channel_id, msg_1)['message_id']
    with pytest.raises(InputError):
        message_edit_v1(token, msg_id, invalid_msg_1)

def test_global_owner_can_edit_members_message_channel():
    clear_v1()
    session_id = create_session_id()
    
    msg_1 = ',' 
    msg_2 = 'Something'
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
    
    message_edit_v1(token_1, msg_id, msg_2)

def test_owner_can_edit_members_message_channel():
    clear_v1()
    session_id = create_session_id()
    
    msg_1 = ',' 
    msg_2 = 'Something'

    user1 = auth_register_v1("AgentSmith@hotmail.com", "abcd1234", "Agent", "Smith")
    u_id_1 = user1['auth_user_id']
    #permission_id = 1
    channel = channels_create_v1(u_id_1, 'comp1531', True)
    channel_id = channel["channel_id"]
    
    user2 = auth_register_v1("JohnSmith@hotmail.com", "abcd1234", "John", "Smith")
    u_id_2 = user2['auth_user_id']
    token_2 = create_jwt(u_id_2, session_id)
    channel_invite_v1(u_id_1, channel_id, u_id_2)
    channel_addowner_v1(u_id_1, channel_id, u_id_2)

    user3 = auth_register_v1("AgentJohnson@hotmail.com", "abcd1234", "Agent", "Johnson")
    u_id_3 = user3['auth_user_id']
    token_3 = create_jwt(u_id_3, session_id)
    channel_invite_v1(u_id_1, channel_id, u_id_3)
    # message was sent by a non-owner user
    msg_id = message_send_v1(token_3, channel_id, msg_1)['message_id']
    
    message_edit_v1(token_2, msg_id, msg_2)


def test_original_poster_can_edit_message_channel():
    clear_v1()
    session_id = create_session_id()
    
    msg_1 = '!,'
    msg_2 = 'Something'
    
    user1 = auth_register_v1("AgentSmith@hotmail.com", "abcd1234", "Agent", "Smith")
    u_id_1 = user1['auth_user_id']
    channel = channels_create_v1(u_id_1, 'comp1531', True)
    channel_id = channel["channel_id"]

    user2 = auth_register_v1("JohnSmith@hotmail.com", "abcd1234", "John", "Smith")
    u_id_2 = user2['auth_user_id']
    token_2 = create_jwt(u_id_2, session_id)
    channel_invite_v1(u_id_1, channel_id, u_id_2)

    
    msg_id = message_send_v1(token_2, channel_id, msg_1)['message_id']
    message_edit_v1(token_2, msg_id, msg_2)

def test_nonowner_nonposter_cant_edit():
    clear_v1()
    session_id = create_session_id()
    
    msg_1 = ',' 
    msg_2 = 'Something'
    msg_3 = 'Something Something'
    user1 = auth_register_v1("AgentSmith@hotmail.com", "abcd1234", "Agent", "Smith")
    u_id_1 = user1['auth_user_id']
    token_1 = create_jwt(u_id_1, session_id)
    channel = channels_create_v1(u_id_1, 'comp1531', True)
    channel_id = channel["channel_id"]
    
    user2 = auth_register_v1("JohnSmith@hotmail.com", "abcd1234", "John", "Smith")
    u_id_2 = user2['auth_user_id']
    token_2 = create_jwt(u_id_2, session_id)
    channel_invite_v1(u_id_1, channel_id, u_id_2)
    channel_addowner_v1(u_id_1, channel_id, u_id_2)

    user3 = auth_register_v1("AgentJohnson@hotmail.com", "abcd1234", "Agent", "Johnson")
    u_id_3 = user3['auth_user_id']
    token_3 = create_jwt(u_id_3, session_id)
    channel_invite_v1(u_id_1, channel_id, u_id_3)
    
    msg_id = message_send_v1(token_1, channel_id, msg_1)['message_id']
    
    message_edit_v1(token_2, msg_id, msg_2)
    with pytest.raises(AccessError):
        message_edit_v1(token_3, msg_id, msg_3)
        
def test_cannot_edit_deleted_message():
    clear_v1()
    session_id = create_session_id()
    
    msg_1 = ','
    msg_2 = ''
    msg_3 = 'Something'
    
    user1 = auth_register_v1("AgentSmith@hotmail.com", "abcd1234", "Agent", "Smith")
    auth_id = user1['auth_user_id']
    token = create_jwt(auth_id, session_id)
    channel = channels_create_v1(auth_id, 'comp1531', True)
    channel_id = channel["channel_id"]
    msg_id = message_send_v1(token, channel_id, msg_1)['message_id']
    message_edit_v1(token, msg_id, msg_2) #redirect to message/remove/v1
    with pytest.raises(InputError):
        message_edit_v1(token, msg_id, msg_3)

def test_original_poster_can_edit_message_dm():
    clear_v1()
    session_id = create_session_id()

    msg_1 = "Something"
    msg_2 = "Edit"
    
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
    message_edit_v1(token, msg_id, msg_2)

def test_global_owner_cant_edit_members_message_dm():
    clear_v1()
    session_id = create_session_id()

    msg_1 = "Something"
    msg_2 = "Edit"
    
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
    dm_id = dm_create_v1(u_id3,u_ids)['dm_id'] #Owner: user3
    msg_id = message_senddm_v1(token_1, dm_id, msg_1)['message_id']
    with pytest.raises(AccessError):
        message_edit_v1(token_2, msg_id,msg_2)  

def test_owner_can_edit_members_message_dm():
    clear_v1()
    session_id = create_session_id()

    msg_1 = "Something"
    msg_2 = "Edit"
    
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
    dm_id = dm_create_v1(u_id3,u_ids)['dm_id'] #Owner: user3
    msg_id = message_senddm_v1(token_2, dm_id, msg_1)['message_id']
    
    message_edit_v1(token_1, msg_id,msg_2)  

