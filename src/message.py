import re
import os
from src.dm import dm_create_v1
from src.helper import get_data,is_database_exist, check_valid_token, decode_jwt
from src.data_store import data_store
from src.error import InputError, AccessError

def send_v1(token, channel_id, message):
    # Fetch data
    if(len(message)<1 or len(message)>1000):
        raise InputError("Error: message too long or too short")
    db_store = data_store.get()
    if is_database_exist() == True:
        db_store = get_data()
        if check_valid_token(token) == True:
            #get authorised user id 
            u_id = decode_jwt(token)['u_id']
            
            #Check channel_id is valid
            #Also check if the authorised user is not a member of the channel
            valid = False
            for user in db_store['users']:
                if user['u_id'] == u_id:
                    valid = True
                if not valid:
                    raise InputError(description="Authorised u_id does not refer to a valid user")
                
            is_member = False
            valid_channel = False
            for chan in db_store['channels']:
                if chan['channel_id'] == channel_id:
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
            
    return {
    'message_id': message_id,
    }
            
    
def senddm_v1(token, dm_id, message):
    # Fetch data
    if(len(message)<1 or len(message)>1000):
        raise InputError("Error: message too long or too short")
    db_store = data_store.get()
    if is_database_exist() == True:
        db_store = get_data()
        if check_valid_token(token) == True:
            #Get authorised user id 
            u_id = decode_jwt(token)['u_id']

            #Check if dm_id is not valid
            valid = False
            for dm in db_store['dms']:
                if dm['dm_id'] == dm_id:
                    valid = True
                if not valid:
                    raise InputError(description="dm_id does not refer to a valid user")
                
            is_member = False

            for dm in db_store['dms']:
                if dm['auth_user_id'] == u_id:
                    is_member = True# Check if authorised user is a member of the channel
                    break
   
    if is_member == False:
        raise AccessError("Authorised user is not a member of DM")
   
    #seek_target_channel_and_errors(db_store, u_id, channel_id)
    message_id = db_store['message_index']
    db_store['message_index']+=1
            
    return {
    'message_id': message_id,
    }
         
         
