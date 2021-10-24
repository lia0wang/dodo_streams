import pytest
from src.other import clear_v1
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.message import message_send_v1
from src.helper import create_jwt, create_session_id, check_valid_token
from src.data_store import data_store
from src.error import InputError, AccessError

### Input Error

def test_msg__invalid_input_length():
    '''tests for invalid message length'''
    clear_v1()
    session_id = create_session_id()
    
    invalid_msg_1 = ',' * 1001
    invalid_msg_2 = ''
    user1 = auth_register_v1("AgentSmith@hotmail.com", "abcd1234", "Agent", "Smith")
    auth_id = user1['auth_user_id']
    token = create_jwt(auth_id, session_id)
    #check_valid_token(token)
    channel = channels_create_v1(auth_id, 'comp1531', True)
    channel_id = channel["channel_id"]
    
    with pytest.raises(InputError):
        message_send_v1(token, channel_id, invalid_msg_1)
    with pytest.raises(InputError):
        message_send_v1(token, channel_id, invalid_msg_2)

def test_msg_invalid_channel_id():
    '''tests for invalid message length'''
    clear_v1()
    session_id = create_session_id()
    
    msg = "Something"
    user1 = auth_register_v1("AgentSmith@hotmail.com", "abcd1234", "Agent", "Smith")
    auth_id = user1['auth_user_id']
    token = create_jwt(auth_id, session_id)
    
    channel = channels_create_v1(auth_id, 'comp1531', True)
    invalid_channel_id_1 = channel["channel_id"]+1799
    invalid_channel_id_2 = -1
    
    with pytest.raises(InputError):
        message_send_v1(token, invalid_channel_id_1, msg)
    with pytest.raises(InputError):
        message_send_v1(token, invalid_channel_id_2, msg)

### Access Error
def test_msg__invalid_auth_id():
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


    
