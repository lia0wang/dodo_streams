import pytest
from src.other import clear_v1
from src.auth import auth_register_v1
from src.channel import channel_messages_v1
from src.channels import channels_create_v1, channels_list_v1
from src.message import message_send_v1,message_remove_v1
from src.helper import create_jwt, create_session_id, check_valid_token
from src.error import InputError, AccessError
from src.data_store import data_store
### Input Error


def test_msg_rm_repeated():
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
    invalid_msg_id_2 = message_send_v1(token2, channel2['channel_id'], msg2)
    
    with pytest.raises(InputError):
        message_remove_v1(token2, invalid_msg_id_1['message_id'])
    
    with pytest.raises(InputError):
        message_remove_v1(token1, invalid_msg_id_2['message_id'])
        
def test_msg_rm_invalid_msg_id_2():
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

        
### Access Error
def test_msg_rm_unauthed():
    pass
        

