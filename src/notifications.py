from src.data_store import data_store
from src.error import AccessError, InputError
from src.helper import get_data

def notifications_v1(auth_user_id):
    """
    Return the user's most recent 20 notifications, ordered from most recent to 
    least recent.   
    Arguments:

    Return Value:
        Returns start on condition that start <= total messages
        Returns end 
        Returns messages 
    """

    store = get_data()
    
    log_history = store['log_history']
    notifications = []
    log_history.reverse()
    for notif in log_history:
        # finds the user who requested notifications
        if auth_user_id == notif['u_id']:
            #channel_id = get_channel_id(notif)
            #dm_id = get_dm_id(notif)
            notif_message = create_notification_message(notif)
            notification = {
                'channel_id': notif['channel_id'],
                'dm_id': notif['dm_id'],
                'notification_message': notif_message
            }
            notifications.append(notification)
            
    return notifications

def create_notification_message(notif):
    if notif['notif_type'] == 'channel_invite' or notif['notif_type'] == 'dm_create':
        return(f"added to a channel/DM: {notif['handle_str']} added you to {notif['channel/dm_name']}")
    elif notif['notif_type'] == 'message_react':
        return(f"{notif['handle_str']} reacted to your message in {notif['channel/dm_name']}")
    return(f"{notif['handle_str']} tagged you in {notif['channel/dm_name']}: {notif['notif_type']}")

