import re
import os
from src.dm import dm_create_v1, dm_details_v1
from src.helper import get_data, check_valid_token,\
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
        'time_created': timestamp,
        'is_pinned': False
    }

    target_channel['messages'].append(message)  
    save_database_updates(db_store)

    return {
        'message_id': message_id,
        'time_created': timestamp
    }

def message_edit_v1(token, message_id, new_message):
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
    auth_request = False
    has_owner_permission = False
    valid_channel_message = False
    valid_dm = False
    if len(new_message)>1000:
        raise InputError("Error: message too long")
    
    elif len(new_message)<1:
        message_remove_v1(token, message_id)
        return None

    db_store = get_data()
        
    #Get authorised user id 
    auth_user_id = decode_jwt(token)['u_id']
            
    #Check message_id is valid
    #Also check if the authorised user is not an owner member of the channel
    for user in db_store['users']:
        if user['u_id'] == auth_user_id:
            targer_user = user
            
    for channel in db_store['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                valid_channel_message = True
                if message['u_id'] == auth_user_id:
                    auth_request = True
                for users in channel['owner_members']:
                    if auth_user_id == users['u_id']:
                        has_owner_permission = True
                if targer_user['permission_id'] == 1:
                    has_owner_permission = True
                if has_owner_permission == False and auth_request == False:
                    raise AccessError("Authorised user does not have owner permisson \
                          of the channel or the message was not sent by the \
                          authorised user making this request")
    if valid_channel_message and auth_request:
        for channel in db_store['channels']:
            for msg in channel['messages']:
                if msg['message_id'] == message_id:
                    msg['message'] = new_message
                    save_database_updates(db_store)
    
    for dm in db_store['dms']:
        for message in dm['messages']:
            if message['message_id'] == message_id:
                valid_dm = True
                dm_id = message['dm_id']
                dm_owner = dm_details_v1(auth_user_id, dm_id)['members'][0]
                if message['u_id'] == auth_user_id:
                    auth_request = True
                elif dm_owner['u_id'] == auth_user_id:
                    auth_request = True       
                if valid_dm == True and auth_request == False:
                    raise AccessError("Authorised user does not have owner permisson \
                          of the channel or the message was not sent by the \
                          authorised user making this request")
            if not valid_dm:
                raise InputError("Error: message_id does not refer to a \
                         valid message within the current dm")
                
    if valid_dm and auth_request:
        for dm in db_store['dms']:
            for message in dm['messages']:
                if message['message_id'] == message_id:
                    dm['messages'] = new_message
                    save_database_updates(db_store)

    if valid_dm == False and valid_channel_message == False:
        raise InputError("Error: message_id oes not refer to a valid message within \
                         a channel /DM that the authorised user has joined")   

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
    valid_channel_message = False
    valid_dm = False

    db_store = get_data()
        
    #Get authorised user id 
    auth_user_id = decode_jwt(token)['u_id']
            
    #Check message_id is valid
    #Also check if the authorised user is not an owner member of the channel
    for user in db_store['users']:
        if user['u_id'] == auth_user_id:
            targer_user = user
            
    #Remove channel messages       
    for channel in db_store['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                valid_channel_message = True
                if message['u_id'] == auth_user_id:
                    auth_request = True        
                for users in channel['owner_members']:
                    if auth_user_id == users['u_id']:
                        has_owner_permission = True
                if targer_user['permission_id'] == 1:
                    has_owner_permission = True
                if has_owner_permission == False and auth_request == False:
                    raise AccessError("Authorised user does not have owner permisson \
                          of the channel or the message was not sent by the \
                          authorised user making this request")
                
    if valid_channel_message and auth_request:
        for channel in db_store['channels']:
            for message in channel['messages']:
                if message['message_id'] == message_id:
                    channel['messages'].remove(message)
                    save_database_updates(db_store)
        
    #Remove dm messages
    for dm in db_store['dms']:
        for message in dm['messages']:
            if message['message_id'] == message_id:
                dm_id = message['dm_id']
                dm_owner = dm_details_v1(auth_user_id, dm_id)['members'][0]
                valid_dm = True
                if message['u_id'] == auth_user_id:
                    auth_request = True
                elif dm_owner['u_id'] == auth_user_id:
                    auth_request = True
                if valid_dm == True and auth_request == False:
                    raise AccessError("Authorised user does not have owner permisson \
                          of the channel or the message was not sent by the \
                          authorised user making this request")
                
    if valid_dm and auth_request:
        for dm in db_store['dms']:
            for message in dm['messages']:
                if message['message_id'] == message_id:
                    dm['messages'].remove(message)
                    save_database_updates(db_store)               

    if valid_dm == False and valid_channel_message == False:
        raise InputError("Error: message_id does not refer to a valid message within \
                         a channel /DM that the authorised user has joined")
                  
    
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
    valid_dm = False
    if(len(message)<1 or len(message)>1000):
        raise InputError("Error: message too long or too short")

    db_store = get_data()
    #Get authorised user id 
    auth_user_id = decode_jwt(token)['u_id']
    for user in db_store['users']:
        if user['u_id'] == auth_user_id:
            targer_user = user    

    #Check if dm_id is not valid
    for dm in db_store['dms']:
        if dm['dm_id'] == dm_id:
            target_dm = dm
            valid_dm = True
            if dm['auth_user_id'] == auth_user_id:
                is_member = True # Check if authorised user is a member of the dm
            for members in dm_details_v1(auth_user_id, dm_id)['members']:
                if targer_user['u_id'] == members['u_id']:
                    is_member = True # Check if authorised user is a member of the dm

    if is_member == False and valid_dm == True:
        raise AccessError(description="Authorised user is not a member of DM")
    if valid_dm == False:
        raise InputError(description="dm_id does not refer to a valid dm id")
   
    message_id = db_store['message_index']
    db_store['message_index']+=1

    # creates the unix time_stamp
    timestamp = datetime_to_unix_time_stamp()
    
    dm_message = {
        'message_id': message_id,
        'u_id': auth_user_id,
        'message': message,
        'dm_id':dm_id,
        'time_created': timestamp,
        'is_pinned': False
    }

    target_dm['messages'].append(dm_message)
    save_database_updates(db_store)
       
    return {
        'message_id': message_id,
    }


def message_pin_v1(token, message_id):
    store = get_data()

    u_id = decode_jwt(token)['u_id']

    if store['message_index'] <= message_id:
        raise InputError(description="Error: message_id does not refer to a valid message")

    for user in store['users']:
        if user['u_id'] == u_id:
            targer_user = user
    
    in_channel_dm = False
    is_pinned = False
    owner_permission = False

    #Checking in channels       
    for channel in store['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                if message['is_pinned']:
                    is_pinned = True
                for users in channel['all_members']:
                    if u_id == users['u_id']:
                        in_channel_dm = True
                for users in channel['owner_members']:
                    if u_id == users['u_id']:
                        owner_permission = True
                if targer_user['permission_id'] == 1:
                    owner_permission = True

                if not in_channel_dm:
                    raise InputError(description="Authorised user is not a member of the channel")

                if not owner_permission:
                    raise AccessError(description="Authorised user does not have owner permissions")

                if is_pinned:
                    raise InputError(description="Message is already pinned")
                
    if in_channel_dm and owner_permission:
        for channel in store['channels']:
            for message in channel['messages']:
                if message['message_id'] == message_id:
                    message['is_pinned'] = True
                    save_database_updates(store)

    in_channel_dm = False
    owner_permission = False

    #Checking in dms
    for dm in store['dms']:
        for message in dm['messages']:
            if message['message_id'] == message_id:
                if message['is_pinned']:
                    is_pinned = True
                for users in channel['all_members']:
                    if u_id == users['u_id']:
                        in_channel_dm = True
                for users in channel['owner_members']:
                    if u_id == users['u_id']:
                        owner_permission = True
                if targer_user['permission_id'] == 1:
                    owner_permission = True

                if not in_channel_dm:
                    raise InputError(description="Authorised user is not a member of the channel")

                if not owner_permission:
                    raise AccessError(description="Authorised user does not have owner permissions")

                if is_pinned:
                    raise InputError(description="Message is already pinned")
                
    if in_channel_dm and owner_permission:
        for dm in store['dms']:
            for message in dm['messages']:
                if message['message_id'] == message_id:
                    message['is_pinned'] = True
                    save_database_updates(store)

    return {}