'''
data_store.py

This contains a definition for a Datastore class which you should use to store your data.
You don't need to understand how it works at this point, just how to use it :)

The data_store variable is global, meaning that so long as you import it into any
python file in src, you can access its contents.

Example usage:

    from data_store import data_store

    store = data_store.get()
    print(store) # Prints { 'names': ['Nick', 'Emily', 'Hayden', 'Rob'] }

    names = store['names']

    names.remove('Rob')
    names.append('Jake')
    names.sort()

    print(store) # Prints { 'names': ['Emily', 'Hayden', 'Jake', 'Nick'] }
    data_store.set(store)
'''

## YOU SHOULD MODIFY THIS OBJECT BELOW
'''
from src.helper import datetime_to_unix_time_stamp

time_stamp = datetime_to_unix_time_stamp()
'''


initial_object = {
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
## YOU SHOULD MODIFY THIS OBJECT ABOVE

class Datastore:
    def __init__(self):
        self.__store = initial_object

    def get(self):
        return self.__store

    def set(self, store):
        if not isinstance(store, dict):
            raise TypeError('store must be of type dictionary')
        self.__store = store

print('Loading Datastore...')

global data_store
data_store = Datastore()

