import pytest
from src.other import clear_v1
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.message import message_send_v1,message_senddm_v1
from src.dm import dm_create_v1
from src.helper import create_jwt, create_session_id
from src.error import InputError, AccessError

### Input Error

def invalid_length():
    '''tests for invalid message length'''
    clear_v1()
    session_id = create_session_id()
    
    invalid_msg_1 = ',' * 1001
    invalid_msg_2 = ''
    user1 = auth_register_v1("AgentSmith@hotmail.com", "abcd1234", "Agent", "Smith")
    auth_id = user1['auth_user_id']
    token = create_jwt(auth_id, session_id)
    
    channel = channels_create_v1(auth_id, 'comp1531', True)
    channel_id = channel["channel_id"]
    
    with pytest.raises(InputError):
        message_send_v1(token, channel_id, invalid_msg_1)
    with pytest.raises(InputError):
        message_send_v1(token, channel_id, invalid_msg_2)

def invalid_length_dm():
    '''tests for invalid message length'''
    clear_v1()
    session_id = create_session_id()
    
    invalid_msg_1 = ',' * 1001
    invalid_msg_2 = ''
    
    user1 = auth_register_v1("AgentSmith@hotmail.com", "abcd1234", "Agent", "Smith")
    user2 = auth_register_v1("JohnSmith@hotmail.com", "abcd1234", "John", "Smith")
    user3 = auth_register_v1("AgentJohnson@hotmail.com", "abcd1234", "Agent", "Johnson")
    
    auth_id = user1['auth_user_id']
    token = create_jwt(auth_id, session_id)
        
    u_id1 = user2['auth_user_id']
    u_id2 = user3['auth_user_id']
    u_ids = [u_id1,u_id2]
    dm_id = dm_create_v1(auth_id,u_ids)
    
    with pytest.raises(InputError):
        message_senddm_v1(token, dm_id, invalid_msg_1)
    with pytest.raises(InputError):
        message_senddm_v1(token, dm_id, invalid_msg_2)


### Access Error
def invalid_auth_id():
    clear_v1()
    session_id = create_session_id()
    user1 = auth_register_v1("AgentSmith@hotmail.com", "abcd1234", "Agent", "Smith")
    user2 = auth_register_v1("JohnSmith@hotmail.com", "abcd1234", "John", "Smith")
    
    auth_id = user1['auth_user_id']
    channel = channels_create_v1(auth_id, 'comp1531', True)
    channel_id = channel["channel_id"]

    u_id = user2['auth_user_id']
    invalid_token = create_jwt(u_id, session_id)
    
    msg = "Something"
    
    with pytest.raises(AccessError):
        message_send_v1(invalid_token, channel_id, msg)

def invalid_auth_id_dm():
    user1 = auth_register_v1("AgentSmith@hotmail.com", "abcd1234", "Agent", "Smith")
    user2 = auth_register_v1("JohnSmith@hotmail.com", "abcd1234", "John", "Smith")
    user3 = auth_register_v1("AgentJohnson@hotmail.com", "abcd1234", "Agent", "Johnson")
    user4 = auth_register_v1("AgentBrown@hotmail.com", "abcd1234", "Agent", "Brown")
    
    auth_id = user1['auth_user_id']
    u_id1 = user2['auth_user_id']
    u_id2 = user3['auth_user_id']
    u_id3 = user4['auth_user_id']

    invalid_token = create_jwt(auth_id, session_id)
    u_ids = [u_id1,u_id2]
    dm_id = dm_create_v1(u_id3,u_ids)
    
    msg = "Something"
    with pytest.raises(AccessError):
        message_senddm_v1(invalid_token, dm_id, msg)
    
