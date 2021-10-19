import pytest
from src.other import clear_v1
from src.error import InputError
from src.auth import auth_register_v1
from src.dm import dm_create_v1

def test_invalid_user_id():
    '''
    Test when the u id is invalid
    '''
    clear_v1()

    auth_user = auth_register_v1('shifan@gmail.com', 'chenshifan0207', 'shifan', 'chen')
    auth_user_id = auth_user['auth_user_id']

    user = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    invalid_user_id = user['auth_user_id'] + 1

    with pytest.raises(InputError):
        dm_create_v1(auth_user_id, invalid_user_id)
    with pytest.raises(InputError):
        dm_create_v1(auth_user_id, -1)
    with pytest.raises(InputError):
        dm_create_v1(auth_user_id, 0)
