from src.data_store import data_store
import os
# import database

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
    store = data_store.get()
    store['users'] = []
    store['channels'] = []
    store['messages'] = []
    data_store.set(store)

    open('database.json', 'w').close()
    
    # os.remove()
    
    return {
    }
