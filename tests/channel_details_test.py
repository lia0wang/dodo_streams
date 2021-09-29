import pytest

from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.channel import channel_join_v1, channel_details_v1
from src.error import InputError
from src.error import AccessError
from src.other import clear_v1

def test_invalid_channel_id():
    clear_v1()
    u_id1 = auth_register_v1("11037.666@gmail.com", "armStrongCann0n", "Isaac", "Schneider")
    channel_id_1 = channels_create_v1(u_id1['auth_user_id'], 'passione', True)
    invalid_channel_id = channel_id_1['channel_id'] + 1
    with pytest.raises(InputError):
        channel_details_v1(u_id1['auth_user_id'], invalid_channel_id)   

def test_not_member():
    clear_v1()
    u_id1 = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    u_id2 = auth_register_v1("StandUser@gmail.com", "StandPower", "Generic", "name")
    u_id3 = auth_register_v1("11037.666@gmail.com", "armStrongCann0n", "Isaac", "Schneider")
    channel_id_1 = channels_create_v1(u_id1['auth_user_id'], 'passione', True)   
    channel_join_v1(u_id3['auth_user_id'], channel_id_1['channel_id'])
    with pytest.raises(AccessError):
        channel_details_v1(u_id2['auth_user_id'], channel_id_1['channel_id'])   
    
def test_valid_channel_id_and_member():
    clear_v1()
    u_id1 = auth_register_v1('wangliao@gmail.com', 'liaowang0207', 'wang', 'liao')
    channel_id_1 = channels_create_v1(u_id1['auth_user_id'], 'passione', True)  
    channel_details_v1(u_id1['auth_user_id'], channel_id_1['channel_id'])

def test_one_member_channel_details():
    clear_v1()
    u_id1 = auth_register_v1("11037.666@gmail.com", "armStrongCann0n", "Isaac", "Schneider")
    channel_id = channels_create_v1(u_id1['auth_user_id'], 'TheRealMonsters', True)

    # Checking details of the only member
    details = channel_details_v1(u_id1['auth_user_id'], channel_id['channel_id'])
    assert details['name'] == "TheRealMonsters"
    assert details['is_public'] == True

    assert details['owner_members'][0]['u_id'] == u_id1['auth_user_id']
    assert details['owner_members'][0]['email'] == "11037.666@gmail.com"
    assert details['owner_members'][0]['name_first'] == "Isaac"
    assert details['owner_members'][0]['name_last'] == "Schneider"
    assert details['owner_members'][0]['handle_str'] == "isaacschneider"

    assert details['all_members'][0]['u_id'] == u_id1['auth_user_id']
    assert details['all_members'][0]['email'] == "11037.666@gmail.com"
    assert details['all_members'][0]['name_first'] == "Isaac"
    assert details['all_members'][0]['name_last'] == "Schneider"
    assert details['all_members'][0]['handle_str'] == "isaacschneider" 

def test_multiple_members_channel_details():
    clear_v1()
    u_id1 = auth_register_v1("11037.666@gmail.com", "armStrongCann0n", "Isaac", "Schneider")
    u_id2 = auth_register_v1("StandUser@gmail.com", "StandPower", "Generic", "name")
    u_id3 = auth_register_v1('liaowang@gmail.com', 'liaowang0207', 'wang', 'liao')
    channel_id = channels_create_v1(u_id1['auth_user_id'], 'TheRealMonsters', True)
    channel_join_v1(u_id2['auth_user_id'], channel_id['channel_id'])
    channel_join_v1(u_id3['auth_user_id'], channel_id['channel_id'])

    details = channel_details_v1(u_id1['auth_user_id'], channel_id['channel_id'])

    assert details['name'] == "TheRealMonsters"
    assert details['is_public'] == True

    # Checking details of multiple members
    assert details['all_members'][0]['u_id'] == u_id1['auth_user_id']
    assert details['all_members'][0]['email'] == "11037.666@gmail.com"
    assert details['all_members'][0]['name_first'] == "Isaac"
    assert details['all_members'][0]['name_last'] == "Schneider"
    assert details['all_members'][0]['handle_str'] == "isaacschneider"    

    assert details['all_members'][1]['u_id'] == u_id2['auth_user_id']
    assert details['all_members'][1]['email'] == "StandUser@gmail.com"
    assert details['all_members'][1]['name_first'] == "Generic"
    assert details['all_members'][1]['name_last'] == "name"
    assert details['all_members'][1]['handle_str'] == "genericname"  

    assert details['all_members'][2]['u_id'] == u_id3['auth_user_id']
    assert details['all_members'][2]['email'] == "liaowang@gmail.com"
    assert details['all_members'][2]['name_first'] == "wang"
    assert details['all_members'][2]['name_last'] == "liao"
    assert details['all_members'][2]['handle_str'] == "wangliao"  


def test_multiple_channel_details_test():
    clear_v1()
    u_id1 = auth_register_v1('liaowang@gmail.com', 'liaowang0207', 'wang', 'liao')
    u_id2 = auth_register_v1("StandUser@gmail.com", "StandPower", "Generic", "name")
    u_id3 = auth_register_v1("11037.666@gmail.com", "armStrongCann0n", "Isaac", "Schneider")
    channel_id_1 = channels_create_v1(u_id1['auth_user_id'], 'Passione', False)   
    channel_id_2 = channels_create_v1(u_id2['auth_user_id'], 'Beauty Cuties', True)
    channel_join_v1(u_id3['auth_user_id'], channel_id_2['channel_id'])

    # Checking details for the first channel created, Passione.
    details_1 = channel_details_v1(u_id1['auth_user_id'], channel_id_1['channel_id'])

    assert details_1['name'] == "Passione"
    assert details_1['is_public'] == False

    assert details_1['owner_members'][0]['u_id'] == u_id1['auth_user_id']
    assert details_1['owner_members'][0]['email'] == "liaowang@gmail.com"
    assert details_1['owner_members'][0]['name_first'] == "wang"
    assert details_1['owner_members'][0]['name_last'] == "liao"
    assert details_1['owner_members'][0]['handle_str'] == "wangliao"  

    assert details_1['all_members'][0]['u_id'] == u_id1['auth_user_id']
    assert details_1['all_members'][0]['email'] == "liaowang@gmail.com"
    assert details_1['all_members'][0]['name_first'] == "wang"
    assert details_1['all_members'][0]['name_last'] == "liao"
    assert details_1['all_members'][0]['handle_str'] == "wangliao"  

    # Checking details for the second channel created, Beauty Cuties.
    details_2 = channel_details_v1(u_id2['auth_user_id'], channel_id_2['channel_id'])

    assert details_2['name'] == "Beauty Cuties"
    assert details_2['is_public'] == True

    assert details_2['owner_members'][0]['u_id'] == u_id2['auth_user_id']
    assert details_2['owner_members'][0]['email'] == "StandUser@gmail.com"
    assert details_2['owner_members'][0]['name_first'] == "Generic"
    assert details_2['owner_members'][0]['name_last'] == "name"
    assert details_2['owner_members'][0]['handle_str'] == "genericname" 

    assert details_2['all_members'][0]['u_id'] == u_id2['auth_user_id']
    assert details_2['all_members'][0]['email'] == "StandUser@gmail.com"
    assert details_2['all_members'][0]['name_first'] == "Generic"
    assert details_2['all_members'][0]['name_last'] == "name"
    assert details_2['all_members'][0]['handle_str'] == "genericname"  

    assert details_2['all_members'][1]['u_id'] == u_id3['auth_user_id']
    assert details_2['all_members'][1]['email'] == "11037.666@gmail.com"
    assert details_2['all_members'][1]['name_first'] == "Isaac"
    assert details_2['all_members'][1]['name_last'] == "Schneider"
    assert details_2['all_members'][1]['handle_str'] == "isaacschneider"    


    
