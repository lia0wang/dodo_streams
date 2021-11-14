from src.data_store import data_store


def clear_v1():
    '''
    Resets the internal data of the application to its initial state

    Arguments:
        N/A
    Exceptions:
        N/A
    Return Value:
        N/A  
    '''
    empty = {
        "users": [],
        "channels": [],
        "messages": [],
        "dms": [],
        "reset_tokens": [],
        "log_history": [],
        "message_index": 0,
        'message_count': 0,
        'workspace_stats': {
            'channels_exist': [{'num_channels_exist':0,'time_stamp':0}],
            'dms_exist': [{'num_dms_exist':0,'time_stamp':0}],
            'messages_exist': [{'num_messages_exist':0,'time_stamp':0}],
            'utilization_rate': 0
            }
    }
    data_store.set(empty)    
    return {}
