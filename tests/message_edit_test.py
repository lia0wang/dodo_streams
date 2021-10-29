import pytest
from src.other import clear_v1
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.message import message_send_v1, message_edit_v1, message_remove_v1
from src.helper import create_jwt, create_session_id, check_valid_token
from src.data_store import data_store
from src.error import InputError, AccessError


### Input Error

def test_msg_ed_invalid_input_length():
    '''tests for invalid message length'''
    clear_v1()
    session_id = create_session_id()
    
    msg_1 = ',' 
    invalid_msg_1 = ','* 1001
    user1 = auth_register_v1("AgentSmith@hotmail.com", "abcd1234", "Agent", "Smith")
    auth_id = user1['auth_user_id']
    token = create_jwt(auth_id, session_id)
    #check_valid_token(token)
    channel = channels_create_v1(auth_id, 'comp1531', True)
    channel_id = channel["channel_id"]
    msg_id = message_send_v1(token, channel_id, msg_1)['message_id']
    
    with pytest.raises(InputError):
        message_edit_v1(token, msg_id, invalid_msg_1)

def test_msg_ed_empty_input_length():
    '''tests for invalid message length'''
    clear_v1()
    session_id = create_session_id()
    
    msg_1 = ',' 
    empty_msg_1 = ''
    user1 = auth_register_v1("AgentSmith@hotmail.com", "abcd1234", "Agent", "Smith")
    auth_id = user1['auth_user_id']
    token = create_jwt(auth_id, session_id)
    #check_valid_token(token)
    channel = channels_create_v1(auth_id, 'comp1531', True)
    channel_id = channel["channel_id"]
    msg_id = message_send_v1(token, channel_id, msg_1)['message_id'] 
    message_edit_v1(token, msg_id, empty_msg_1)


def test_cannot_edit_deleted_message():
    clear_v1()
    session_id = create_session_id()
    
    msg_1 = ',' 
    empty_msg_1 = ''
    msg_2 = '***'
    user1 = auth_register_v1("AgentSmith@hotmail.com", "abcd1234", "Agent", "Smith")
    auth_id = user1['auth_user_id']
    token = create_jwt(auth_id, session_id)
    #check_valid_token(token)
    channel = channels_create_v1(auth_id, 'comp1531', True)
    channel_id = channel["channel_id"]
    msg_id = message_send_v1(token, channel_id, msg_1)['message_id'] 
    message_edit_v1(token, msg_id, empty_msg_1)

    with pytest.raises(InputError):
        message_edit_v1(token, msg_id, msg_2)

def test_msg_rm_invalid_msg_id_1():
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
    invalid_msg_id_2 = message_send_v1(token2, channel2['channel_id'], msg1)
    
    with pytest.raises(AccessError):
        message_edit_v1(token2, invalid_msg_id_1['message_id'],msg2)
    
    with pytest.raises(AccessError):
        message_edit_v1(token1, invalid_msg_id_2['message_id'],msg2)  
