import pytest
from src.other import clear_v1
from src.error import AccessError, InputError
from src.auth import auth_register_v1
from src.dm import dm_create_v1

def test_invalid_user_id():
    '''
    Test when the u id is invalid
    '''
    clear_v1()

    auth_user = auth_register_v1('shifan@gmail.com', 'chenshifan0207', 'shifan', 'chen')
    auth_user_id = auth_user['auth_user_id']

    user_1 = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    invalid_user_id = user_1['auth_user_id'] + 10

    user_2 = auth_register_v1('haha@gmail.com', 'haha0207', 'ha', 'ha')
    valid_user_id = user_2['auth_user_id']

    with pytest.raises(InputError):
        dm_create_v1(auth_user_id, [invalid_user_id])
    with pytest.raises(InputError):
        dm_create_v1(auth_user_id, [-1])
    with pytest.raises(InputError):
        dm_create_v1(auth_user_id, [invalid_user_id, valid_user_id])

def test_invalid_auth_user_id():
    '''
    Test when the auth user id is invalid
    '''
    clear_v1()

    auth_user = auth_register_v1('shifan@gmail.com', 'chenshifan0207', 'shifan', 'chen')
    invalid_auth_user_id = auth_user['auth_user_id'] + 10

    user_1 = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    user_id = user_1['auth_user_id']


    with pytest.raises(InputError):
        dm_create_v1(invalid_auth_user_id, [user_id])

def test_dm_create_basic():
    '''
    Test if dm/create/v1 working properly
    '''
    clear_v1()

    auth_user = auth_register_v1('shifan@gmail.com', 'chenshifan0207', 'shifan', 'chen')
    auth_user_id = auth_user['auth_user_id']

    user_1 = auth_register_v1('wangliao@gmail.com', 'haha123', 'wang', 'liao')
    user_id_1 = user_1['auth_user_id']

    user_2 = auth_register_v1('wangliao1@gmail.com', 'hehe321', 'wang', 'liao')
    user_id_2 = user_2['auth_user_id']

    user_3 = auth_register_v1('wangliao2@gmail.com', 'xixi123', 'wang', 'liao')
    user_id_3 = user_3['auth_user_id']

    u_ids = [user_id_1, user_id_2, user_id_3]

    assert dm_create_v1(auth_user_id, u_ids) == {'dm_id': 1, 'dm_name': 'shifanchen, wangliao, wangliao0, wangliao1'}

def test_dm_create_only_creator():
    '''
    Test when create dm with an user and itself
    '''
    clear_v1()

    auth_user = auth_register_v1('shifan@gmail.com', 'chenshifan0207', 'shifan', 'chen')
    auth_user_id = auth_user['auth_user_id']

    with pytest.raises(AccessError):
        dm_create_v1(auth_user_id, [auth_user_id])
