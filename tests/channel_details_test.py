import pytest

from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.channel import channel_join_v1, channel_details_v1
from src.error import InputError
from src.error import AccessError
from src.other import clear_v1

def test_invalid_channel_id():
    clear_v1()
    u_id1 = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    u_id2 = auth_register_v1('liaowang@gmail.com', 'liaowang0207', 'wang', 'liao')
    channel_id_1 = channels_create_v1(u_id1, 'passione', True)
    channel_id_2 = channel_id_1['channel_id'] + 1
    with pytest.raises(InputError):
        channel_details_v1(u_id1, channel_id_2)   

def test_not_member():
    clear_v1()
    u_id1 = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    u_id2 = auth_register_v1('liaowang@gmail.com', 'liaowang0207', 'wang', 'liao')
    channel_id_1 = channels_create_v1(u_id1, 'passione', True)   
    channel_id_2 = channels_create_v1(u_id2, 'league', False)
    with pytest.raises(AccessError):
        channel_details_v1(u_id1['auth_user_id'], channel_id_2['channel_id'])   
    
def test_valid_channel_id_and_member():
    clear_v1()
    u_id1 = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    channel_id_1 = channels_create_v1(u_id1, 'passione', True)  
    channel_details_v1(u_id1['auth_user_id'], channel_id_1)  

def test_return_details():
    clear_v1()
    u_id1 = auth_register_v1("11037.666@gmail.com", "armStrongCann0n", "Isaac", "Schneider")
    u_id2 = auth_register_v1("StandUser@gmail.com", "StandPower", "Generic", "name")
    u_id3 = auth_register_v1('liaowang@gmail.com', 'liaowang0207', 'wang', 'liao')
    channel_id = channels_create_v1(u_id1['auth_user_id'], 'TheRealMonsters', True)
    channel_join_v1(u_id2['auth_user_id'], channel_id)
    channel_join_v1(u_id3['auth_user_id'], channel_id)

    details = channel_details_v1(u_id1['auth_user_id'], channel_id)
    assert details['name'] == "TheRealMonsters"
    assert details['is_public'] == True
    assert details['owner_members'] == [
        {
            'u_id': u_id1['auth_user_id'],
            'email': "11037.666@gmail.com",
            'name_first': 'Isaac',
            'name_last': 'Schneider',
            'handle_str': 'isaacschneider'
        }
    ]
    assert details['all_members'] == [
        {
            'u_id': u_id1['auth_user_id'],
            'email': "11037.666@gmail.com",
            'name_first': 'Isaac',
            'name_last': 'Schneider',
            'handle_str': 'isaacschneider'
        },
        {
            'u_id': u_id2['auth_user_id'],
            'email': "StandUser@gmail.com",
            'name_first': 'Generic',
            'name_last': 'name',
            'handle_str': 'genericname'            
        },
        {
            'u_id': u_id3['auth_user_id'],
            'email': "liaowang@gmail.com",
            'name_first': 'wang',
            'name_last': 'liao',
            'handle_str': 'wangliao'     
        }
    ]


