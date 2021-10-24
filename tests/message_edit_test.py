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
    invalid_msg_2 = ''
    user1 = auth_register_v1("AgentSmith@hotmail.com", "abcd1234", "Agent", "Smith")
    auth_id = user1['auth_user_id']
    token = create_jwt(auth_id, session_id)
    #check_valid_token(token)
    channel = channels_create_v1(auth_id, 'comp1531', True)
    channel_id = channel["channel_id"]
    msg_id = message_send_v1(token, channel_id, msg_1)['message_id']
    message_edit_v1(token, msg_id, invalid_msg_2)
    
    with pytest.raises(InputError):
        message_edit_v1(token, msg_id, invalid_msg_1)

