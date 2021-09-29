from src.data_store import data_store
from src.error import AccessError, InputError

def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
    # Fetch data
    store = data_store.get()

    # Check if auth_user_id refers to existing user
    valid_user = False
    for user in store['users']:
        if user['u_id'] == auth_user_id:
            valid_user = True
    if valid_user == False:
        raise InputError("Error: Invalid auth_user_id")
    
    # Check if channel_id refers to valid channel
    # Find and save target channel if it exists
    valid_channel = False
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            target_channel = channel
            valid_channel = True
    if valid_channel == False:
        raise InputError("Error: Invalid channel_id")

    # Check if authorised user is a member of the target channel
    # Search list of members in the target channel
    is_member = False
    for member in target_channel['all_members']:
        if member['u_id'] == auth_user_id:
            is_member = True
    if is_member == False:
        raise AccessError("Error: Authorised user is not a member")

    # Return details
    return {
        'name': target_channel['name'],
        'is_public': target_channel['is_public'],
        'owner_members': target_channel['owner_members'],
        'all_members': target_channel['all_members']
    }

def channel_messages_v1(auth_user_id, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_join_v1(auth_user_id, channel_id):
    """
    Add authorised users to the channel with given channel_id
    Arguments:
        auth_user_id (int) - The ID of the authorised valid user
        channel_id (int)   - The ID of the channel where the user will join in
    Exceptions:
        InputError  - Channel_id is invalid
        AccessError - Channel_id refers to a channel that is private
                      and the authorised user is not already a channel member
                      and is not a global owner
    Return Value:
        Return an empty dictionary
    """

    # Fetch data
    store = data_store.get()
    
    # Check if the auth_user_id is valid
    valid = False
    for user in store['users']:
        if user['u_id'] == auth_user_id:
            new_member = user # Catch the new_member
            valid = True
    if valid == False:
        raise AccessError("Invalid user ID!")
    
    # Check if the channel_id is valid
    valid = False
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            valid = True
            target_channel = channel # Catch the channel where the new_member is gonna join
    if valid == False:
        raise InputError("Invalid channel ID!")
    
    # A user can't join a channel where he is alreday a member.
    for old_member in target_channel['all_members']:
        if old_member['u_id'] == new_member['u_id']:
            raise AccessError("Sorry, you can't join the same channel agian.")

    # A user can't join the private channel when the use is not a member nor a global owner.
    if target_channel['is_public'] == False:
        raise AccessError("Sorry, you can't join the private channel.")

    # Append the new member to the target channel
    target_channel['all_members'].append(new_member)
    data_store.set(store)

    return {
    }
