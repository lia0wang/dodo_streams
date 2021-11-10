from src.helper import get_data, search_channel_messages, search_dm_messages
from src.error import InputError

def search_v1(u_id, query_str):
    """
    Given u_id and a query string, returns all messages in channels and dms 
    with that query string.

    Arguments:
        u_id (int)       
        query_str (str)

    Exceptions:
        InputError - query string is greater than 1000 characters

    Return Value:
        returns list of message dictionaries
        Each dictionary contains:
            message_id (int)
            u_id (int)
            message (string)
            time_created (int)
            reacts (list of react dictionaries)
            is_pinned (bool)
    """
    if len(query_str) not in range(1, 1001):
        raise InputError(description="Error: query string is greater than 1000 characters")
    messages = []
    db_store = get_data()
    # Fetch and append channel messages with query_str
    for channel in db_store["channels"]:
        channel_messages = search_channel_messages(u_id, channel, query_str)
        messages.extend(channel_messages)
    # Fetch and append dm messages with query_str
    for dm in db_store["dms"]:
        dm_messages = search_dm_messages(u_id, dm, query_str)
        messages.extend(dm_messages)
    return messages





