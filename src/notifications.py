from src.data_store import data_store
from src.error import AccessError, InputError
from src.helper import get_data, seek_target_channel_and_errors, save_database_updates

def notifications_v1(auth_user_id):
    """
    Return the user's most recent 20 notifications, ordered from most recent to 
    least recent.   
    Arguments:
        
    Exceptions:
        InputError  - Channel_id is invalid
        InputError - start is greater than the total number of messages in the 
                    channel
        AccessError - channel_id is valid and the authorised user is not a 
                        member of the channe;
    Return Value:
        Returns start on condition that start <= total messages
        Returns end 
        Returns messages 
    """

    store = get_data()
    
    log_history = store['log_history']
    #Note reverse for some reason is causing problems
    log_history = log_history.reverse()
    notifications = []
    
    for notif in store['log_history']:
        if auth_user_id == notif['u_id']:
            channel_id = get_channel_id(notif)
            dm_id = get_dm_id(notif)
            notif_message = create_notification_message(notif)
            notification = {
                'channel_id': channel_id,
                'dm_id': dm_id,
                'notification_message': notif_message
            }
            notifications.append(notification)
            
    return notifications

def get_channel_id(notif):
    if "channel_id" in notif:
        return notif['channel_id']
    else:
        return -1

def get_dm_id(notif):
    if "dm_id" in notif:
        return notif['channel_id']
    else:
        return -1

def create_notification_message(notif):
    if notif['notif_type'] == 'channel_invite':
        return(f"added to a channel/DM: {notif['handle_str']} added you to {notif['channel_name']}")
