import pytest
from src.other import clear_v1
from src.auth import auth_register_v1
from src.channels import channels_create_v1, channels_list_v1
from src.message import message_send_v1,message_remove_v1,message_edit_v1
from src.helper import create_jwt, create_session_id, check_valid_token
from src.error import InputError, AccessError
from src.data_store import data_store
### Input Error


def test_msg_ed_too_long():
    '''tests for invalid message length'''
    clear_v1()
    session_id = create_session_id()
    
    msg1 = ","
    msg2 = "," * 1001
    user1 = auth_register_v1("AgentSmith@hotmail.com", "abcd1234", "Agent", "Smith")
    user2 = auth_register_v1("JohnSmith@hotmail.com", "abcd1234", "John", "Smith")

    auth_id = user1['auth_user_id']
    token1 = create_jwt(auth_id, session_id)
    channel1 = channels_create_v1(auth_id, 'groupA', True)
    msg_id_1 = message_send_v1(token1, channel1['channel_id'], msg1)
    
    with pytest.raises(InputError):
        message_edit_v1(token1, msg_id_1, msg2)
    


### Access Error
def test_msg_ed_unauthed():
    pass
        

