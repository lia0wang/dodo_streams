from src.data_store import data_store
from src.helper import save_database_updates

empty = {
    "users": [],
    "channels": [],
    "messages": [],
    "dms": [],
    "reset_tokens": [],
    "log_history": [],
    "message_index": 0
}

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
    data_store.set(empty)
    save_database_updates(empty)    
    return {
    }
