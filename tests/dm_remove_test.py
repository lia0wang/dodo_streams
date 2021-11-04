import pytest
from src.other import clear_v1
from src.error import AccessError, InputError
from src.auth import auth_register_v1
from src.message import message_senddm_v1
from src.dm import dm_create_v1, dm_remove_v1
from src.helper import create_jwt, create_session_id

def test_successful_dm_removal():
    clear_v1()
    session_id = create_session_id()

    user_1 = auth_register_v1('JohnSmith@gmail.com', 'abcd1234', 'John', 'Smith')
    u_id_1 = user_1['auth_user_id']

    user_2 = auth_register_v1('AgentSmith@gmail.com', 'abcd1234', 'Agent', 'Smith')
    u_id_2 = user_2['auth_user_id']

    user_3 = auth_register_v1('AgentJohnson@gmail.com', 'abcd1234', 'Agent', 'Johnson')
    u_id_3 = user_3['auth_user_id']

    u_ids = [u_id_1,u_id_2]

    dm_id = dm_create_v1(u_id_3, u_ids)['dm_id']
    
    msg = "test"
    token = create_jwt(u_id_3, session_id)
    message_senddm_v1(token, dm_id, msg)

    dm_remove_v1(token,dm_id)

def test_nonowner_cannot_remove_dm():
    clear_v1()
    session_id = create_session_id()

    user_1 = auth_register_v1('JohnSmith@gmail.com', 'abcd1234', 'John', 'Smith')
    u_id_1 = user_1['auth_user_id']

    user_2 = auth_register_v1('AgentSmith@gmail.com', 'abcd1234', 'Agent', 'Smith')
    u_id_2 = user_2['auth_user_id']

    user_3 = auth_register_v1('AgentJohnson@gmail.com', 'abcd1234', 'Agent', 'Johnson')
    u_id_3 = user_3['auth_user_id']

    u_ids = [u_id_1,u_id_2]
    dm_id = dm_create_v1(u_id_3, u_ids)['dm_id'] #Owner is user 3
    
    token_2 = create_jwt(u_id_2, session_id)

    with pytest.raises(AccessError):
        dm_remove_v1(token_2,dm_id)

def test_dm_remove_invalid_dm_id():
    clear_v1()
    session_id = create_session_id()

    user_1 = auth_register_v1('JohnSmith@gmail.com', 'abcd1234', 'John', 'Smith')
    u_id_1 = user_1['auth_user_id']

    user_2 = auth_register_v1('AgentSmith@gmail.com', 'abcd1234', 'Agent', 'Smith')
    u_id_2 = user_2['auth_user_id']

    user_3 = auth_register_v1('AgentJohnson@gmail.com', 'abcd1234', 'Agent', 'Johnson')
    u_id_3 = user_3['auth_user_id']

    u_ids = [u_id_1,u_id_2]
    dm_create_v1(u_id_3, u_ids)['dm_id'] #Owner is user 3
    
    token_1 = create_jwt(u_id_3, session_id)

    with pytest.raises(InputError):
        dm_remove_v1(token_1,-1)    

def test_dm_remove_invalid_token():
    clear_v1()
    session_id = create_session_id()

    user_1 = auth_register_v1('JohnSmith@gmail.com', 'abcd1234', 'John', 'Smith')
    u_id_1 = user_1['auth_user_id']

    user_2 = auth_register_v1('AgentSmith@gmail.com', 'abcd1234', 'Agent', 'Smith')
    u_id_2 = user_2['auth_user_id']

    user_3 = auth_register_v1('AgentJohnson@gmail.com', 'abcd1234', 'Agent', 'Johnson')
    u_id_3 = user_3['auth_user_id']

    u_ids = [u_id_1,u_id_2]
    dm_id = dm_create_v1(u_id_3, u_ids)['dm_id'] #Owner is user 3
    
    msg = "test"
    token_1 = create_jwt(u_id_3, session_id)
    token_2 = create_jwt(u_id_2, session_id)
    message_senddm_v1(token_1, dm_id, msg)
    with pytest.raises(AccessError):
        dm_remove_v1(token_2,dm_id)     
