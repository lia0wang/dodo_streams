import re
import os
from src.dm import dm_create_v1
from src.helper import get_data,is_database_exist, check_valid_token,\
     decode_jwt,save_database_updates, datetime_to_unix_time_stamp
from src.channel import channel_details_v1, channel_messages_v1
from src.channels import channels_list_v1
from src.data_store import data_store
from src.error import InputError, AccessError

def message_send_v1(token, channel_id, message):
    '''
    Send a message from the authorised user to the channel specified
    by channel_id. Note: Each message should have its own unique ID,
    i.e. no messages should share an ID with another message, even if
    that other message is in a different channel.
    Assumption: returning type message_id is dict contains integer message
    id
    Arguments:
        token - Used to identify the user
        channel_id - Refers to the channel where message will be sent 
        message - The message needs to be send
    Exceptions:
        InputError - channel_id does not refer to a valid channel
        InputError - the length of message is smaller than 1 or bigger than 1000
        AccessError - channel_id is valid and the authorised user is not a
                      member of the channel
         Return Value:
         Return a dictionary containing the message id              
    '''
    is_member = False
    valid_channel = False
    
    # Fetch data
    if(len(message)<1 or len(message)>1000):
        raise InputError("Error: message too long or too short")
    db_store = data_store.get()
    if is_database_exist() == True:
        db_store = get_data()
        
    #Get authorised user id 
    auth_user_id = decode_jwt(token)['u_id']
            
    #Check channel_id is valid
    #Also check if the authorised user is not a member of the channel

    for chan in db_store['channels']:
        if chan['channel_id'] == channel_id:
            target_channel = chan
            valid_channel = True
    if valid_channel == False:
        raise InputError("channel_id does not refer to a valid channel")
            
    for user in target_channel['all_members']:
        if user['u_id'] == auth_user_id:
            # Check if authorised user is a member of the channel
            is_member = True 
            break               
   
    if is_member == False:
        raise AccessError("Authorised user is not a member of the channel")
   
    message_id = db_store['message_index']
    db_store['message_index']+=1
    
    # creates the unix time_stamp
    timestamp = datetime_to_unix_time_stamp()

    message = {
        'message_id': message_id,
        'u_id': auth_user_id,
        'message': message,
        'channel_id': channel_id,
        'time_created': timestamp
    }

    target_channel['messages'].append(message)
    db_store['messages'].append(message)
    
    if is_database_exist:
        save_database_updates(db_store)
    else:
        data_store.set(db_store)

    return {
        'message_id': message_id,
        'time_created': timestamp
    }

def message_edit_v1(token, message_id, message):
    '''
    Given a message, update its text with new text.
    If the new message is an empty string, the message is deleted.
    Arguments:
        token - Used to identify the user
        message_id - Refers to the message will be edited
        message - The message needs to be send
    Exceptions:
        InputError - message_id does not refer to a valid message within
                     a channel /DM that the authorised user has joined
        InputError - the length of message is bigger than 1000
        AccessError - the message was not sent by the authorised user making t
                      his request, and the authorised user has owner permissions
                      in the channel/DM
         Return Value:
             N/A        
    '''
    # Fetch data
    
    if len(message)>1000:
        raise InputError("Error: message too long")
    '''
    elif len(message)<1:
        message_remove_v1(token, message_id)
        return None
        
    db_store = data_store.get()
    if is_database_exist() == True:
        db_store = get_data()
        
    #Get authorised user id 
    auth_user_id = decode_jwt(token)['u_id']
            
    #Check channel_id is valid
    #Also check if the authorised user is not a member of the channel

    channel_list = channels_list_v1(auth_user_id)
    target_message = {}
    messgae_ids = [m['message_id'] for m in db_store['messages']]
    if message_id not in messgae_ids:
        print ("message_id", message_id)
        print("messgae_ids", messgae_ids)
        raise InputError("Error: message_id does not refer to a \
                         valid message within a channel")
    for msg in db_store['messages']:
        if msg['message_id'] == message_id:
            target_message = msg
        
    target_channel_id = target_message['channel_id']

    channel_ids = [chan['channel_id'] for chan in channel_list['channels']]
    print(target_channel_id)
    
    print(auth_user_id)
    print(channel_ids)
    if target_channel_id not in channel_ids:
        raise InputError("Error: message_id does not refer to a \
                         valid message within the current channel")
    
    if target_message['u_id'] == auth_user_id:
        auth_request = True

    ownership = channel_details_v1(auth_user_id, target_channel_id)['owner_members']
    print(ownership)
    if auth_user_id not in ownership:
            has_owner_permission = True
            
    if has_owner_permission == False and auth_request == False:
        raise AccessError("Authorised user does not have owner permisson \
                          of the channel or the message was not sent by the \
                          authorised user making this request")
    
    # creates the unix time_stamp
    timestamp = datetime_to_unix_time_stamp()

    message = {
        'message_id': message_id,
        'u_id': auth_user_id,
        'message': message,
        'time_created': timestamp
    }

    target_channel = db_store['channels'][target_channel_id-1]
    target_channel['messages'].append(message)
    db_store['messages'].append(message)
    if is_database_exist:
        save_database_updates(db_store)
    else:
        data_store.set(db_store)
    '''



def message_remove_v1(token, message_id):
    '''
    Given a message_id for a message, this message is removed from
    the channel/DM.
    Assumption: A meesage can not be removed twice.
    Arguments:
        token - Used to identify the user
        message_id - Refers to the message will be removed
    Exceptions:
        InputError - message_id does not refer to a valid message within
                     a channel /DM that the authorised user has joined
        AccessError - the message was not sent by the authorised user making t
                      his request, and the authorised user has owner permissions
                      in the channel/DM
         Return Value:
             N/A        
    '''
    # Fetch data
    auth_request = False
    has_owner_permission = False

    db_store = data_store.get()
    if is_database_exist() == True:
        db_store = get_data()
        
    #Get authorised user id 
    auth_user_id = decode_jwt(token)['u_id']
            
    #Check channel_id is valid
    #Also check if the authorised user is not a member of the channel
    
    channel_list = channels_list_v1(auth_user_id)
    target_message = {}
    messgae_ids = [m['message_id'] for m in db_store['messages']]
    if message_id not in messgae_ids:
        raise InputError("Error: message_id does not refer to a \
                         valid message within a channel")
    for msg in db_store['messages']:
        if msg['message_id'] == message_id:
            target_message = msg
        
    target_channel_id = target_message['channel_id']

    channel_ids = [chan['channel_id'] for chan in channel_list['channels']]
    print(target_channel_id)
    
    print(auth_user_id)
    print(channel_ids)
    if target_channel_id not in channel_ids:
        raise InputError("Error: message_id does not refer to a \
                         valid message within the current channel")
    
    if target_message['u_id'] == auth_user_id:
        auth_request = True

    ownership = channel_details_v1(auth_user_id, target_channel_id)['owner_members']
    print(ownership)
    if auth_user_id not in ownership:
            has_owner_permission = True
            
    if has_owner_permission == False and auth_request == False:
        raise AccessError("Authorised user does not have owner permisson \
                          of the channel or the message was not sent by the \
                          authorised user making this request")

    target_channel = db_store['channels'][target_channel_id-1]
    print(target_channel['messages'])
    target_channel['messages'].remove(target_message)
    db_store['message_index']-=1

    db_store['messages'].remove(target_message)
    if is_database_exist:
        save_database_updates(db_store)
    else:
        data_store.set(db_store)
    
def message_senddm_v1(token, dm_id, message):
    '''
    Send a message from authorised_user to the DM specified by dm_id.
    Arguments:
        token - Used to identify the user
        dm_id - Used to identify the dm will be sent 
        message - The dm needs to be send
    Exceptions:
    InputError - the length of message is smaller than 1 or bigger than 1000
    AccessError - dm_id is valid and the authorised user is not a
                      member of the DM
         Return Value:
         Return a dictionary containing the message id of the dm message     
    '''
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

         
         
