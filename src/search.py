from src.helper import get_data, search_channel_messages, search_dm_messages
from src.error import InputError

def search_v1(u_id, query_str):
    if len(query_str) not in range(1, 1001):
        raise InputError(description="Error: query string is greater than 1000 characters")
    messages = []
    db_store = get_data()
    for channel in db_store["channels"][::-1]:
        channel_messages = search_channel_messages(u_id, channel, query_str)
        messages.extend(channel_messages)
    for dm in db_store["dms"][::-1]:
        dm_messages = search_dm_messages(u_id, dm, query_str)
        messages.extend(dm_messages)
    return messages





