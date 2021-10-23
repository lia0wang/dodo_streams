import re
import os
from src.dm import dm_create_v1
from src.helper import get_data,is_database_exist, check_valid_token, \
    decode_jwt,save_database_updates, datetime_to_unix_time_stamp
from src.data_store import data_store
from src.error import InputError, AccessError

def message_send_v1(token, channel_id, message):
    # Fetch data
    is_member = False
    valid_channel = False
    if(len(message)<1 or len(message)>1000):
        raise InputError("Error: message too long or too short")
    db_store = data_store.get()
    if is_database_exist() == True:
        db_store = get_data()
        
    #if check_valid_token(token) == True:
        #get authorised user id 
    u_id = decode_jwt(token)['u_id']
            
        #Check channel_id is valid
        #Also check if the authorised user is not a member of the channel

    for chan in db_store['channels']:
        if chan['channel_id'] == channel_id:
            target_channel = chan
            valid_channel = True
        for user in chan["all_members"]:
            if user['u_id'] == u_id:
                is_member = True # Check if authorised user is a member of the channel
                break
                
    if valid_channel == False:
        raise InputError("channel_id does not refer to a valid channel")
   
    if is_member == False:
        raise AccessError("Authorised user is not a member of the channel")
   
    #seek_target_channel_and_errors(db_store, u_id, channel_id)
    message_id = db_store['message_index']
    db_store['message_index']+=1
    if is_database_exist:
        save_database_updates(db_store)
    else:
        data_store.set(db_store)
    
    # creates the unix time_stamp
    timestamp = datetime_to_unix_time_stamp()

    message = {
        'message_id': message_id,
        'u_id': u_id,
        'message': message,
        'time_created': timestamp
    }

    target_channel['messages'].append(message)
    save_database_updates(db_store)

    return {
        'message_id': message_id,
        'time_created': timestamp
    }
            
    
def message_senddm_v1(token, dm_id, message):
    # Fetch data
    is_member = False
    if(len(message)<1 or len(message)>1000):
        raise InputError("Error: message too long or too short")
    db_store = data_store.get()
    if is_database_exist() == True:
        db_store = get_data()
    #Get authorised user id 
    u_id = decode_jwt(token)['u_id']

    #Check if dm_id is not valid
    valid = False
    for dm in db_store['dms']:
        if dm['dm_id'] == dm_id:
            target_dm = dm
            valid = True
        if not valid:
            raise InputError(description="dm_id does not refer to a valid dm id")

    for dm in db_store['dms']:
        if dm['auth_user_id'] == u_id:
            is_member = True# Check if authorised user is a member of the channel
            break
   
    if is_member == False:
        raise AccessError("Authorised user is not a member of DM")
   
    #seek_target_channel_and_errors(db_store, u_id, channel_id)
    message_id = db_store['message_index']
    db_store['message_index']+=1

    # creates the unix time_stamp
    timestamp = datetime_to_unix_time_stamp()
    
    dm_message = {
        'message_id': message_id,
        'u_id': u_id,
        'message': message,
        'time_created': timestamp
    }

    target_dm['messages'].append(dm_message)
    save_database_updates(db_store)


    if is_database_exist:
        save_database_updates(db_store)
    else:
        data_store.set(db_store)        
    return {
        'message_id': message_id,
    }
         
         
